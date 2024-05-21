"""
Este script contiene las funciones necesarias para realizar el scrapeo
de los PDFs y las imágenes de la página web de Alerta Amber de la
Fiscalía General de la República de México. Además, contiene una función
para leer los PDFs descargados y extraer el texto de los mismos.
"""

import os
import requests
import PyPDF2
import pandas as pd


def scrapeado_pdf(digitos, letra):
    """
    Esta función descarga los PDFs de la página web de Alerta Amber.
    """
    base_url_pdf = (
        "https://appalertaamber.fgr.org.mx/Alerta/CreaAlertaPDFPublico?"
        "numero_reporte="
    )
    current_directory = os.getcwd()
    data_folder = os.path.join(os.path.dirname(current_directory), "data")
    pdf_folder = os.path.join(data_folder, "pdf")

    for folder in [data_folder, pdf_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    links = [base_url_pdf +
             str(i).zfill(digitos) for i in range(1, 10**digitos)]

    for index, pdf_link in enumerate(links, start=1):
        response_pdf = requests.get(pdf_link, timeout=10)
        if response_pdf.status_code == 200:
            pdf_path = os.path.join(pdf_folder, f"{letra}_{index}.pdf")
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(response_pdf.content)
            print("Downloaded PDF:", pdf_path)

            try:
                with open(pdf_path, "rb") as pdf_file:
                    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                    text = ""
                    for page_num in range(pdf_reader.numPages):
                        text += pdf_reader.getPage(page_num).extractText()

                    if "Publicación no disponible" in text:
                        os.remove(pdf_path)
                        print("Deleted PDF:", pdf_path)
            except PyPDF2.errors.PdfReadError:
                print("Failed to read PDF:", pdf_path)
        else:
            print("Failed to retrieve data for PDF link:", pdf_link)


def read_pdfs_from_directory(directory):
    """
    Esta función lee los PDFs descargados y extrae el texto de los mismos.
    """
    files = os.listdir(directory)
    pdf_files = [file for file in files if file.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the directory.")
        return None

    pdf_data_list = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            pdf_text = ""

            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                pdf_text += page.extractText()

            id_file = pdf_file[0:-4]
            pdf_data_list.append(
                pd.DataFrame({"Text": [pdf_text], "id_file": [id_file]})
            )

    pdf_data = pd.concat(pdf_data_list, ignore_index=True)
    return pdf_data


def download_images_for_numbers(numbers, images_folder, digits):
    """
    Esta función descarga las imágenes de los números de
    Alerta Amber y las sube a un bucket de S3.
    """
    base_url_image = (
        "https://appalertaamber.fgr.org.mx/Alerta/ObtenerFotoDesaparecido?"
        "numero_reporte="
    )
    current_directory = os.getcwd()
    data_folder = os.path.join(os.path.dirname(current_directory), "data")
    images_folder_path = os.path.join(data_folder, images_folder)

    if not os.path.exists(images_folder_path):
        os.makedirs(images_folder_path)

    for number in numbers:
        image_link = base_url_image + str(number).zfill(digits)
        response_image = requests.get(image_link, timeout=10)
        if response_image.status_code == 200:
            image_path = os.path.join(images_folder_path,
                                      f"image_{number}.jpg")
            with open(image_path, "wb") as img_file:
                img_file.write(response_image.content)
        else:
            print("Failed to retrieve data for image link:", image_link)
