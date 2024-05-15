import sys
import os
import dropbox
import pandas as pd
import numpy as np
from io import BytesIO

# Define DROPBOX_TOKEN using the environment variable
DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN')

def process_data(file_path):
    # Authenticate with Dropbox
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)

    # Download the CSV file from Dropbox
    _, res = dbx.files_download(file_path)
    data = res.content

    # Read the CSV file into a DataFrame with proper encoding
    df = pd.read_csv(BytesIO(data), encoding='utf-8', quotechar='"', skipinitialspace=True)

    # Debug: Print the DataFrame to verify its structure
    print(df.head())

    # Ensure the DataFrame is read correctly
    if df.columns[0] != "AÑOS" or df.iloc[1, 0] != "Total Categorías":
        print("Error: CSV structure is not as expected.")
        return

    # Set random seed for reproducibility
    np.random.seed(123)
    
    # Update values below "Total Categorías" with random values between 2,000,000 and 2,600,000
    for col in df.columns[1:]:  # Skip the first column
        df.loc[2:, col] = np.random.randint(2000000, 2600000, size=len(df) - 2)
    
    # Recalculate the totals for "Total Categorías"
    for col in df.columns[1:]:  # Skip the first column
        df.at[1, col] = df[col].iloc[2:].sum()

    # Ensure the first column and first row remain unchanged
    df.iloc[0, 0] = "AÑOS"
    df.iloc[1, 0] = "Total Categorías"
    df.iloc[2:, 0] = ["Marca " + str(i) for i in range(1, len(df) - 1)]

    # Convert the updated DataFrame back to CSV with proper encoding
    csv_data = df.to_csv(index=False, encoding='utf-8').encode('utf-8')

    # Upload the updated CSV file back to Dropbox
    try:
        dbx.files_upload(csv_data, file_path, mode=dropbox.files.WriteMode.overwrite)
        print("File uploaded successfully to Dropbox.")
    except Exception as e:
        print(f"Error uploading file to Dropbox: {e}")

if __name__ == '__main__':
    # Get the file path from command line arguments
    file_path = sys.argv[1]

    # Process the data
    process_data(file_path)
