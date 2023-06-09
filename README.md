# Filtered Data Downloader


This is a Streamlit app that allows users to upload an Excel, CSV or JSON file and filter it based on a selected column. The app then creates a new Excel file for each unique value in the selected column and downloads them as a zip file.


## Getting Started

### Prerequisites
Python 3.7+

Streamlit 1.0+

Pandas 1.5+

Openpyxl 3.0+

### Installation
Clone the repository:
```sh
git clone https://github.com/hakyemezi/filterandsave.git
```
Navigate to the cloned repository
```sh
cd https://github.com/hakyemezi/filterandsave.git
```
Install the required Python libraries:
```sh
pip install -r requirements.txt
```
### Usage
1.	Start the app:
```sh
streamlit run filterandsave.py
```
2.	Upload an Excel, CSV or JSON file.
3.	Select the column you want to filter on.
4.	Click the "Start" button.
5.	Download the zip file containing the created Excel files.

## Demo

A demo of this project is available on https://hakyemezi-filterandsave.streamlit.app

