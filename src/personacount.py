from function import *
from pathlib import Path
import os
import json
from dotenv import load_dotenv

load_dotenv()
SORTED_DATA_FILE_PATH = os.getenv('SORTED_DATA_FILE_PATH')
PERSONAS_DATA_FILE_PATH = os.getenv('PERSONAS_DATA_FILE_PATH')
PERSONAS_SUMMARY_FILE_PATH = os.getenv('PERSONAS_SUMMARY_FILE_PATH')
PERSONA_GROUPS_DATA_FILE_PATH = os.getenv('PERSONA_GROUPS_DATA_FILE_PATH')
PERSONA_GROUPS_SUMMARY_FILE_PATH = os.getenv('PERSONA_GROUPS_SUMMARY_FILE_PATH')
PARQUET_FILE_PATH = os.getenv('PARQUET_FILE_PATH')

# Read the parquet file
data_dir = Path(str(PARQUET_FILE_PATH))
full_df = pd.concat(
    pd.read_parquet(parquet_file)
    for parquet_file in data_dir.glob('*.parquet')
)

#Read in the data to a dataframe
df = pd.read_csv(SORTED_DATA_FILE_PATH)

#Select necessary columns and convert to dictionary for processing
selectedf = df.iloc[:, :3]
data_dict = full_df.pivot(index='unique_mem_id', columns='Final_Attribute_Name', values='AMOUNT').to_dict(orient='index')

#Process the data and store it within a new dictionary
cust_scored = process_data(data_dict)

#Evaluate and store corresponding members into their categories
i_lists = evaluator(cust_scored, "individual")
g_lists = evaluator(cust_scored, "group")

#Evaluate total
total_people = len(pd.unique(full_df.iloc[1:, 0]))

#Open output files
i_data_file = open(PERSONAS_DATA_FILE_PATH, 'w+')
i_summary_file = open(PERSONAS_SUMMARY_FILE_PATH, 'w+')
g_data_file = open(PERSONA_GROUPS_DATA_FILE_PATH, 'w+')
g_summary_file = open(PERSONA_GROUPS_SUMMARY_FILE_PATH, 'w+')

i_list_people = 0

# Output persona summary statistics
for list_name, lst in i_lists.items():
    list_length = len(lst)
    i_list_people += list_length
    list_percentage = (list_length / total_people) * 100
    print(f"Amount of people in {(list_name + ':'):60s} {list_length} ({list_percentage:.2f}% of {total_people})", file=i_summary_file)
print(f"Total amount of people: {i_list_people} ({i_list_people / total_people * 100:.2f}% of {total_people})", file=i_summary_file)

g_list_people = 0

for list_name, lst in g_lists.items():
    list_length = len(lst)
    g_list_people += list_length
    list_percentage = (list_length / total_people) * 100
    print(f"Amount of people in {(list_name + ':'):60s} {list_length} ({list_percentage:.2f}% of {total_people})", file=g_summary_file)
print(f"Total amount of people: {g_list_people} ({g_list_people / total_people * 100:.2f}% of {total_people})", file=g_summary_file)

# Output persona data
json_data = json.dumps(i_lists)
print(json_data, file=i_data_file)

json_data = json.dumps(g_lists)
print(json_data, file=g_data_file)

# Close output files
i_summary_file.close()
i_data_file.close()
g_summary_file.close()
g_data_file.close()