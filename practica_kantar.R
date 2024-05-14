#Cargamos las librerias
library(dplyr)
library(readr)
library(magrittr)

# Definimos la función para cargar el archivo
process_data <- function(file_path) {
  # Convertimos el csv a una DF
  df <- read_csv(file_path)
  
  # Añadimos nueva columna
  set.seed(123)  # Fijamos un número arbitrario de randomness
  df <- df %>% mutate(`Nueva columna` = runif(n()))
  
  # Guardamos el archivo en un csv
  write_csv(df, file_path)
}

# Obtenemos el archivo de la linea de comandos
args <- commandArgs(trailingOnly = TRUE)
file_path <- args[1]

# Procesamos la data
process_data(file_path)
