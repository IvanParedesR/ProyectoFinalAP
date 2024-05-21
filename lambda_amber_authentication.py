"""
Este script define una función AWS Lambda para identificar posibles
coincidencias entre una imagen proporcionada y las caras en la colección
"amber-alerts" de Rekognition. Si se encuentra una coincidencia, recupera
los detalles de una tabla de DynamoDB y devuelve el informe correspondiente.
"""
import json
import boto3

s3 = boto3.client("s3")
rekognition = boto3.client("rekognition", region_name="us-east-1")
DYNAMODBTABLENAME = "amber-alerts"
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
amberTable = dynamodb.Table(DYNAMODBTABLENAME)
BUCKETNAME = "itam-proyecto-saraluz-test"
# Cambiar nombre de bucket cuando se cree el de producción


def lambda_handler(event, context):
    """
    Función manejadora de AWS Lambda para procesar imagenes y buscar
    coincidencia de rostros en Rekognition y verificar si existe en DynamoDB.
    """
    print(event)
    object_key = event["queryStringParameters"]["object_key"]
    image_bytes = s3.get_object(Bucket=BUCKETNAME,
                                Key=object_key)["Body"].read()
    response = rekognition.search_faces_by_image(
        CollectionId="amber-alerts", Image={"Bytes": image_bytes}
    )

    print(response["FaceMatches"])

    for match in response["FaceMatches"]:
        print("gol")
        print(match)

        face = amberTable.get_item(Key={"rekognitionId":
                                        match["Face"]["FaceId"]})
        if "Item" in face:
            print("Coincide con una persona en Alerta Amber", face["Item"])
            return build_response(
                200,
                {
                    "Message": "Coincide con una persona en Alerta Amber",
                    "reporte": face["Item"]["reporte"],
                },
            )
    print("No coincide con una persona en Alerta Amber")
    return build_response(
        403, {"Message": "No coincide con una persona en Alerta Amber"}
    )


def build_response(status_code, body=None):
    """
    Construye un diccionario de respuesta para la función Lambda.
    Args:
    status_code (int): El código de estado HTTP para la respuesta.
    body (dict, optional): El cuerpo de la respuesta, si lo hay.
    Returns:
    dict: El diccionario de respuesta que contiene el código de estado.
    """
    response = {
        "status_code": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
    if body is not None:
        response["body"] = json.dumps(body)
    return response
