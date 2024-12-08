import pandas as pd
import os

# Number of rows per split (except the last one)
N_ROWS_PER_SPLIT = 100_000

# Get current folder name
current_folder = os.path.basename(os.getcwd())

# Get list of all parquet files in current folder
files = os.listdir(".")
parquet_files = [f for f in files if f.endswith('.parquet')]

if not parquet_files:
    raise FileNotFoundError("No parquet files found in current folder")

# Read and combine all parquet files
dfs = []
for file in parquet_files:
    file_path = os.path.join(".", file)
    df = pd.read_parquet(file_path)
    dfs.append(df)

# Concatenate all dataframes
combined_df = pd.concat(dfs, ignore_index=True)

# Split the dataframe
num_splits = 10 # total 907_464 so need 10 splits each max 100_000 (N_ROWS_PER_SPLIT)
split_size = N_ROWS_PER_SPLIT
remainder_size = len(combined_df) - (num_splits -1) * split_size


splits = []
start_index = 0
for i in range(num_splits - 1):
    end_index = start_index + split_size
    splits.append(combined_df[start_index:end_index])
    start_index = end_index
splits.append(combined_df[start_index:])


# Create split folders if they don't exist
for i in range(1, num_splits + 1):
    split_folder = f'split_{current_folder}_{i}'
    if not os.path.exists(split_folder):
        os.makedirs(split_folder)

# Save each split as parquet and csv
for i, df_split in enumerate(splits):
    split_number = i + 1
    output_base = f'{current_folder}_split_{split_number}'
    split_folder = f'split_{current_folder}_{split_number}'
    df_split.to_parquet(f'{split_folder}/{output_base}.parquet')
    df_split.to_csv(f'{split_folder}/{output_base}.csv', index=False)

print(f"Created split files in folders split_{current_folder}_1 to split_{current_folder}_{num_splits}")
