# API Amber-Rekognition

## Objetivo 

- Usar la información de la página de Alerta Amber en México y la tecnología de Amazon Rekognition para identificar fotos de menores de edad publicadas en  redes sociales que carecen de una Alerta Amber.

## Datos

- Los datos utilizados en este proyecto son scrapeados de [Alerta Amber México](https://alertaamber.fgr.org.mx/)
- Para las pruebas en test:
    - Para la prueba positiva, se buscó una paersona con Alerta Amber pero actualmente mayor de edad, y se descargaron dos fotos suyas de redes sociales.
    - Para las pruebas negaivas, se usaron nuestras fotos.

## Pasos

- `S01_etl.ipynb`: Extract, transform and load Yelp datasets.
    + Here `json` files are read and converted to parquet files. Data is partitioned by metropolitan_area and year to optimize Spark performance.
    + Data quality checks are perfomed and data is cleaned. Text variables are converted to lower case, json lists are unnested in yelp_academic_dataset_business. Date and time variables are extracted from timestamp.
    + Business metropolitan areas a created using KMeans algorithm, and a catalog is created
    + Cleaned datasets are stored in output for further analysis.
- `S02_eda.ipynb`: A brief exploratory analysis is conducted on the partitioned parquets and cleaned data to learn more about the data, aggregations and quality issues.
- `S03_data_model.ipynb`: The data model is implemented the dimensions and a restaurant fact table is created.
    + Create number of business checkins table
    + Create number of business tips table
    + Create number of business reviews table
    + Create business union table: Here the fact table is built for all business.
    + Create a Restaurants Catalog: A catalog for all restaurant business is created, labelling observations manually.
    + Create restaurants table. The final fact table is stored in a dataset in the following address `data/output/restaurants.csv`. 
- `S04_analytics.Rmd`: This is the analytics code where the top 10 most reviewed restaurants for each metropolitan is generated. The final report can be consulted in `S04_analytics.html`

## Estructura del repositorio

`config`: Configuration files for data and aws services.
`data`: The inputs, preprocessing and outputs are stored here.
    `input`: Here is where the original `json` files are stored for further preprocessing.
    `preprocessing`: Intermediate tables such as catalogs are stored here.
    `output`: Cleaned data are stored here as parquet files.

## Modelo de datos
 
The data model for this project is explained in the following diagram.

![Data Model](figs/data_model.png)

Data dictionary for `restaurants.csv`

- `categories`: character. Restaurants category.
- `cluster`: double. Id metropolitan area.
- `metropolitan_area`: character. Name of metropolitan area.
- `business_id`: character. Business id.
- `name`: character. Name of business.
- `latitude`: double. Latitude.
- `longitude`: double. Longitude.
- `review_count`: double. Number of reviews that the restaurant has.
- `stars`: double. Average stars that the restaurant has.
- `year`: double. Year of the data.
- `num_checkins`: double. Number of checkins for the given year.
- `num_tips`: double. Number of tips that the users have written given the year.
- `num_reviews`: double. Number of user reviews in the dataset for this business in the given year.
- `mean_stars_reviews`: double. Number of mean stars for the user reviews.
- `is_restrautrant`: logical. Is this business a restaurant.


## Tecnologías usadas

- `Spark`: Spark was used in the local environment, as the data is not big enough to demand a cluster. However, data is big enough that file partitioning optimizations had to be performed, to increase the performance of the ETL.

- `Python`: Python was used to perform the ETLs and to connect to Spark. This pipeline was implemented in Python so it could be run in a AWS EMR cluster as well.

- `R`: An R Markdown was used to analyze the data and produce the maps in leaflet.

## Escenario de Producción

- Assuming that Yelp data can be extracted periodically, this pipeline can be executed in AWS services using a EMR cluster with Spark.

- Data should be stored in the data lake in S3, using the code `S00_stage_data.ipynb`.

- The ETL in `S01_etl.ipynb` already has the code to launch the EMR cluster, and in `config` the configuration files to setup the credentials and variables for the infrastructure will be stored.

- Based on the objective of this analysis, the pipeline could be scheduled to run with Airflow every start of a new month.

## Pylint y Flake8

![pylint](aws_screanshots/pylint.png)
![flake8](aws_screanshots/flake8.png)


--------------------------------------------------------------------------------





# ProyectoFinalAP
Este repositorio tiene por objetivo resguardar todo los archivos y modelo de identificación de imagenes para la materia de Arquitectura de Producto

# les dejo acá los links para que las puedan editar más facil
working backwards
https://docs.google.com/document/d/1iUAD5lQKMfh_aG3wlN3bzLpjRmP-iITJtGmMrn_kBBs/edit?usp=sharing

presentación
no alcance a hacerla, mañana la termino
https://docs.google.com/presentation/d/1sboQzMv_p1cDkurnLl7EnGX2L56W2bM19JhrGj4lsiE/edit?usp=sharing


aca viene más información para el working backwards y la presentación, pero tenemos que sacar gráficas de las bases que tienen ahí
https://derechosinfancia.org.mx/v1/grupo-de-trabajo/


#