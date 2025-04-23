import boto3

try:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.type_defs import (
        PutObjectRequestTypeDef,
        ResponseMetadataTypeDef,
    )

except ImportError:
    print("boto3-stubs[s3] is not installed")

BUCKET_NAME = "cloud-course-bucket-nim"

session = boto3.Session()
s3_client: "S3Client" = session.client("s3")

# s3_client.get_paginator()
# write a file to s3 bucket with the contents "Hello, world!"
# response: PutObjectRequestTypeDef = s3_client.put_object(
#     Bucket=BUCKET_NAME, 
#     Key="folder/hello.txt", 
#     Body="Hello world!", 
#     ContentType="text/plain"
#     )
