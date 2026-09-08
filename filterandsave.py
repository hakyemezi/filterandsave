import streamlit as st
import pandas as pd
import zipfile
import io
import os
import re

st.set_page_config(page_title="Split a spreadsheet by column", page_icon="✂️", layout="wide")


def safe_name(value):
    # Turn a cell value into a name that is safe to use as a file name
    name = re.sub(r'[\\/:*?"<>|]', "_", str(value)).strip()
    return (name or "unnamed")[:100]


def sheet_name(value, used):
    # Excel sheet names are limited to 31 characters, cannot contain : \ / ? * [ ]
    # and have to be unique inside the workbook
    name = re.sub(r'[\\/:*?\[\]]', "_", str(value)).strip()[:31] or "unnamed"
    if name in used:
        used[name] += 1
        suffix = f"_{used[name]}"
        name = name[:31 - len(suffix)] + suffix
    else:
        used[name] = 1
    return name


def read_uploaded_file(file_bytes, file_name, sheet):
    # Read whichever format was uploaded into a DataFrame
    file_type = os.path.splitext(file_name)[1].lower()
    buffer = io.BytesIO(file_bytes)

    if file_type == ".xlsx":
        return pd.read_excel(buffer, sheet_name=sheet)
    elif file_type == ".csv":
        return pd.read_csv(buffer)
    elif file_type == ".json":
        return pd.read_json(buffer)
    return None


def build_groups(df, split_columns, keep_columns, drop_empty):
    # Split the frame into one group per unique combination of the chosen columns
    frame = df.dropna(subset=split_columns) if drop_empty else df.copy()

    groups = []
    for keys, group in frame.groupby(split_columns, dropna=False, sort=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        label = " - ".join(safe_name(key) for key in keys)
        groups.append((label, group[keep_columns]))

    return groups


st.title("✂️ Split a spreadsheet by column")
st.caption(
    "Upload an Excel, CSV or JSON file, choose the column to split it on, and get back "
    "one file per value — or one workbook with a separate sheet per value. "
    "Splits on several columns at once, and shows you what you will get before it builds anything."
)

uploaded_file = st.file_uploader("Excel, CSV or JSON file", type=["xlsx", "csv", "json"])

if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()
    file_type = os.path.splitext(uploaded_file.name)[1].lower()

    # An Excel file can hold several sheets, so ask which one to work on
    sheet = 0
    if file_type == ".xlsx":
        sheet_names = pd.ExcelFile(io.BytesIO(file_bytes)).sheet_names
        if len(sheet_names) > 1:
            sheet = st.selectbox("This workbook has several sheets. Which one?", sheet_names)

    df = read_uploaded_file(file_bytes, uploaded_file.name, sheet)

    st.success(f"Loaded **{len(df):,} rows** and **{len(df.columns)} columns**.")
    with st.expander("Preview the data"):
        st.dataframe(df.head(50), use_container_width=True)

    st.subheader("1. How should it be split?")

    column_list = list(df.columns)
    split_columns = st.multiselect(
        "Split on these columns",
        column_list,
        default=column_list[:1],
        help="Pick more than one to split on a combination, for example region and year.",
    )

    if split_columns:

        drop_empty = st.checkbox("Skip rows with no value in those columns", value=True)

        keep_columns = st.multiselect(
            "Columns to keep in the output",
            column_list,
            default=column_list,
            help="Leave every column selected to keep the files as they are.",
        )

        if not keep_columns:
            st.warning("Select at least one column to keep.")
            st.stop()

        groups = build_groups(df, split_columns, keep_columns, drop_empty)

        if not groups:
            st.warning("Splitting on those columns produced no groups.")
            st.stop()

        st.subheader("2. This is what you will get")

        summary = pd.DataFrame(
            {"Group": [label for label, _ in groups],
             "Rows": [len(group) for _, group in groups]}
        )

        left, right = st.columns([1, 2])
        with left:
            st.metric("Groups", f"{len(groups):,}")
            st.metric("Rows covered", f"{int(summary['Rows'].sum()):,}")
            st.metric("Largest group", f"{int(summary['Rows'].max()):,} rows")
            skipped = len(df) - int(summary["Rows"].sum())
            if skipped:
                st.metric("Rows skipped", f"{skipped:,}")
        with right:
            st.dataframe(summary, use_container_width=True, hide_index=True, height=260)

        st.subheader("3. How should it come back?")

        delivery = st.radio(
            "Output",
            ["One Excel workbook, a sheet per group",
             "Separate Excel files in a zip",
             "Separate CSV files in a zip"],
            help="A workbook with one sheet per group is the option a spreadsheet cannot give you on its own.",
        )

        if delivery.startswith("One Excel") and len(groups) > 200:
            st.info(f"{len(groups):,} groups means {len(groups):,} sheets in one workbook, which is slow to open. A zip may work better here.")

        if st.button("Build it", type="primary"):

            with st.spinner(f"Building {len(groups):,} groups"):

                if delivery.startswith("One Excel"):
                    output = io.BytesIO()
                    used = {}
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        for label, group in groups:
                            group.to_excel(writer, sheet_name=sheet_name(label, used), index=False)

                    st.download_button(
                        "Download workbook",
                        output.getvalue(),
                        file_name="split.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

                else:
                    as_csv = delivery.endswith("zip") and "CSV" in delivery
                    zip_buffer = io.BytesIO()
                    used_names = {}

                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                        for label, group in groups:
                            # Two labels can clean up to the same name, so keep them apart
                            name = safe_name(label)
                            used_names[name] = used_names.get(name, 0) + 1
                            if used_names[name] > 1:
                                name = f"{name}_{used_names[name]}"

                            if as_csv:
                                zip_file.writestr(f"{name}.csv", group.to_csv(index=False).encode("utf-8-sig"))
                            else:
                                excel_buffer = io.BytesIO()
                                group.to_excel(excel_buffer, index=False)
                                zip_file.writestr(f"{name}.xlsx", excel_buffer.getvalue())

                    st.download_button(
                        "Download zip",
                        zip_buffer.getvalue(),
                        file_name="split.zip",
                        mime="application/zip",
                    )

            st.success("Ready.")
