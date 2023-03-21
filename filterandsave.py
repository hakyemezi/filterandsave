import streamlit as st
import pandas as pd
import zipfile
import os

# Create a file uploader on the screen
uploaded_file = st.file_uploader("Upload Excel / CSV / JSON file", type=["xlsx", "csv", "json"])

# Create a listbox on the screen
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column_list = list(df.columns)
    selected_column = st.selectbox("Select the column you want to process:", column_list)

# Create a Start button on the screen
if st.button("Start"):
    if selected_column is not None:
        # Filter data based on the selected column
        filtered_df = df[df[selected_column].notna()]
        
        # Create a new Excel file for each unique value in the selected column
        for value in filtered_df[selected_column].unique():
            filtered_data = filtered_df[filtered_df[selected_column] == value]
            filtered_data.to_excel(f"{value}.xlsx", index=False)
        
        # Create a download link to download the zip file containing the created Excel files
        file_paths = [f"{value}.xlsx" for value in filtered_df[selected_column].unique()]
        with zipfile.ZipFile("filtered_data.zip", "w") as zip_file:
            for file in file_paths:
                zip_file.write(file)
        with open('filtered_data.zip', 'rb') as f:
            st.download_button('Download Zip', f, file_name='filtered_data.zip')
       # st.markdown(f"### [Download the file](filtered_data.zip)")

        # Delete the created files
        for file in file_paths:
            os.remove(file)
        os.remove("filtered_data.zip")
