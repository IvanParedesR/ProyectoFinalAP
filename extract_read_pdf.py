'''Este  script scrapea los datos de los PDFs de la página de Alerta Amber'''
import os
from src.utils import scrapeado_pdf, read_pdfs_from_directory

# Para 4 dígitos y letra A
# scrapeado_pdf(4, "A")

# Para 3 dígitos y letra B
scrapeado_pdf(3, "B")

# Directory containing files
PDF_DIRECTORY = "./data/pdf"
DATA_DIRECTORY = "./data"

# Check if the directory exists
if not os.path.exists(PDF_DIRECTORY):
    print(f"Directory '{PDF_DIRECTORY}' does not exist.")
else:
    # Read PDFs from the directory
    pdf_dataframe = read_pdfs_from_directory(PDF_DIRECTORY)

    if pdf_dataframe is not None:
        print("\nData from PDFs:")
        print(pdf_dataframe.head())

csv_file_path = os.path.join(DATA_DIRECTORY, "pdf_data_raw.csv")
pdf_dataframe.to_csv(csv_file_path, index=False)
print(f"\nDataFrame saved to CSV file at: {csv_file_path}")
