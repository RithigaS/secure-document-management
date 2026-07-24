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

    # Get logged-in user details from Cognito
    claims = event["requestContext"]["authorizer"]["claims"]

    user_email = claims["email"]

    groups = claims.get("cognito:groups", [])

    if isinstance(groups, str):
        groups = [groups]


    # Get document id from URL
    document_id = event["pathParameters"]["documentId"]


    # Get document details from DynamoDB
    response = table.get_item(
        Key={
            "documentId": document_id
        }
    )


    if "Item" not in response:

        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "Document not found"
            })
        }


    document = response["Item"]


    # Permission check
    # Admin can delete any document
    # Owner can delete own document
    # Shared users cannot delete

    if (
        "Admin" not in groups
        and document["owner"] != user_email
    ):

        return {
            "statusCode": 403,
            "body": json.dumps({
                "message": "Only owner or Admin can delete this document"
            })
        }


    # Delete file from S3
    s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=document["s3Key"]
    )


    # Delete metadata from DynamoDB
    table.delete_item(
        Key={
            "documentId": document_id
        }
    )


    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Document deleted successfully"
        })
    }