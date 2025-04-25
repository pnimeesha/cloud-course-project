from fastapi import status
from fastapi.testclient import TestClient

# from src.files_api.main import app

TEST_FILE_PATH = "some/nested/file2.txt"
TEST_FILE_CONTENT = b"test content2"
TEST_FILE_CONTENT_TYPE = "text/plain"


def test_upload_file(client: TestClient):
    response = client.put(
        f"/v1/files/{TEST_FILE_PATH}",
        files={"file": (TEST_FILE_PATH, TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "file_path": TEST_FILE_PATH,
        "message": f"New file uploaded at path : /{TEST_FILE_PATH}",
    }

    # update an existing file
    updated_content = b"updated content"
    response = client.put(
        f"/v1/files/{TEST_FILE_PATH}",
        files={"file": (TEST_FILE_PATH, updated_content, TEST_FILE_CONTENT_TYPE)},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "file_path": TEST_FILE_PATH,
        "message": f"Existing file updated at path: /{TEST_FILE_PATH}",
    }


# update an existing file


def test_list_files_with_pagination(client: TestClient):
    # Upload multiple files to test pagination
    for i in range(0, 15):
        file_path = f"test_file_{i}.txt"
        response1 = client.put(
            f"/v1/files/{file_path}",
            files={"file": (file_path, TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)},
        )
        assert response1.status_code == status.HTTP_201_CREATED

    # Test listing files with pagination
    response = client.get("/v1/files?page_size=10")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["files"]) == 10
    assert "next_page_token" in response.json()


def test_get_file_metadata(client: TestClient):
    # Upload a file to test metadata retrieval
    file_path = "test_file_metadata.txt"
    response1 = client.put(
        f"/v1/files/{file_path}",
        files={"file": (file_path, TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)},
    )
    assert response1.status_code == status.HTTP_201_CREATED

    # Test getting file metadata
    response2 = client.head(f"/v1/files/{file_path}")
    assert response2.status_code == status.HTTP_200_OK
    assert response2.headers["Content-Type"] == TEST_FILE_CONTENT_TYPE
    assert int(response2.headers["Content-Length"]) == len(TEST_FILE_CONTENT)


def test_get_file(client: TestClient):
    # Upload a file to test retrieval
    file_path = "test_file_retrieval.txt"
    response1 = client.put(
        f"/v1/files/{file_path}",
        files={"file": (file_path, TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)},
    )
    assert response1.status_code == status.HTTP_201_CREATED

    # Test getting the file
    response2 = client.get(f"/v1/files/{file_path}")
    assert response2.status_code == status.HTTP_200_OK
    assert response2.content == TEST_FILE_CONTENT
    assert TEST_FILE_CONTENT_TYPE in response2.headers["Content-Type"]


def test_delete_file(client: TestClient):
    # upload a file
    response = client.put(
        "/v1/files/dummy_file.txt",
        files={"file": ("dummy_file.txt", b"to be deleted", TEST_FILE_CONTENT_TYPE)},
    )
    assert response.status_code == status.HTTP_201_CREATED

    # delete the file
    response = client.delete(("files/dummy_file.txt"))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/v1/files/dummy_file.txt")
    assert response.status_code == status.HTTP_404_NOT_FOUND
