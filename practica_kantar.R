# Ensure necessary packages are installed
required_packages <- c("dplyr", "readr", "magrittr", "httr")
new_packages <- required_packages[!(required_packages %in% installed.packages()[,"Package"])]

if(length(new_packages)) install.packages(new_packages)

# Load libraries
library(dplyr)
library(readr)
library(magrittr)
library(httr)

# Define the function to process the data
process_data <- function(file_path) {
  # Download the CSV file from Dropbox
  dropbox_download(file_path, "data_actualizar.csv")
  
  # Read the CSV file into a DataFrame
  df <- read_csv("data_actualizar.csv")
  
  # Add a new column with random values
  set.seed(123)  # Set a seed for reproducibility
  df <- df %>% mutate(`Nueva columna` = runif(n()))
  
  # Write the updated DataFrame back to a CSV file
  write_csv(df, "data_actualizar.csv")
  
  # Upload the updated CSV file back to Dropbox
  dropbox_upload("data_actualizar.csv", file_path)
}

# Function to download a file from Dropbox
dropbox_download <- function(dropbox_path, local_path) {
  url <- "https://content.dropboxapi.com/2/files/download"
  res <- httr::POST(url,
                    httr::add_headers("Authorization" = paste("Bearer", Sys.getenv("DROPBOX_TOKEN")),
                                      "Dropbox-API-Arg" = paste0("{\"path\": \"", dropbox_path, "\"}")),
                    httr::write_disk(local_path, overwrite = TRUE))
  
  if (res$status_code != 200) {
    stop("Failed to download file from Dropbox")
  }
}

# Function to upload a file to Dropbox
dropbox_upload <- function(local_path, dropbox_path) {
  url <- "https://content.dropboxapi.com/2/files/upload"
  res <- httr::POST(url,
                    httr::add_headers("Authorization" = paste("Bearer", Sys.getenv("DROPBOX_TOKEN")),
                                      "Dropbox-API-Arg" = paste0("{\"path\": \"", dropbox_path, "\", \"mode\": \"overwrite\"}"),
                                      "Content-Type" = "application/octet-stream"),
                    body = upload_file(local_path))
  
  if (res$status_code != 200) {
    stop("Failed to upload file to Dropbox")
  }
}

# Get the file path from command line arguments
args <- commandArgs(trailingOnly = TRUE)
file_path <- args[1]

# Process the data
process_data(file_path)



