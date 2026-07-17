import pytest


@pytest.fixture
def sample_user():
    return {
        "id": "1",
        "name": "Ali",
        "age": "25",
    }


@pytest.fixture
def sample_users():
    return [
        {
            "id": "1",
            "name": "Ali",
            "age": "25",
        },
        {
            "id": "2",
            "name": "Sara",
            "age": "30",
        },
        {
            "id": "3",
            "name": "Reza",
            "age": "28",
        },
    ]