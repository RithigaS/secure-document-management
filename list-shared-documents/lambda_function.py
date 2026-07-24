import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")

s3 = boto3.client(
    "s3",
    region_name="eu-north-1"
)

TABLE_NAME = os.environ["TABLE_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    claims = event["requestContext"]["authorizer"]["claims"]

    user_email = claims["email"]

    response = table.scan()

    documents = response.get("Items", [])

    shared_by_me = []
    shared_with_me = []

    for document in documents:

        download_url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": document["s3Key"]
            },
            ExpiresIn=300
        )

        document["downloadUrl"] = download_url

        if document["owner"] == user_email and len(document.get("sharedWith", [])) > 0:
            shared_by_me.append(document)

        if user_email in document.get("sharedWith", []):
            shared_with_me.append(document)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "sharedByMe": shared_by_me,
            "sharedWithMe": shared_with_me
        })
    }