import sys
import os
import dropbox
import pandas as pd
import numpy as np
from io import BytesIO

def process_data(file_path):
    
    dropbox_token = os.getenv('DROPBOX_TOKEN')
    dbx = dropbox.Dropbox(dropbox_token)

    
    _, res = dbx.files_download(file_path)
    data = res.content

    
    df = pd.read_csv(BytesIO(data))

    
    np.random.seed(123)  
    df.iloc[1:, 1:] = np.random.randint(2000000, 2600000, size=(df.shape[0]-1, df.shape[1]-1))
    df.iloc[1:, 1:] = df.iloc[1:, 1:].astype(int)
    df.iloc[0, 1:] = df.iloc[1:, 1:].sum(axis=0)

    
    csv_data = df.to_csv(index=False, line_terminator='\n', encoding='utf-8').encode('utf-8')

   
    dbx.files_upload(csv_data, file_path, mode=dropbox.files.WriteMode.overwrite)

if __name__ == '__main__':
    
    file_path = sys.argv[1]

    
    process_data(file_path)
