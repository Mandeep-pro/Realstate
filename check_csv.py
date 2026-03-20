import pandas as pd
import sys

try:
    # Try to read the CSV from the attachment location
    df = pd.read_csv('indian_real_estate_data.csv')
    print("Columns:", df.columns.tolist())
    print("\nShape:", df.shape)
    print("\nFirst row:")
    print(df.iloc[0])
    print("\nData types:")
    print(df.dtypes)
except Exception as e:
    print(f"Error: {e}")
