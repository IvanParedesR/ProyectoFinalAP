import os
import requests
import PyPDF2
import pandas as pd
import numpy as np
from json import loads, dumps
from src.utils import scrapeado_pdf, read_pdfs_from_directory


# Para 4 dígitos y letra A
# scrapeado_pdf(4, "A")

# Para 3 dígitos y letra B
scrapeado_pdf(3, "B")

# Directory containing files
pdf_directory = "./data/pdf"
data_directory = "./data"

# Check if the directory exists
if not os.path.exists(pdf_directory):
    print(f"Directory '{pdf_directory}' does not exist.")
else:
    # Read PDFs from the directory
    pdf_dataframe = read_pdfs_from_directory(pdf_directory)

    if pdf_dataframe is not None:
        print("\nData from PDFs:")
        print(pdf_dataframe.head())  # Display the first few rows of the DataFrame

csv_file_path = os.path.join(data_directory, "pdf_data_raw.csv")
pdf_dataframe.to_csv(csv_file_path, index=False)
print(f"\nDataFrame saved to CSV file at: {csv_file_path}")
