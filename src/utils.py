import os
import requests
import PyPDF2
import pandas as pd
import numpy as np
from json import loads, dumps


def scrapeado_pdf(digitos, letra):

    # Base URL of the webpage to scrape for PDFs
    base_url_pdf = (
        "https://appalertaamber.fgr.org.mx/Alerta/CreaAlertaPDFPublico?numero_reporte="
    )

    # Create folders if they don't exist
    current_directory = os.getcwd()
    data_folder = os.path.join(os.path.dirname(current_directory), "data")
    pdf_folder = os.path.join(data_folder, "pdf")

    for folder in [data_folder, pdf_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Generate links by changing the last 4 digits
    links = [base_url_pdf + str(i).zfill(digitos) for i in range(1, 10**digitos)]

    # Iterate over the links and send requests to retrieve PDFs
    for index, pdf_link in enumerate(links, start=1):
        # Sending request for PDF link
        response_pdf = requests.get(pdf_link)
        if response_pdf.status_code == 200:
            # Save the PDF to the pdf folder
            pdf_path = os.path.join(pdf_folder, f"{letra}_{index}.pdf")
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(response_pdf.content)
            print("Downloaded PDF:", pdf_path)

            # Read the content of the PDF
            try:
                with open(pdf_path, "rb") as pdf_file:
                    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                    text = ""
                    for page_num in range(pdf_reader.numPages):
                        text += pdf_reader.getPage(page_num).extractText()

                    # Check if the string "Publicación no disponible" is present in the text
                    if "Publicación no disponible" in text:
                        os.remove(pdf_path)  # Delete the PDF file
                        print("Deleted PDF:", pdf_path)
            except PyPDF2.utils.PdfReadError:
                print("Failed to read PDF:", pdf_path)
        else:
            print("Failed to retrieve data for PDF link:", pdf_link)


# Function to read PDF files from a directory
def read_pdfs_from_directory(directory):
    # List all files in the directory
    files = os.listdir(directory)

    # Filter out only PDF files
    pdf_files = [file for file in files if file.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the directory.")
        return None

    # Create an empty list to store DataFrames for each PDF
    pdf_data_list = []

    # Iterate over each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        # print(f"Reading PDF file: {pdf_path}")

        # Open the PDF file
        with open(pdf_path, "rb") as file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfFileReader(file)

            # Get number of pages in the PDF
            num_pages = pdf_reader.numPages

            # Initialize text for each page
            pdf_text = ""

            # Extract text from each page
            for page_num in range(num_pages):
                page = pdf_reader.getPage(page_num)
                pdf_text += page.extractText()

            # Store the text and the last 4 digits of the PDF file name in a DataFrame
            id_file = pdf_file[0:-4]  # Extract the last 4 digits from the file name
            pdf_data_list.append(
                pd.DataFrame({"Text": [pdf_text], "id_file": [id_file]})
            )

    # Concatenate all DataFrames in the list into a single DataFrame
    pdf_data = pd.concat(pdf_data_list, ignore_index=True)

    return pdf_data


base_url_image = (
    "https://appalertaamber.fgr.org.mx/Alerta/ObtenerFotoDesaparecido?numero_reporte="
)


# Function to download images for a list of numbers
def download_images_for_numbers(numbers, images_folder, digits):
    # Create images folder if it doesn't exist
    current_directory = os.getcwd()
    data_folder = os.path.join(os.path.dirname(current_directory), "data")
    images_folder_path = os.path.join(data_folder, images_folder)

    if not os.path.exists(images_folder_path):
        os.makedirs(images_folder_path)

    # Iterate over the list of numbers
    for number in numbers:
        # Generate the image link for the current number
        image_link = base_url_image + str(number).zfill(digits)

        # Sending request for image link
        response_image = requests.get(image_link)
        if response_image.status_code == 200:
            # Save the image to the images folder
            image_path = os.path.join(images_folder_path, f"image_{number}.jpg")
            with open(image_path, "wb") as img_file:
                img_file.write(response_image.content)
            # print("Downloaded image:", image_path)
        else:
            print("Failed to retrieve data for image link:", image_link)
