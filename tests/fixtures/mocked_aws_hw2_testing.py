import boto3
from moto import mock_aws
from pytest import fixture

from tests.consts import TEST_BUCKET_NAME
from tests.unit_tests.s3.test__write_objects import point_away_from_aws


@fixture
def mocked_aws():
    
    with mock_aws():
        # Set the environment variables to point away from AWS
        point_away_from_aws()
        
        # 1. Create an S3 bucket
        s3_client = boto3.client("s3")
        s3_client.create_bucket(Bucket=TEST_BUCKET_NAME)
        
        yield 
        
        #  4. Clean up/Teardown by deleting the bucket
        response = s3_client.list_objects_v2(Bucket=TEST_BUCKET_NAME)
        for obj in response["Contents"]:
            s3_client.delete_object(Bucket=TEST_BUCKET_NAME, Key=obj["Key"])
        s3_client.delete_bucket(Bucket=TEST_BUCKET_NAME)