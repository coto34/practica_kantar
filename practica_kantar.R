install.packages("googledrive") # Instalamos la librería

# Cargamos librerias
library(dplyr)
library(readr)
library(magrittr)
library(googledrive)

# Autenticamos Google drive
drive_auth(path = "credentials.json")

# Procesamos los datos
data_procesamiento <- function(file_id) {
  # Download the CSV file from Google Drive
  drive_download(as_id(file_id), path = "data_actualizar.csv", overwrite = TRUE)
  
  # Read the CSV file into a DataFrame
  df <- read_csv("data_actualizar.csv")
  
  # Añadimos una columna con valores aleatorios
  set.seed(123)  # Seteamos una semilla para reproducir
  df <- df %>% mutate(`Nueva columna` = runif(n()))
  
  # Convertimos de nuevo el archivo a csv
  write_csv(df, "data_actualizar.csv")
  
  # Retornamos el archivo CSV a google drive
  drive_update(as_id(file_id), media = "data_actualizar.csv")
}

# Obtenemos el ID de los argumentos
args <- commandArgs(trailingOnly = TRUE)
file_id <- args[1]

# Procesamos los datos
data_procesamiento(file_id)

