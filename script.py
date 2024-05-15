import sys
import os
import dropbox
import pandas as pd
import numpy as np
from io import BytesIO

def process_data(file_path):
    # Autenticamos Dropbox
    dropbox_token = os.getenv('DROPBOX_TOKEN')
    dbx = dropbox.Dropbox(dropbox_token)

    # Bajamos el CSV desde dropbox
    _, res = dbx.files_download(file_path)
    data = res.content

    # Convertimos el CSV en un DF
    df = pd.read_csv(BytesIO(data))

    # Mantenemos la primera fila y columna, añadimos valores nuevos y calculamos totales
    np.random.seed(123)  # Ponemos 123 como semilla de aleatoreidad para reproduccion
    df.iloc[1:, 1:] = np.random.randint(2000000, 2600000, size=(df.shape[0]-1, df.shape[1]-1))
    df.iloc[1:, 1:] = df.iloc[1:, 1:].astype(int)
    df.iloc[0, 1:] = df.iloc[1:, 1:].sum(axis=0)

    # Convertimos el DF en CSV nuevamente
    csv_data = df.to_csv(index=False, lineterminator='\n').encode('utf-8')

    # Subimos el nuevo CSV de vuelta a DROPBOX
    dbx.files_upload(csv_data, file_path, mode=dropbox.files.WriteMode.overwrite)

if __name__ == '__main__':
    # Obtenemos el filepath desde archivos del sistema
    file_path = sys.argv[1]

    # Procesamos la data
    process_data(file_path)
