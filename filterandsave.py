import streamlit as st
import pandas as pd
import zipfile
import io
import os
import re


def safe_name(value):
    # Turn a cell value into a name that is safe to use inside the zip file
    name = re.sub(r'[\\/:*?"<>|]', "_", str(value)).strip()
    return (name or "unnamed")[:100]


# Create a file uploader on the screen
uploaded_file = st.file_uploader("Upload Excel / CSV / JSON file", type=["xlsx", "csv", "json"])

# Create a listbox on the screen
if uploaded_file is not None:

    # Specify the type of selected file
    file_type = os.path.splitext(uploaded_file.name)[1].lower()

    # Determine the appropriate read function according to the type of selected file
    if file_type == ".xlsx":
        df = pd.read_excel(uploaded_file)
    elif file_type == ".csv":
        df = pd.read_csv(uploaded_file)
    elif file_type == ".json":
        df = pd.read_json(uploaded_file)

    # Process the dataframe as needed
    column_list = list(df.columns)
    selected_column = st.selectbox("Select the column you want to process:", column_list)

    # Create a Start button on the screen
    if st.button("Start"):

        # Filter data based on the selected column
        filtered_df = df[df[selected_column].notna()]

        # Create a new Excel file for each unique value in the selected column.
        # Everything is built in memory, so concurrent users never overwrite
        # each other's files on the server.
        zip_buffer = io.BytesIO()
        used_names = {}

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for value in filtered_df[selected_column].unique():
                filtered_data = filtered_df[filtered_df[selected_column] == value]

                # Two different values can clean up to the same name, so keep them apart
                name = safe_name(value)
                used_names[name] = used_names.get(name, 0) + 1
                if used_names[name] > 1:
                    name = f"{name}_{used_names[name]}"

                excel_buffer = io.BytesIO()
                filtered_data.to_excel(excel_buffer, index=False)
                zip_file.writestr(f"{name}.xlsx", excel_buffer.getvalue())

        # Create a download button for the zip file containing the created Excel files
        st.download_button(
            "Download Zip",
            zip_buffer.getvalue(),
            file_name="filtered_data.zip",
            mime="application/zip",
        )
