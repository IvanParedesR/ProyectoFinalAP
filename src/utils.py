import os
import requests
from datetime import datetime
import logging
import PyPDF2
import pandas as pd


# Función para configurar logging
def get_logger(archivo_log):
    """This function configures the logging module to save
    the logs in a file"""
    now = datetime.now()
    date_time = now.strftime("%Y%m%d_%H%M%S")
    log_train_file_name = f"logs/{date_time}_{archivo_log}.log"
    logging.basicConfig(
        filename=log_train_file_name,
        level=logging.DEBUG,
        filemode="w",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(log_train_file_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def scrapeado_pdf(digitos, letra, logger):
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

    links = [base_url_pdf + str(i).zfill(digitos) for i in range(1, 10**digitos)]

    for index, pdf_link in enumerate(links, start=1):
        response_pdf = requests.get(pdf_link, timeout=10)
        if response_pdf.status_code == 200:
            pdf_path = os.path.join(pdf_folder, f"{letra}_{index}.pdf")
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(response_pdf.content)
            logger.info("Downloaded PDF: %s", pdf_path)

            try:
                with open(pdf_path, "rb") as pdf_file:
                    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                    text = ""
                    for page_num in range(pdf_reader.numPages):
                        text += pdf_reader.getPage(page_num).extractText()

                    if "Publicación no disponible" in text:
                        os.remove(pdf_path)
                        logger.info("Deleted PDF: %s", pdf_path)
            except PyPDF2.errors.PdfReadError:
                logger.info("Failed to read PDF: %s", pdf_path)
        else:
            logger.info("Failed to retrieve data for PDF link: %s", pdf_link)


def read_pdfs_from_directory(directory, logger):
    """
    Esta función lee los PDFs descargados y extrae el texto de los mismos.
    """
    files = os.listdir(directory)
    pdf_files = [file for file in files if file.lower().endswith(".pdf")]

    if not pdf_files:
        logger.info("No PDF files found in the directory.")
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
            logger.info("Failed to retrieve data for image link:", image_link)
