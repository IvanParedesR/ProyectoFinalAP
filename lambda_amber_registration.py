"""
Este script de Lambda se utiliza para indexar imágenes de
alertas Amber en Amazon Rekognition y registrarlas en una
tabla DynamoDB.
"""
import boto3

s3 = boto3.client("s3")
rekognition = boto3.client("rekognition", region_name="us-east-1")
DYNAMODBTABLENAME = "amber-alerts"
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
amberTable = dynamodb.Table(DYNAMODBTABLENAME)


def lambda_handler(event, context):
    """
    Extrae información del evento, indexa la cara en la imagen
    utilizando Amazon Rekognition, y registra la alerta
    Amber en DynamoDB.
    """
    print("Received event:", event)

    # Obtener el bucket y object key del evento en S3
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    try:
        # Indexar la cara en la imagen utilizando Amazon Rekognition
        response = index_amber_image(bucket, key)
        print("Indexing response:", response)

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            # Extraer el FaceId y el reporte de la clave de la imagen
            image_name = key.split("/")[-1]  # Obtener la última parte de llave
            imagenid = image_name.split("_")  # Separar por guión bajo
            if len(imagenid) >= 2:
                reporte = imagenid[1].split(".")[0]  # Extraer reporte de llave
            else:
                raise ValueError(f"Unable to extract reporte from key: {key}")

            # Obtener el FaceId de la respuesta
            if "FaceRecords" in response and len(response["FaceRecords"]) > 0:
                face_id = response["FaceRecords"][0]["Face"]["FaceId"]
            else:
                raise ValueError(f"No se detectan rostros en la imagen: {key}")

            # Registrar la alerta Amber en DynamoDB
            register_amber(face_id, reporte)

        return response
    except Exception as e:
        print("Error:", e)
        print("Error processing object {} from bucket {}. ".
              format(key, bucket))
        raise e


def index_amber_image(bucket, key):
    """
    Indexa la cara en la imagen utilizando Amazon Rekognition.
    :param bucket: Nombre del bucket de S3.
    :param key: Clave del objeto de la imagen en S3.
    :return: Respuesta de la indexación de Rekognition.
    """
    response = rekognition.index_faces(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        CollectionId="amber-alerts",
    )
    return response


def register_amber(face_id, reporte):
    """
    Registra la alerta Amber en DynamoDB.
    :param face_id: ID de la cara detectada.
    :param reporte: Reporte asociado a la alerta Amber.
    """
    amberTable.put_item(
        Item={
            "rekognitionId": face_id,
            "reporte": reporte,
        }
    )
