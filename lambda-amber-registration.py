import boto3

s3 = boto3.client("s3")
rekognition = boto3.client("rekognition", region_name="us-east-1")
dynamoTableName = "amber-alerts"
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
amberTable = dynamodb.Table(dynamoTableName)


def lambda_handler(event, context):
    print("Received event:", event)

    # Get the bucket and object key from the S3 event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    try:
        # Index the face in the image using Amazon Rekognition
        response = index_amber_image(bucket, key)
        print("Indexing response:", response)

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            # Extract the FaceId and reporte from the image key
            image_name = key.split("/")[-1]  # Get the last part of the key
            imagenid = image_name.split("_")  # Split by underscore
            if len(imagenid) >= 2:
                reporte = imagenid[1].split(".")[0]  # Extract reporte from key
            else:
                raise ValueError(f"Unable to extract reporte from key: {key}")

            # Get the FaceId from the response
            if "FaceRecords" in response and len(response["FaceRecords"]) > 0:
                faceId = response["FaceRecords"][0]["Face"]["FaceId"]
            else:
                raise ValueError(f"No face detected in image: {key}")

            # Register the amber alert in DynamoDB
            register_amber(faceId, reporte)

        return response
    except Exception as e:
        print("Error:", e)
        print("Error processing object {} from bucket {}. ".format(key, bucket))
        raise e


def index_amber_image(bucket, key):
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


def register_amber(faceId, reporte):
    amberTable.put_item(
        Item={
            "rekognitionId": faceId,
            "reporte": reporte,
        }
    )
