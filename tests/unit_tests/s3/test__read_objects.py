"""Test cases for `s3.read_objects`."""

import boto3

from files_api import s3
from files_api.s3.read_objects import (
    fetch_s3_objects_metadata,
    fetch_s3_objects_using_page_token,
    object_exists_in_s3,
)
from tests.consts import TEST_BUCKET_NAME


# pylint: disable=unused-argument
def test_object_exists_in_s3(mocked_aws: None):
    s3_client = boto3.client("s3")
    s3_client.put_object(
        Bucket=TEST_BUCKET_NAME,
        Key="testfile.txt",
        Body=b"test content!",
    )
    assert object_exists_in_s3(TEST_BUCKET_NAME, "testfile.txt") is True
    assert object_exists_in_s3(TEST_BUCKET_NAME, "nonexistent.txt") is False

# pylint: disable=unused-argument
def test_pagination(mocked_aws: None):
    s3_client = boto3.client("s3")
    # Create multiple objects in the bucket
    for i in range(1, 6):
        s3_client.put_object(
            Bucket=TEST_BUCKET_NAME,
            Key=f"testfile_{i}.txt",
            Body=b"test content!",
        )
    
    # Paginate 2 objects at a time
    files, next_pageen_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME, max_keys=2)
    assert len(files) == 2
    assert files[0]["Key"] == "testfile_1.txt"
    assert files[1]["Key"] == "testfile_2.txt"
  
    # Fetch the next page using the continuation token
    files, next_pageen_token = fetch_s3_objects_using_page_token(TEST_BUCKET_NAME, continuation_token=next_pageen_token, max_keys=2    )
    assert len(files) == 2
    assert files[0]["Key"] == "testfile_3.txt"
    assert files[1]["Key"] == "testfile_4.txt"
    # Fetch the last page
    files, next_pageen_token = fetch_s3_objects_using_page_token(TEST_BUCKET_NAME, continuation_token=next_pageen_token, max_keys=2)
    assert len(files) == 1
    assert files[0]["Key"] == "testfile_5.txt"
    assert next_pageen_token is None

def test_mixed_page_sizes(mocked_aws: None): 
    s3_client = boto3.client("s3")
    for i  in [1, 2, 3, 4, 5]:
        s3_client.put_object(
            Bucket=TEST_BUCKET_NAME,
            Key=f"testfile_{i}.txt",
            Body=b"test content {i}!",
        )
        
    # paginate with mixed page sizes
    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME, max_keys=3)
    assert len(files) == 3
    assert files[0]["Key"] == "testfile_1.txt"
    assert files[1]["Key"] == "testfile_2.txt"
    assert files[2]["Key"] == "testfile_3.txt"
    
    files, next_page_token = fetch_s3_objects_using_page_token(TEST_BUCKET_NAME, continuation_token=next_page_token, max_keys=1)
    assert len(files) == 1
    assert files[0]["Key"] == "testfile_4.txt"
    
    files, next_page_token = fetch_s3_objects_using_page_token(TEST_BUCKET_NAME, continuation_token=next_page_token, max_keys=2)
    assert len(files) == 1
    assert files[0]["Key"] == "testfile_5.txt"
    assert next_page_token is None

def test_directory_queries(mocked_aws: None):
    
    s3_client = boto3.client("s3")
    # Create a directory structure in the bucket
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="dir1/testfile_1.txt", Body=b"test content 1!",)
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="dir1/testfile_2.txt", Body=b"test content 2!")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="dir2/testfile_3.txt", Body=b"test content 3!")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="dir2/subdir1/testfile_4.txt", Body=b"test content 4!")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="testfile_5.txt", Body=b"test content 5!")
    
    #Query with prefix
    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME, prefix="dir1/")
    assert len(files) == 2
    assert files[0]["Key"] == "dir1/testfile_1.txt"
    assert files[1]["Key"] == "dir1/testfile_2.txt"
    assert next_page_token is None
    
    # Query with prefix for nested directories
    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME, prefix="dir2/subdir1/")
    assert len(files) == 1
    assert files[0]["Key"] == "dir2/subdir1/testfile_4.txt"
    assert next_page_token is None
    
    # Query with prefix for no prefix
    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME)
    assert len(files) == 5
    # assert files[1]["Key"] == "dir1/testfile_1.txt"
    # assert files[2]["Key"] == "dir1/testfile_2.txt"
    # assert files[3]["Key"] == "dir2/testfile_3.txt"
    # assert files[4]["Key"] == "dir2/subdir1/testfile_4.txt"
    # assert files[0]["Key"] == "testfile_5.txt"
    actual_keys = {obj["Key"] for obj in files}
    expected_keys = {
        "dir1/testfile_1.txt",
        "dir1/testfile_2.txt",
        "dir2/testfile_3.txt",
        "dir2/subdir1/testfile_4.txt",
        "testfile_5.txt",
    }
    assert actual_keys == expected_keys

    assert next_page_token is None
    
