import boto3
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="ap-south-1",
)

bucket_name = "langchainprojectsdocuments"

# Generate a presigned URL for the object
def generate_presigned_url(object_name, operation, expiration=3600):
    try:
        url = s3_client.generate_presigned_url(
            operation,
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
        return url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating URL: {str(e)}")

