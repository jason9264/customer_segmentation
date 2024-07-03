import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
PARQUET_FILE_PATH = os.getenv('PARQUET_FILE_PATH')
OUTPUT_FILE_PATH = os.getenv('OUTPUT_FILE_PATH')

# Read the parquet file
data_dir = Path(str(PARQUET_FILE_PATH))
full_df = pd.concat(
    pd.read_parquet(parquet_file)
    for parquet_file in data_dir.glob('*.parquet')
)

# Define the column name
column_name = 'Final_Attribute_Name'

# Get unique values in the specified column
list_of_all_attributes = list(full_df[column_name].unique())

# Create a directory to save the CSV files
output_directory = os.path.join(OUTPUT_FILE_PATH)
os.makedirs(output_directory, exist_ok=True)

# Loop through unique values and save CSV files
for att in list_of_all_attributes:
        # Replace '/' with '+'
    df_att = full_df[full_df[column_name] == att]
    clean_att = att.replace('/', '+')
    output_path = os.path.join(output_directory, 'attribute_'+str(clean_att)+ '.csv')
    df_att.to_csv(output_path, index=False)

print("Conversion complete.")