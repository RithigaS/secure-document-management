import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    claims = event["requestContext"]["authorizer"]["claims"]

    # Get logged-in user email
    user_email = claims["email"]

    # Get groups
    groups = claims.get("cognito:groups", [])

    if isinstance(groups, str):
        groups = [groups]


    # Admin can see all documents
    if "Admin" in groups:

        response = table.scan()


    # User can see only own documents
    else:

        response = table.scan(
            FilterExpression="#o = :owner",
            ExpressionAttributeNames={
                "#o": "owner"
            },
            ExpressionAttributeValues={
                ":owner": user_email
            }
        )


    documents = response.get("Items", [])


    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "documents": documents
        })
    }