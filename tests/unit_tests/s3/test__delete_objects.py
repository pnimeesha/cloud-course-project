"""Test cases for `s3.delete_objects`."""

import boto3

from files_api.s3.delete_objects import delete_s3_object
from files_api.s3.read_objects import object_exists_in_s3
from files_api.s3.write_objects import upload_s3_object
from tests.consts import TEST_BUCKET_NAME


def test_delete_existing_s3_object(mocked_aws: None):
    s3_client = boto3.client("s3")
    # Upload an object to the S3 bucket
    object_key = "testfile.txt"
    file_content: bytes = b"Hello, world!"
    content_type = "text/plain"
    upload_s3_object(
        bucket_name=TEST_BUCKET_NAME,
        object_key=object_key,
        file_content=file_content,
        content_type=content_type,
    )

    # Check that the object exists before deletion
    assert object_exists_in_s3(TEST_BUCKET_NAME, object_key) is True

    # Delete the object
    delete_s3_object(TEST_BUCKET_NAME, object_key)

    # Check that the object no longer exists after deletion
    assert object_exists_in_s3(TEST_BUCKET_NAME, object_key) is False


def test_delete_nonexistent_s3_object(mocked_aws: None):
    object = "doesnotexists.txt"
    # Attempt to delete a non-existent object
    delete_s3_object(TEST_BUCKET_NAME, object)
    # Check that the object does not exist before deletion
    assert object_exists_in_s3(TEST_BUCKET_NAME, object) is False
