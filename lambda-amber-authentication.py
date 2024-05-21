import boto3
import json

s3 = boto3.client("s3")
rekognition = boto3.client("rekognition", region_name="us-east-1")
dynamoTableName = "amber-alerts"
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
amberTable = dynamodb.Table(dynamoTableName)
bucketName = "itam-proyecto-saraluz-test"


def lambda_handler(event, context):
    print(event)
    objectKey = event["queryStringParameters"]["objectKey"]
    image_bytes = s3.get_object(Bucket=bucketName, Key=objectKey)["Body"].read()
    response = rekognition.search_faces_by_image(
        CollectionId="amber-alerts", Image={"Bytes": image_bytes}
    )

    print(response["FaceMatches"])

    for match in response["FaceMatches"]:
        print("gol")
        print(match)

        face = amberTable.get_item(Key={"rekognitionId": match["Face"]["FaceId"]})
        if "Item" in face:
            print("Coincide con una persona en Alerta Amber", face["Item"])
            return buildResponse(
                200,
                {
                    "Message": "Coincide con una persona en Alerta Amber",
                    "reporte": face["Item"]["reporte"],
                },
            )
    print("No coincide con una persona en Alerta Amber")
    return buildResponse(
        403, {"Message": "No coincide con una persona en Alerta Amber"}
    )


def buildResponse(statusCode, body=None):
    response = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
    if body is not None:
        response["body"] = json.dumps(body)
    return response
