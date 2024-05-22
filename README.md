# API Amber-Rekognition

## Objetivo 

- Usar la información de la página de Alerta Amber en México y la tecnología de Amazon Rekognition para identificar fotos de menores de edad publicadas en  redes sociales que carecen de una Alerta Amber.

## Introducción

La desaparición de menores en México constituye una problemática en crecimiento, impactando profundamente a miles de familias en todo el país. Desde la implementación del Registro Nacional de Personas Desaparecidas y No Localizadas en 2012, se han reportado más de 93,000 menores desaparecidos, de los cuales, a mayo de 2023, uno de cada cinco no ha sido aún localizado. En respuesta a esta crisis, el Programa Nacional Alerta AMBER, también iniciado en 2012, ha sido esencial para la localización rápida de menores en situación de riesgo. La difusión de estas alertas a través de redes sociales juega un papel crucial al proporcionar un amplio alcance y movilización comunitaria instantánea, aunque mantener la actualización y precisión de estas publicaciones representa un reto significativo para las autoridades y entidades involucradas.

![Desapariciones de Menores en Chiapas](info2.jpg)

## Datos

- Los datos utilizados en este proyecto son scrapeados de [Alerta Amber México](https://alertaamber.fgr.org.mx/)
- Para las pruebas en test:
    - Para la prueba positiva, se buscó una paersona con Alerta Amber pero actualmente mayor de edad, y se descargaron dos fotos suyas de redes sociales.
    - Para las pruebas negaivas, se usaron nuestras fotos.

## Pasos

### Proceso de registro
- `extract_read_pdf.py`: Scrapea los pdf's de la página web de Alertas Amber
    + Como hay alertas con 3 y 4 dígitos, scrapea primero los de 3 dígitos y luego los de 4.
    + Descarga uno por uno los pdf y revisa si tienen contenido o si son números con un reporte vacío, si son números con un reporte vacío los borra.
    + Una vez que ha descargado todos los pdf's con información, los lee y coloca el texto de un pdf en una celda de un dataframe. 
    + Finalmente guarda el dataframe con los textos de los reportes en la carpeta de `data` con el nombre `pdf_data_raw.csv`.
- `transform_dataframe.py`: Acomoda los textos en columnas para que sea fácil accesar a la información de los reportes, filtra los reportes pertenecientes a Chiapas y los guarda como `chiapas.csv` en la carpeta de `data`, y  como `amber.json` en la carpeta de `facial-recognition-app/src`
- `extract_load_images.py`: Descarga las imágenes de la página wed de Alertas Amber de los reportes de Chiapas y los sube a S3.
    + Primero lee el archivo en la carpeta de `data` llamado `chiapas.csv`
    + Luego con la información de éste archivo descarga las imágenes de menores desaparecidos con Alerta Amber en Chiapas
    + Finalmente sube estas imágenes a S3.
- `lamda_amber_registration.py`: Esta Lambda se activa cada que se suben imágenes al bucket `itam-proyecto-saraluz`, y obtiene una "huella digital" de la cara y le asigna un id, en este caso el número de reporte de Alerta Amber, esta información se guarda en DynamoBD.
### Proceso de Identificación
- Colocar `npm start` en terminal estando dentro de la carpeta `facial-recognition-app`
- Se abrirá la aplicación `http://localhost:3000`
- Seleccionar una imagen para revisar de acuerdo con las instrucciones.
- Esta imágen se sube a S3 al bucket `itam-proyecto-saraluz-test` y la api en Gateway llama a la `lambda_amber_authentication.py`, la cual identifica o no a la persona, si logra identificar a la persona se desplegarán los datos de la alerta amber.

## Estructura del repositorio

.\
├── aws_screanshots: capturas de pantalla del proceso para crear los buckets, lambdas, api.\
├── data: imágenes, csvs y pdf\
├── extract_load_images.py\
├── extract_read_pdf.py\
├── facial-recognition-app\
├── lambda_amber_authentication.py\
├── lambda_amber_registration.py\
├── LICENSE\
├── logs\
├── node_modules\
├── notebooks\
├── README.md\
├── referencias\
├── report\
├── requirements\
├── src\
└── transform_dataframe.py\

## Arquitectura de la solución
 
La arquitectura de este proyecto se encuentra en el siguiente diagrama:

![Data Model](data_model.png)

Diccionario de datos para `chiapas.csv`

- `id_file`: string. "A" ó "B" seguido de un guión bajo, seguido del número de reporte a 4 dígitos si es A y 3 si es B.  
- `image_file`: string. "image_" seguido del número de reporte.
- `reporte`: string. "AAMX" seguido del número de reporte.
- `fecha_act`: string. Fecha de activación.
- `nombre`: string. Nombre del menos de edad desaparecido.
- `fecha_nac`: string. Fecha de nacimiento.
- `edad`: string. Edad de desaparecido.
- `genero`: string. Masculino o Femenino.
- `fecha_hechos`: string. Fecha de los hechos.
- `lugar`: string. Estado
- `nacionalidad`: string. Nacionalidad
- `tipo_cabello`: string. Tipo de Cabello.
- `color_cabello`: string. Color del cabello.
- `color_ojos`: string. Color de ojos.
- `estatura`: string. Estatura.
- `peso`: string. Peso.
- `senas_part`: string. Señas particulares del desaparecido.
- `acompanante`: string. Acompañante.
- `acompanante_sp`: string. Señas particulares del acompañante.
- `sospechoso`: string. Nombre del sospechoso.
- `sospechoso_sp`: string. Señas particulares del sospechoso.
- `resumen_hechos`: string. Resumen de los hechos.

## Tecnologías usadas

- `Amazon Rekognition`: Se utilizó para crear la huella digital de los rostros de los desaparecidos.

- `Amazon S3`: Se usa para almacenar las imágenes de las Alertas Amber en Chiapas y de las imágenes para revisión.

- `Amazon DynamoDB`: Se usa para almacenar la huella digital y id de las imágenes.

- `Amazon Gateway`: Crea la api que conecta la lambda de identificación.

- `Amazon Lambda`: se usa para registrar a las imágenes de los desaparecidos, y para comparar las imágenes que se desea revisar.

- `Python`: se utiliza para scrapear y obtener la información de la página de Alertas Amber.

## Escenario de Producción

- Asumimos que la información se scrapeará de manera semanal, y se puede correr los archivos en el órden mencionado en la sección de Pasos.

- Para correr los archivos en python se puede crear un ambiente en `conda` con la información en el archivo `environment.yml` en la carpeta de `requirements`

- Para correr los scripts de python se requiere:
    + python=3.11
    + pandas
    + numpy
    + pytest
    + ipython
    + jupyterlab
    + matplotlib
    + plotly
    + ipyleaflet
    + pylint
    + autopep8
    + lxml
    + boto3
    + awswrangler
    + PyPDF2
    + json
    + requests

- Para correr la api se requiere:
    + "@testing-library/jest-dom": "^5.17.0"
    + "@testing-library/react": "^13.4.0"
    + "@testing-library/user-event": "^13.5.0"
    + "axios": "^1.6.8"
    + "dotenv": "^16.4.5"
    + "react": "^18.3.1"
    + "react-dom": "^18.3.1"
    + "react-scripts": "5.0.1"
    + "web-vitals": "^2.1.4"

## Pylint y Flake8

![pylint](aws_screenshots/pylint.png)
![flake8](aws_screenshots/flake8.png)

## Working backwards
https://docs.google.com/document/d/1iUAD5lQKMfh_aG3wlN3bzLpjRmP-iITJtGmMrn_kBBs/edit?usp=sharing

## Presentación
https://docs.google.com/presentation/d/1sboQzMv_p1cDkurnLl7EnGX2L56W2bM19JhrGj4lsiE/edit?usp=sharing
