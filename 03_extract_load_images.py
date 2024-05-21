import os
import requests
import PyPDF2
import pandas as pd
import numpy as np
from json import loads, dumps
from src.utils import download_images_for_numbers

# Path to the CSV file
csv_file_path = "./data/chiapas.csv"

# Read the CSV file into a DataFrame
chiapas = pd.read_csv(csv_file_path)

# Display the first few rows of the DataFrame
print(chiapas.head())

### Crear lista para descargar imágenes

df2 = pd.DataFrame(chiapas["id_file"])
df2[["digitos", "num"]] = df2["id_file"].str.split("_", n=1, expand=True)

df_A = df2[df2["digitos"] == "A"]
df_B = df2[df2["digitos"] == "B"]

list_4_digits = df_A["num"].tolist()
list_3_digits = df_B["num"].tolist()


# Folder to save images
images_folder = "./data/images"

# para 3 dígitos
# List of numbers
numbers_to_download = list_3_digits + [398]


# Download images for the specified numbers
download_images_for_numbers(numbers_to_download, images_folder, 3)

# para 4 dígitos
# List of numbers
numbers_to_download = list_4_digits

# Download images for the specified numbers
download_images_for_numbers(numbers_to_download, images_folder, 4)

# Abres un cliente de S3
import boto3

session = boto3.Session(profile_name="arquitectura", region_name="us-east-1")
s3 = session.client("s3")


BUCKET_NAME = "itam-proyecto-saraluz"


# List of image names
image_names = list_4_digits + list_3_digits
print(image_names)

# Loop through each image name and upload to S3
for image_name in image_names:
    file_path = f"./data/images/image_{image_name}.jpg"
    s3_key = f"image_{image_name}.jpg"
    s3.upload_file(Filename=file_path, Bucket=BUCKET_NAME, Key=s3_key)
