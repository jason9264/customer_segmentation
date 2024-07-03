# Envestnet User Segmentation Project

## Prerequsites
Make sure Python version 3.11.6 or greater is installed.

Make sure all packages are installed. 
If packages are not installed, make sure the working directory is in the root directory for this code base. 
Use `py [or python] -m pip install -r requirements.txt` to install all packages needed.

Make sure user data is accessible in a parquet or csv format.

Make sure a .env file is defined in the root directory for this code base.
The .env file should look like the following:
```
PARQUET_FILE_PATH = ""
SORTED_DATA_FILE_PATH = ""
OUTPUT_FILE_PATH = ""
PERSONAS_DATA_FILE_PATH = ""
PERSONAS_SUMMARY_FILE_PATH = ""
PERSONA_GROUP_DATA_FILE_PATH = ""
PERSONA_GROUP_SUMMARY_FILE_PATH = ""
```
With all empty string values replaced with the appropriate values.

## Running

To output values for all users by attribute, run `py src/io/createAttributeToCSV.py`.
The result will be csv files for each attribute in the specified OUTPUT_FILE_PATH.

To output values for all users sorted by their user id, run `py src/io/sortToCSV.py`.
The result will be a csv file will all the data sorted by user id in the specified SORTED_DATA_FILE_PATH.

To output information about the personas, run `py src/personacount.py`.
The result will be a json data file will each persona and its fitting users in the specified PERSONAS_DATA_FILE_PATH and each persona group and its fitting users in the specified PERSONA_GROUP_DATA_FILE_PATH.
The result will be a text summary file with count/breakdown for each persona for the data in the specified PERSONAS_SUMMARY_FILE_PATH and each persona group for the data in the specified PERSONA_GROUP_SUMMARY_FILE_PATH.

## Testing

To test on the terminal, use `py -m coverage run -m unittest`.

To test and view code coverage, use `py -m coverage html`.
Coverage can be viewed by looking at the index.html file in the htmlcov directory.
