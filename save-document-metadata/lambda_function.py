import json
import boto3
import os
import uuid
from datetime import datetime
from urllib.parse import unquote_plus

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

TABLE_NAME = os.environ["TABLE_NAME"]

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    for record in event["Records"]:

        bucket_name = record["s3"]["bucket"]["name"]

        s3_key = unquote_plus(record["s3"]["object"]["key"])

        file_name = os.path.basename(s3_key)

        # Read S3 object metadata
        response = s3.head_object(
            Bucket=bucket_name,
            Key=s3_key
        )

        owner = response["Metadata"]["owner"]

        document_id = str(uuid.uuid4())

        uploaded_at = datetime.utcnow().isoformat()

        table.put_item(
            Item={
                "documentId": document_id,
                "owner": owner,
                "fileName": file_name,
                "s3Key": s3_key,
                "uploadedAt": uploaded_at,
                "status": "UPLOADED",
                "sharedWith": []
            }
        )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Metadata saved successfully."
        })
    }