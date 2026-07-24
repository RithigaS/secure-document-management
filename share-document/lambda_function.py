import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    # Logged-in user email
    claims = event["requestContext"]["authorizer"]["claims"]

    user_email = claims["email"]

    groups = claims.get("cognito:groups", [])

    if isinstance(groups, str):
        groups = [groups]


    # Get document ID from URL
    document_id = event["pathParameters"]["documentId"]


    # Get email to share from request body
    body = json.loads(event["body"])

    share_email = body["email"]


    # Get document
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


    # Only owner or Admin can share

    if "Admin" not in groups and document["owner"] != user_email:

        return {
            "statusCode": 403,
            "body": json.dumps({
                "message": "Only owner or Admin can share document"
            })
        }


    # Existing shared users
    shared_users = document.get("sharedWith", [])


    # Avoid duplicate sharing
    if share_email not in shared_users:

        shared_users.append(share_email)


    # Update DynamoDB

    table.update_item(
        Key={
            "documentId": document_id
        },
        UpdateExpression="SET sharedWith = :users",
        ExpressionAttributeValues={
            ":users": shared_users
        }
    )


    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Document shared successfully",
            "sharedWith": share_email
        })
    }