import pytest
from unittest.mock import MagicMock, patch

from src.common.config import Config
from src.etl.upload import upload_to_s3


@patch("src.etl.upload.boto3.client")
def test_upload_called(mock_client):
    mock_s3 = MagicMock()
    mock_client.return_value = mock_s3

    upload_to_s3("data/users_cleaned.csv", Config.S3_BUCKET)

    mock_s3.upload_file.assert_called_once()


@patch("src.etl.upload.boto3.client")
def test_upload_bucket_name(mock_client):
    mock_s3 = MagicMock()
    mock_client.return_value = mock_s3

    upload_to_s3("data/users_cleaned.csv", "my_bucket")

    args = mock_s3.upload_file.call_args[0]

    assert args[1] == "my_bucket"


@patch("src.etl.upload.boto3.client")
def test_upload_file_name(mock_client):
    mock_s3 = MagicMock()
    mock_client.return_value = mock_s3

    upload_to_s3("abc.csv", "bucket")

    args = mock_s3.upload_file.call_args[0]

    assert args[0] == "abc.csv"


@patch("src.etl.upload.boto3.client")
def test_s3_client_created(mock_client):
    """The upload should create an S3 client."""

    upload_to_s3("file.csv", "bucket")

    mock_client.assert_called_once_with("s3")


@patch("src.etl.upload.boto3.client")
def test_upload_s3_key(mock_client):
    """The uploaded object should be placed under the processed prefix."""

    mock_s3 = MagicMock()
    mock_client.return_value = mock_s3

    upload_to_s3("data/users_cleaned.csv", "bucket")

    s3_key = mock_s3.upload_file.call_args[0][2]

    assert s3_key.startswith("processed/year=")
    assert "/month=" in s3_key
    assert s3_key.endswith("users_cleaned.csv")


@patch("src.etl.upload.boto3.client")
def test_upload_failure(mock_client):
    """
    If boto3 raises an exception, the upload function should
    propagate it after logging.
    """

    mock_s3 = MagicMock()
    mock_s3.upload_file.side_effect = Exception("Upload failed")
    mock_client.return_value = mock_s3

    with pytest.raises(Exception, match="Upload failed"):
        upload_to_s3("file.csv", "bucket")


@patch("src.etl.upload.boto3.client")
def test_upload_logs_success(mock_client, caplog):
    """A successful upload should produce an informational log."""

    mock_client.return_value = MagicMock()

    with caplog.at_level("INFO"):
        upload_to_s3("file.csv", "bucket")

    assert "Uploaded file to s3://" in caplog.text


@patch("src.etl.upload.boto3.client")
def test_upload_logs_failure(mock_client, caplog):
    """A failed upload should be logged before the exception is re-raised."""

    mock_s3 = MagicMock()
    mock_s3.upload_file.side_effect = Exception("Boom")
    mock_client.return_value = mock_s3

    with caplog.at_level("ERROR"):
        with pytest.raises(Exception):
            upload_to_s3("file.csv", "bucket")

    assert "S3 upload failed" in caplog.text


@patch("src.etl.upload.boto3.client")
def test_nested_path_uses_filename_only(mock_client):
    """Only the file name should appear in the S3 object key."""

    mock_s3 = MagicMock()
    mock_client.return_value = mock_s3

    upload_to_s3("some/very/deep/path/users.csv", "bucket")

    s3_key = mock_s3.upload_file.call_args[0][2]

    assert s3_key.endswith("users.csv")