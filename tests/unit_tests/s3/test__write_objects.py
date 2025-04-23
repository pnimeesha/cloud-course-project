import os
from urllib import response

import boto3
from more_itertools import bucket
from moto import mock_aws

from files_api.s3.write_objects import upload_s3_object
from tests.consts import TEST_BUCKET_NAME

# TEST_BUCKET_NAME = "test-bucket-mlops-club-nim"

# export AWS_ACCESS_KEY_ID='testing'
# export AWS_SECRET_ACCESS_KEY='testing'
# export AWS_SECURITY_TOKEN='testing'
# export AWS_SESSION_TOKEN='testing'
# export AWS_DEFAULT_REGION='us-east-1'


def point_away_from_aws():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"  


@mock_aws
def test__upload_s3_object(mocked_aws):

    # upload a file to the bucket, with a particular content type
    object_key = "test.txt"
    file_content: bytes = b"Hello, world!"
    content_type = "text/plain"
    upload_s3_object(
        bucket_name = TEST_BUCKET_NAME,
        object_key = object_key,
        file_content = file_content,
        content_type = content_type,
        # s3_client = s3_client,
    )
    
    # check that the file was uploaded with the correct content type
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=TEST_BUCKET_NAME, Key=object_key)
    assert response["ContentType"] == content_type
    assert response["Body"].read() == file_content
    
    print("cleared up the mock_aws")

