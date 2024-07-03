import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
PARQUET_FILE_PATH = os.getenv('PARQUET_FILE_PATH')
SORTED_DATA_FILE_PATH = os.getenv('SORTED_DATA_FILE_PATH')

# Read the parquet file
data_dir = Path(str(PARQUET_FILE_PATH))
full_df = pd.concat(
    pd.read_parquet(parquet_file)
    for parquet_file in data_dir.glob('*.parquet')
)

# Sort the DataFrame by the 'unique_mem_id' column
df_sorted = full_df.sort_values(by='unique_mem_id')

# Output the sorted DataFrame to a CSV file
df_sorted.to_csv(SORTED_DATA_FILE_PATH, index=False)

