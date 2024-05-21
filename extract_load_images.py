'''Este script descarga las imágenes de los números de Alerta Amber y las sube a un bucket de S3'''
import pandas as pd
import boto3
from src.utils import download_images_for_numbers

# Path to the CSV file
CSV_FILE_PATH = "./data/chiapas.csv"

# Read the CSV file into a DataFrame
chiapas = pd.read_csv(CSV_FILE_PATH)

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
IMAGES_FOLDER = "./data/images"

# para 3 dígitos
# List of numbers
numbers_to_download = list_3_digits + [398]


# Download images for the specified numbers
download_images_for_numbers(numbers_to_download, IMAGES_FOLDER, 3)

# para 4 dígitos
# List of numbers
numbers_to_download = list_4_digits

# Download images for the specified numbers
download_images_for_numbers(numbers_to_download, IMAGES_FOLDER, 4)

# Abres un cliente de S3
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
