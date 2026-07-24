import json
import boto3
import os

s3 = boto3.client(
    "s3",
    region_name="eu-north-1"
)

BUCKET_NAME = os.environ["BUCKET_NAME"]

ALLOWED_EXTENSIONS = [
    ".pdf",
    ".doc",
    ".docx",
    ".txt"
]

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def lambda_handler(event, context):

    try:

        # Get logged-in user
        claims = event["requestContext"]["authorizer"]["claims"]

        # Owner email
        owner = claims["email"]

        # Get file name
        file_name = event["queryStringParameters"]["fileName"]

        # Validate file extension
        extension = os.path.splitext(file_name)[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "message": "Only PDF, DOC, DOCX and TXT files are allowed."
                })
            }

        # Store original filename
        s3_key = f"documents/{file_name}"

        # Generate Pre-signed POST
        response = s3.generate_presigned_post(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Fields={
                "success_action_status": "201",
                "x-amz-meta-owner": owner
            },
            Conditions=[
                ["content-length-range", 0, MAX_FILE_SIZE],
                {"x-amz-meta-owner": owner}
            ],
            ExpiresIn=300
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Upload URL generated successfully.",
                "fileName": file_name,
                "uploadUrl": response["url"],
                "fields": response["fields"]
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": str(e)
            })
        }