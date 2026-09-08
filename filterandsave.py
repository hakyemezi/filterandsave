import streamlit as st
import pandas as pd
import zipfile
import io
import os
import re

from translations import LANGUAGES, TRANSLATIONS, DOT_SEPARATOR, SPACE_SEPARATOR

st.set_page_config(page_title="Split a spreadsheet by column", page_icon="✂️", layout="wide")

# The language has to be picked before any text is written, so the selector
# comes first. set_page_config cannot be translated, it runs before this.
#
# Every language is listed with its flag rather than hidden behind a dropdown,
# so a visitor can see their own language without opening anything. Streamlit
# has already written the new choice into session state by the time this runs,
# which is why the label can be shown in the language being switched to.
current_language = st.session_state.get("language", "en")

language = st.sidebar.radio(
    "🌐 " + TRANSLATIONS[current_language]["language"],
    list(LANGUAGES.keys()),
    format_func=lambda code: f"{LANGUAGES[code][0]} {LANGUAGES[code][1]}",
    key="language",
)


def t(key):
    # Fall back to English so a missing translation never breaks the page
    return TRANSLATIONS[language].get(key) or TRANSLATIONS["en"][key]


def number(value):
    # 1,234 in English, 1.234 in Turkish, German, Spanish and Italian,
    # 1 234 in French
    text = f"{value:,}"
    if language in DOT_SEPARATOR:
        return text.replace(",", ".")
    if language in SPACE_SEPARATOR:
        return text.replace(",", " ")
    return text


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


st.title(t("title"))
st.caption(t("caption"))

uploaded_file = st.file_uploader(t("uploader"), type=["xlsx", "csv", "json"])

if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()
    file_type = os.path.splitext(uploaded_file.name)[1].lower()

    # An Excel file can hold several sheets, so ask which one to work on
    sheet = 0
    if file_type == ".xlsx":
        sheet_names = pd.ExcelFile(io.BytesIO(file_bytes)).sheet_names
        if len(sheet_names) > 1:
            sheet = st.selectbox(t("sheet_pick"), sheet_names)

    df = read_uploaded_file(file_bytes, uploaded_file.name, sheet)

    st.success(t("loaded").format(rows=number(len(df)), cols=len(df.columns)))
    with st.expander(t("preview")):
        st.dataframe(df.head(50), use_container_width=True)

    st.subheader(t("step1"))

    column_list = list(df.columns)
    split_columns = st.multiselect(
        t("split_label"),
        column_list,
        default=column_list[:1],
        help=t("split_help"),
    )

    if split_columns:

        drop_empty = st.checkbox(t("drop_empty"), value=True)

        keep_columns = st.multiselect(
            t("keep_label"),
            column_list,
            default=column_list,
            help=t("keep_help"),
        )

        if not keep_columns:
            st.warning(t("keep_warn"))
            st.stop()

        groups = build_groups(df, split_columns, keep_columns, drop_empty)

        if not groups:
            st.warning(t("no_groups"))
            st.stop()

        st.subheader(t("step2"))

        summary = pd.DataFrame(
            {t("col_group"): [label for label, _ in groups],
             t("col_rows"): [len(group) for _, group in groups]}
        )
        covered = int(summary[t("col_rows")].sum())

        left, right = st.columns([1, 2])
        with left:
            st.metric(t("m_groups"), number(len(groups)))
            st.metric(t("m_rows"), number(covered))
            st.metric(t("m_largest"), t("rows_value").format(n=number(int(summary[t("col_rows")].max()))))
            skipped = len(df) - covered
            if skipped:
                st.metric(t("m_skipped"), number(skipped))
        with right:
            st.dataframe(summary, use_container_width=True, hide_index=True, height=260)

        st.subheader(t("step3"))

        # Selected by position rather than by label, so the choice keeps
        # working whatever language the interface is in
        delivery = st.radio(
            t("output_label"),
            [0, 1, 2],
            format_func=lambda index: t(f"opt{index}"),
            help=t("output_help"),
        )

        if delivery == 0 and len(groups) > 200:
            st.info(t("many_sheets").format(n=number(len(groups))))

        if st.button(t("build"), type="primary"):

            with st.spinner(t("building").format(n=number(len(groups)))):

                if delivery == 0:
                    output = io.BytesIO()
                    used = {}
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        for label, group in groups:
                            group.to_excel(writer, sheet_name=sheet_name(label, used), index=False)

                    st.download_button(
                        t("dl_workbook"),
                        output.getvalue(),
                        file_name="split.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

                else:
                    zip_buffer = io.BytesIO()
                    used_names = {}

                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                        for label, group in groups:
                            # Two labels can clean up to the same name, so keep them apart
                            name = safe_name(label)
                            used_names[name] = used_names.get(name, 0) + 1
                            if used_names[name] > 1:
                                name = f"{name}_{used_names[name]}"

                            if delivery == 2:
                                zip_file.writestr(f"{name}.csv", group.to_csv(index=False).encode("utf-8-sig"))
                            else:
                                excel_buffer = io.BytesIO()
                                group.to_excel(excel_buffer, index=False)
                                zip_file.writestr(f"{name}.xlsx", excel_buffer.getvalue())

                    st.download_button(
                        t("dl_zip"),
                        zip_buffer.getvalue(),
                        file_name="split.zip",
                        mime="application/zip",
                    )

            st.success(t("ready"))
