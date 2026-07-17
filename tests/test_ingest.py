import pytest

from src.etl.ingest import ingest_data


def test_ingest_copies_file(tmp_path):
    source = tmp_path / "source.csv"
    destination = tmp_path / "destination.csv"

    source.write_text("id,name\n1,Ali")

    ingest_data(source, destination)

    assert destination.exists()


def test_ingest_preserves_content(tmp_path):
    source = tmp_path / "source.csv"
    destination = tmp_path / "destination.csv"

    source.write_text("id,name\n1,Ali")

    ingest_data(source, destination)

    assert source.read_text() == destination.read_text()


def test_ingest_missing_source(tmp_path):
    destination = tmp_path / "destination.csv"

    with pytest.raises(FileNotFoundError):
        ingest_data("does_not_exist.csv", destination)