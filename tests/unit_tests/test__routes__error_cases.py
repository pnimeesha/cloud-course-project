from fastapi import status
from fastapi.testclient import TestClient

from tests.consts import TEST_BUCKET_NAME
from tests.utils import delete_s3_bucket


def test_get_nonexistant_file(client: TestClient):
    """Test that a 404 error is returned when trying to get a non-existent file."""
    response = client.get("/v1/files/non_existent_file.txt")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "File not found"}


def test_head_nonexistant_file(client: TestClient):
    """Test that a 404 error is returned when trying to get metadata for a non-existent file."""
    response = client.head("/v1/files/non_existent_file.txt")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistant_file(client: TestClient):
    """Test that a 404 error is returned when trying to delete a non-existent file."""
    response = client.delete("/v1/files/non_existent_file.txt")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "File not found"}


def test_get_files_invalid_page_size(client: TestClient):
    """Test that a 400 error is returned when an invalid page size is provided."""
    response = client.get("/v1/files?page_size=-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.get("/v1/files?page_size={DEFAULT_GET_FILES_MAX_PAGE_SIZE + 1}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_files_page_token_is_mutually_exclusive_with_page_size_and_directory(client: TestClient):
    """Test that a 422 error is returned when page token is set with page size and directory."""
    response = client.get("/v1/files?page_token=some_token&page_size=10")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "mutually exclusive" in str(response.json())

    response = client.get("/v1/files?page_token=some_token&directory=some_directory")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "mutually exclusive" in str(response.json())

    response = client.get("/v1/files?page_token=some_token&directory=some_directory&page_size=10")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "mutually exclusive" in str(response.json())


def test_unforseen_error(client: TestClient):
    """Test that a 500 error is returned when an unseen error occurs."""
    # delete the s3 bucket and all objects inside
    delete_s3_bucket(TEST_BUCKET_NAME)

    # make requests to the API to route that interacts with the s3 bucket
    response = client.get("/v1/files")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Internal Server Error"}
