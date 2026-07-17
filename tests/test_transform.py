import pytest
import csv

from src.etl.transform import (
    transform_user,
    transform_users,
    read_users,
    write_users,
    transform_file,
)


def test_transform_user_young(sample_user):
    result = transform_user(sample_user)

    assert result["age_group"] == "young"
    

def test_transform_user_adult():
    user = {
        "id": "2",
        "name": "Sara",
        "age": "30",
    }

    result = transform_user(user)

    assert result["age_group"] == "adult"


def test_transform_boundary_29():
    user = {
        "id": "1",
        "name": "Ali",
        "age": "29",
    }

    assert transform_user(user)["age_group"] == "young"


def test_transform_boundary_30():
    user = {
        "id": "1",
        "name": "Ali",
        "age": "30",
    }

    assert transform_user(user)["age_group"] == "adult"


def test_transform_boundary_31():
    user = {
        "id": "1",
        "name": "Ali",
        "age": "31",
    }

    assert transform_user(user)["age_group"] == "adult"


def test_transform_preserves_name(sample_user):
    result = transform_user(sample_user)

    assert result["name"] == sample_user["name"]


def test_transform_preserves_id(sample_user):
    result = transform_user(sample_user)

    assert result["id"] == sample_user["id"]


def test_transform_users_returns_three(sample_users):
    result = transform_users(sample_users)

    assert len(result) == 3


def test_transform_users_empty():
    assert transform_users([]) == []


def test_invalid_age():
    user = {
        "id": "1",
        "name": "Ali",
        "age": "abc",
    }

    with pytest.raises(ValueError):
        transform_user(user)


def test_read_users(tmp_path):
    """Verify that users are correctly read from a CSV file."""

    input_file = tmp_path / "users.csv"

    with open(input_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "age"])
        writer.writerow(["1", "Ali", "25"])
        writer.writerow(["2", "Sara", "30"])

    users = read_users(input_file)

    assert len(users) == 2
    assert users[0]["name"] == "Ali"
    assert users[1]["age"] == "30"


def test_read_users_missing_file():
    """Reading a missing file should raise FileNotFoundError."""

    with pytest.raises(FileNotFoundError):
        read_users("does_not_exist.csv")


def test_write_users(tmp_path, sample_users):
    """Verify transformed users are written to disk."""

    output_file = tmp_path / "users.csv"

    write_users(sample_users, output_file)

    assert output_file.exists()

    users = read_users(output_file)

    assert len(users) == 3


def test_write_users_empty(tmp_path):
    """
    Current behavior:
    An empty user list should simply return without creating a file.
    """

    output_file = tmp_path / "users.csv"

    write_users([], output_file)

    assert not output_file.exists()


def test_transform_file(tmp_path):
    """Verify the entire transformation pipeline."""

    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    with open(input_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "age"])
        writer.writerow(["1", "Ali", "25"])
        writer.writerow(["2", "Sara", "30"])

    transform_file(input_file, output_file)

    users = read_users(output_file)

    assert users[0]["age_group"] == "young"
    assert users[1]["age_group"] == "adult"


def test_transform_file_missing_input(tmp_path):
    """
    The pipeline should propagate the original exception
    after logging the failure.
    """

    output_file = tmp_path / "output.csv"

    with pytest.raises(FileNotFoundError):
        transform_file("missing.csv", output_file)


def test_transform_file_invalid_age(tmp_path):
    """
    Invalid ages should stop the pipeline instead of producing
    corrupted output.
    """

    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    with open(input_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "age"])
        writer.writerow(["1", "Ali", "abc"])

    with pytest.raises(ValueError):
        transform_file(input_file, output_file)


def test_transform_logs_success(tmp_path, caplog):
    """The pipeline should log a success message when it finishes."""

    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    with open(input_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "age"])
        writer.writerow(["1", "Ali", "25"])

    with caplog.at_level("INFO"):
        transform_file(input_file, output_file)

    assert "Data transformation completed successfully." in caplog.text


def test_transform_logs_failure(caplog):
    """Failures should be logged before the exception is re-raised."""

    with caplog.at_level("ERROR"):

        with pytest.raises(FileNotFoundError):
            transform_file("missing.csv", "output.csv")

    assert "Data transformation failed." in caplog.text