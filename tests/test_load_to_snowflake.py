import pytest
from unittest.mock import MagicMock, patch

from src.common.config import Config
from src.warehouse.load_to_snowflake import load_users
from src.warehouse.load_to_snowflake import read_csv


@patch("src.warehouse.load_to_snowflake.connect_to_snowflake")
@patch("src.warehouse.load_to_snowflake.read_csv")
def test_connect_called(mock_read, mock_connect):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    mock_read.return_value = []

    load_users(
        Config.CLEANED_FILE,
        Config.SNOWFLAKE_TABLE,
    )

    mock_connect.assert_called_once()


@patch("src.warehouse.load_to_snowflake.connect_to_snowflake")
@patch("src.warehouse.load_to_snowflake.read_csv")
def test_commit_called(mock_read, mock_connect):

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = MagicMock()

    mock_connect.return_value = mock_conn

    mock_read.return_value = []

    load_users(
        Config.CLEANED_FILE,
        Config.SNOWFLAKE_TABLE,
    )

    mock_conn.commit.assert_called_once()


@patch("src.warehouse.load_to_snowflake.connect_to_snowflake")
@patch("src.warehouse.load_to_snowflake.read_csv")
def test_connection_closed(mock_read, mock_connect):

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = MagicMock()

    mock_connect.return_value = mock_conn

    mock_read.return_value = []

    load_users(
        Config.CLEANED_FILE,
        Config.SNOWFLAKE_TABLE,
    )

    mock_conn.close.assert_called_once()


@patch("src.warehouse.load_to_snowflake.connect_to_snowflake")
@patch("src.warehouse.load_to_snowflake.read_csv")
def test_cursor_closed(mock_read, mock_connect):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    mock_read.return_value = []

    load_users(
        Config.CLEANED_FILE,
        Config.SNOWFLAKE_TABLE,
    )

    mock_cursor.close.assert_called_once()


@patch("src.warehouse.load_to_snowflake.connect_to_snowflake")
@patch("src.warehouse.load_to_snowflake.read_csv")
def test_cursor_created(mock_read, mock_connect):
    """A cursor should be created from the Snowflake connection."""

    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_read.return_value = []

    load_users("users.csv", "USERS")

    mock_conn.cursor.assert_called_once()


@patch("src.warehouse.load_to_snowflake.connect_to_snowflake")
@patch("src.warehouse.load_to_snowflake.read_csv")
def test_insert_called(mock_read, mock_connect):
    """Each user should generate one INSERT statement."""

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    mock_read.return_value = [
        {
            "id": "1",
            "name": "Ali",
            "age": "25",
            "age_group": "young",
        }
    ]

    load_users("users.csv", "USERS")

    mock_cursor.execute.assert_called_once()


@patch("src.warehouse.load_to_snowflake.connect_to_snowflake")
@patch("src.warehouse.load_to_snowflake.read_csv")
def test_insert_parameters(mock_read, mock_connect):
    """The INSERT statement should receive converted values."""

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    mock_read.return_value = [
        {
            "id": "5",
            "name": "Sara",
            "age": "30",
            "age_group": "adult",
        }
    ]

    load_users("users.csv", "USERS")

    params = mock_cursor.execute.call_args[0][1]

    assert params == (5, "Sara", 30, "adult")


@patch("src.warehouse.load_to_snowflake.connect_to_snowflake")
def test_connection_failure(mock_connect):
    """Connection errors should be re-raised."""

    mock_connect.side_effect = Exception("Connection failed")

    with pytest.raises(Exception, match="Connection failed"):
        load_users("users.csv", "USERS")


@patch("src.warehouse.load_to_snowflake.connect_to_snowflake")
@patch("src.warehouse.load_to_snowflake.read_csv")
def test_execute_failure(mock_read, mock_connect):
    """Database errors during INSERT should be re-raised."""

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.execute.side_effect = Exception("Insert failed")

    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    mock_read.return_value = [
        {
            "id": "1",
            "name": "Ali",
            "age": "20",
            "age_group": "young",
        }
    ]

    with pytest.raises(Exception, match="Insert failed"):
        load_users("users.csv", "USERS")


@patch("src.warehouse.load_to_snowflake.connect_to_snowflake")
@patch("src.warehouse.load_to_snowflake.read_csv")
def test_success_logging(mock_read, mock_connect, caplog):
    """Successful loads should be logged."""

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = MagicMock()

    mock_connect.return_value = mock_conn
    mock_read.return_value = []

    with caplog.at_level("INFO"):
        load_users("users.csv", "USERS")

    assert "Loaded 0 users into Snowflake." in caplog.text


@patch("src.warehouse.load_to_snowflake.connect_to_snowflake")
def test_failure_logging(mock_connect, caplog):
    """Failures should be logged before raising."""

    mock_connect.side_effect = Exception("Boom")

    with caplog.at_level("ERROR"):
        with pytest.raises(Exception):
            load_users("users.csv", "USERS")

    assert "Snowflake load failed" in caplog.text


def test_read_csv(tmp_path):
    """CSV rows should be returned as dictionaries."""

    csv_file = tmp_path / "users.csv"

    csv_file.write_text(
        "id,name,age,age_group\n"
        "1,Ali,25,young\n",
        encoding="utf-8",
    )

    rows = read_csv(csv_file)

    assert rows == [
        {
            "id": "1",
            "name": "Ali",
            "age": "25",
            "age_group": "young",
        }
    ]