import pandas as pd
import sys

if len(sys.argv) != 2:
    print("Usage: python3 load.py")
    sys.exit(1)

file_path = sys.argv[1]

try:
    df = pd.read_excel(file_path)
    print("Dataset loaded successfully!")
    print(df.head())
except Exception as e:
    print(f"Error loading the dataset: {e}")
# save dataset for next step
df.to_csv("/home/doc-bd-a1/loaded_data.csv", index=False)
