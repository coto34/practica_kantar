import sys
import dropbox
import pandas as pd
import numpy as np
from io import BytesIO

def process_data(file_path):
    # Authenticate with Dropbox
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)

    # Download the CSV file from Dropbox
    _, res = dbx.files_download(file_path)
    data = res.content

    # Read the CSV file into a DataFrame
    df = pd.read_csv(BytesIO(data))

    # Maintain the first row and column, add new values, and calculate totals
    np.random.seed(123)  # Set a seed for reproducibility
    df.iloc[1:, 1:] = np.random.randint(2000000, 2600000, size=(df.shape[0]-1, df.shape[1]-1))
    df.iloc[1:, 1:] = df.iloc[1:, 1:].astype(int)
    df.iloc[0, 1:] = df.iloc[1:, 1:].sum(axis=0)

    # Convert the updated DataFrame back to CSV
    csv_data = df.to_csv(index=False).encode('utf-8')

    # Upload the updated CSV file back to Dropbox
    dbx.files_upload(csv_data, file_path, mode=dropbox.files.WriteMode.overwrite)

if __name__ == '__main__':
    # Get the file path from command line arguments
    file_path = sys.argv[1]

    # Process the data
    process_data(file_path)


