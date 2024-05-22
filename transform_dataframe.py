''' Este script transforma los datos scrapeados de los PDFs de
la página de Alerta Amber y los guarda en un archivo CSV'''
import os
import pandas as pd
from src.utils import get_logger

# Configurar logging
logger = get_logger("TransformDataFrame")
logger.info("Comenzando limpieza ...")

# Path to the CSV file
CSV_FILE_PATH = "./data/pdf_data_raw.csv"
DATA_DIRECTORY = "./data"

# Read the CSV file into a DataFrame
pdf_dataframe = pd.read_csv(CSV_FILE_PATH)

# Separar datos en columnas
pdf_dataframe[["A", "B"]] = (
    pdf_dataframe["Text"].str.split(": ", n=1, expand=True)
)
pdf_dataframe[["reporte", "B"]] = (
    pdf_dataframe["B"].str.split("\n", n=1, expand=True)
)
pdf_dataframe[["A", "B"]] = (
    pdf_dataframe["B"].str.split(":", n=1, expand=True)
)
pdf_dataframe[["fecha_act", "B"]] = (
    pdf_dataframe["B"].str.split("\n", n=1, expand=True)
)
pdf_dataframe[["nombre", "B"]] = pdf_dataframe["B"].str.split(
    "FECHA DE NACIMIENTO:", n=1, expand=True
)
pdf_dataframe[["fecha_nac", "B"]] = pdf_dataframe["B"].str.split(
    "EDAD:", n=1, expand=True
)
pdf_dataframe[["edad", "B"]] = (
    pdf_dataframe["B"].str.split("GÉNERO:", n=1, expand=True)
)
pdf_dataframe[["genero", "B"]] = (
    pdf_dataframe["B"].str.split("FECHA", n=1, expand=True)
)
pdf_dataframe[["A", "B"]] = (
    pdf_dataframe["B"].str.split(":", n=1, expand=True)
)
pdf_dataframe[["fecha_hechos", "B"]] = pdf_dataframe["B"].str.split(
    "LUGAR", n=1, expand=True
)
pdf_dataframe[["A", "B"]] = pdf_dataframe["B"].str.split(":", n=1, expand=True)
pdf_dataframe[["lugar", "B"]] = pdf_dataframe["B"].str.split(
    "NACIONALIDAD:", n=1, expand=True
)
pdf_dataframe[["nacionalidad", "B"]] = pdf_dataframe["B"].str.split(
    "CABELLO:", n=1, expand=True
)
pdf_dataframe[["tipo_cabello", "B"]] = pdf_dataframe["B"].str.split(
    "COLOR:", n=1, expand=True
)
pdf_dataframe[["color_cabello", "B"]] = pdf_dataframe["B"].str.split(
    "COLOR", n=1, expand=True
)
pdf_dataframe[["A", "B"]] = (
    pdf_dataframe["B"].str.split("OJOS:", n=1, expand=True)
)
pdf_dataframe[["color_ojos", "B"]] = pdf_dataframe["B"].str.split(
    "ESTATURA:", n=1, expand=True
)
pdf_dataframe[["estatura", "B"]] = pdf_dataframe["B"].str.split(
    "PESO:", n=1, expand=True
)
pdf_dataframe[["peso", "B"]] = (
    pdf_dataframe["B"].str.split("SEÑAS", n=1, expand=True)
)
pdf_dataframe[["A", "B"]] = pdf_dataframe["B"].str.split(
    "PARTICULARES:", n=1, expand=True
)
pdf_dataframe[["senas_part", "B"]] = pdf_dataframe["B"].str.split(
    "RESUMEN", n=1, expand=True
)
pdf_dataframe[["A", "B"]] = (
    pdf_dataframe["B"].str.split("HECHOS:", n=1, expand=True)
)
pdf_dataframe[["resumen_hechos", "B"]] = pdf_dataframe["B"].str.split(
    "RESUMEN", n=1, expand=True
)
pdf_dataframe[["senas_part", "B"]] = pdf_dataframe["senas_part"].str.split(
    "Acompañante", n=1, expand=True
)
pdf_dataframe[["A", "acompanante"]] = pdf_dataframe["B"].str.split(
    "NOMBRE:", n=1, expand=True
)
pdf_dataframe[["acompanante", "B"]] = pdf_dataframe["acompanante"].str.split(
    "SEÑAS", n=1, expand=True
)
pdf_dataframe[["A", "acompanante_sp"]] = pdf_dataframe["B"].str.split(
    "PARTICULARES:", n=1, expand=True
)
pdf_dataframe[["senas_part", "B"]] = pdf_dataframe["senas_part"].str.split(
    "Sospechoso", n=1, expand=True
)
pdf_dataframe[["A", "sospechoso"]] = pdf_dataframe["B"].str.split(
    "NOMBRE:", n=1, expand=True
)
pdf_dataframe[["sospechoso", "B"]] = pdf_dataframe["sospechoso"].str.split(
    "SEÑAS", n=1, expand=True
)
pdf_dataframe[["A", "sospechoso_sp"]] = pdf_dataframe["B"].str.split(
    "PARTICULARES:", n=1, expand=True
)
pdf_dataframe[["A", "num"]] = (
    pdf_dataframe["id_file"].str.split("_", n=1, expand=True)
)
pdf_dataframe["image_file"] = "image_" + pdf_dataframe["num"] + ".jpg"

# Quitar '\n'
# Columns to process
columns_to_process = [
    "nombre",
    "edad",
    "fecha_nac",
    "genero",
    "fecha_hechos",
    "lugar",
    "nacionalidad",
    "tipo_cabello",
    "color_cabello",
    "color_ojos",
    "estatura",
    "peso",
    "senas_part",
    "acompanante",
    "acompanante_sp",
    "sospechoso",
    "sospechoso_sp",
    "resumen_hechos",
]

# Iterate over columns and replace '\n'
for column in columns_to_process:
    pdf_dataframe[column] = (
        pdf_dataframe[column].str.replace(r"\n", " ", regex=True)
    )

pdf_dataframe = (
    pdf_dataframe.map(lambda x: x.strip() if isinstance(x, str) else x)
)

# Renombrar y quitar duplicados
df1 = pdf_dataframe[
    [
        "id_file",
        "image_file",
        "reporte",
        "fecha_act",
        "nombre",
        "fecha_nac",
        "edad",
        "genero",
        "fecha_hechos",
        "lugar",
        "nacionalidad",
        "tipo_cabello",
        "color_cabello",
        "color_ojos",
        "estatura",
        "peso",
        "senas_part",
        "acompanante",
        "acompanante_sp",
        "sospechoso",
        "sospechoso_sp",
        "resumen_hechos",
    ]
]

df1 = df1.drop_duplicates(subset=["reporte"], keep="first")

# Revisar y filtrar qué imágenes queremos antes de descargar
chiapas = df1[df1["lugar"] == "CHIAPAS"]
prueba_positiva = df1[df1["reporte"] == "AAMX398"]

chiapas = pd.concat([chiapas, prueba_positiva], ignore_index=True)
len(chiapas)

csv_file_path = os.path.join(DATA_DIRECTORY, "chiapas.csv")
chiapas.to_csv(csv_file_path, index=False)
logger.info(f"\nDataFrame saved to CSV file at: {CSV_FILE_PATH}")

result = chiapas.reset_index().to_json(
    r"./facial-recognition-app/src/amber.json",
    orient="table",
    force_ascii=False
)
