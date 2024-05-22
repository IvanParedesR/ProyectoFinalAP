# main script
import os
import logging
from src.utils import scrapeado_pdf, read_pdfs_from_directory, get_logger

# Configurar logging
logger = get_logger("ExtractReadPDF")
logger.info("Comenzando scrapeado ...")

# Para 4 dígitos y letra A
# scrapeado_pdf(4, "A", logger)

# Para 3 dígitos y letra B
scrapeado_pdf(3, "B", logger)

# Directory containing files
PDF_DIRECTORY = "./data/pdf"
DATA_DIRECTORY = "./data"

# Check if the directory exists
if not os.path.exists(PDF_DIRECTORY):
    logger.info(f"Directory '{PDF_DIRECTORY}' does not exist.")
else:
    # Read PDFs from the directory
    pdf_dataframe = read_pdfs_from_directory(PDF_DIRECTORY, logger)

    if pdf_dataframe is not None:
        logger.info("\nData from PDFs:")
        logger.info(pdf_dataframe.head().to_string())

csv_file_path = os.path.join(DATA_DIRECTORY, "pdf_data_raw.csv")
if pdf_dataframe is not None:
    pdf_dataframe.to_csv(csv_file_path, index=False)
    logger.info(f"\nDataFrame saved to CSV file at: {csv_file_path}")
