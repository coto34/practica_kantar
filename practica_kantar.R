# Ensure necessary libraries are installed
if (!requireNamespace("googledrive", quietly = TRUE)) {
  install.packages("googledrive")
}
if (!requireNamespace("dplyr", quietly = TRUE)) {
  install.packages("dplyr")
}
if (!requireNamespace("readr", quietly = TRUE)) {
  install.packages("readr")
}
if (!requireNamespace("magrittr", quietly = TRUE)) {
  install.packages("magrittr")
}

# Load libraries
library(dplyr)
library(readr)
library(magrittr)
library(googledrive)

# Authenticate Google Drive
drive_auth(path = "credentials.json")

# Process the data
data_procesamiento <- function(file_id) {
  # Download the CSV file from Google Drive
  drive_download(as_id(file_id), path = "data_actualizar.csv", overwrite = TRUE)
  
  # Read the CSV file into a DataFrame
  df <- read_csv("data_actualizar.csv")
  
  # Update only numerical columns with random values
  df_numeric <- df %>% select(where(is.numeric))
  df_numeric[] <- lapply(df_numeric, function(x) runif(length(x)))
  
  # Combine the modified numeric columns back with the original dataframe
  df %>% mutate(across(where(is.numeric), ~ runif(n())))
  
  # Write the updated DataFrame back to a CSV file
  write_csv(df, "data_actualizar.csv")
  
  # Upload the updated CSV back to Google Drive
  drive_update(as_id(file_id), media = "data_actualizar.csv")
}

# Get the file ID from the arguments
args <- commandArgs(trailingOnly = TRUE)
file_id <- args[1]

# Process the data
data_procesamiento(file_id)


