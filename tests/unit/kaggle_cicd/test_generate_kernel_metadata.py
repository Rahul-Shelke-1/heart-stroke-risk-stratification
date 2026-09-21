import json

import pytest

from scripts.kaggle_cicd.generate_kernel_metadata import (build_metadata,
                                                          get_bool, get_list,
                                                          write_metadata)

###############################################################################
# get_bool()
###############################################################################

@pytest.mark.parametrize(
    "value,expected",
    [
        ("true", True),
        ("True", True),
        ("TRUE", True),
        ("false", False),
        ("False", False),
        ("", False),
    ],
)
def test_get_bool(monkeypatch, value, expected):
    monkeypatch.setenv("TEST_BOOL", value)
    assert get_bool("TEST_BOOL") is expected


def test_get_bool_missing(monkeypatch):
    monkeypatch.delenv("TEST_BOOL", raising=False)
    assert get_bool("TEST_BOOL") is False


###############################################################################
# get_list()
###############################################################################

@pytest.mark.parametrize(
    "value,expected",
    [
        ('[]', []),
        ('["a"]', ["a"]),
        ('["a","b"]', ["a", "b"]),
        ("", []),
    ],
)
def test_get_list(monkeypatch, value, expected):
    monkeypatch.setenv("TEST_LIST", value)
    assert get_list("TEST_LIST") == expected


def test_get_list_missing(monkeypatch):
    monkeypatch.delenv("TEST_LIST", raising=False)
    assert get_list("TEST_LIST") == []


def test_get_list_invalid_json(monkeypatch):
    monkeypatch.setenv("TEST_LIST", "not-json")

    with pytest.raises(json.JSONDecodeError):
        get_list("TEST_LIST")


###############################################################################
# build_metadata()
###############################################################################

def populate_env(monkeypatch):
    monkeypatch.setenv("NOTEBOOK", "notebooks/demo.ipynb")
    monkeypatch.setenv("SLUG", "rahul/demo")
    monkeypatch.setenv("TITLE", "Demo Notebook")
    monkeypatch.setenv("LANGUAGE", "python")
    monkeypatch.setenv("KERNEL_TYPE", "notebook")
    monkeypatch.setenv("IS_PRIVATE", "true")

    monkeypatch.setenv("ENABLE_GPU", "true")
    monkeypatch.setenv("ENABLE_TPU", "false")
    monkeypatch.setenv("ENABLE_INTERNET", "true")
    monkeypatch.setenv("MACHINE_SHAPE", "standard")

    monkeypatch.setenv("DATASET_SOURCES", '["ds1"]')
    monkeypatch.setenv("COMPETITION_SOURCES", '["comp1"]')
    monkeypatch.setenv("KERNEL_SOURCES", '["kernel1"]')
    monkeypatch.setenv("MODEL_SOURCES", '["model1"]')
    monkeypatch.setenv("KEYWORDS", '["ml","kaggle"]')


def test_build_metadata(monkeypatch):
    populate_env(monkeypatch)

    metadata = build_metadata()

    assert metadata["id"] == "rahul/demo"
    # assert metadata["title"] == "Demo Notebook"
    assert metadata["code_file"] == "demo.ipynb"
    assert metadata["language"] == "python"
    assert metadata["kernel_type"] == "notebook"

    assert metadata["is_private"] is True
    assert metadata["enable_gpu"] is True
    assert metadata["enable_tpu"] is False
    assert metadata["enable_internet"] is True

    assert metadata["dataset_sources"] == ["ds1"]
    assert metadata["competition_sources"] == ["comp1"]
    assert metadata["kernel_sources"] == ["kernel1"]
    assert metadata["model_sources"] == ["model1"]

    assert metadata["keywords"] == ["ml", "kaggle"]


###############################################################################
# write_metadata()
###############################################################################

def test_write_metadata(tmp_path, monkeypatch):

    notebook_dir = tmp_path / "notebooks"
    notebook_dir.mkdir()

    notebook = notebook_dir / "demo.ipynb"
    notebook.write_text("{}")

    monkeypatch.setenv("NOTEBOOK", str(notebook))

    metadata = {
        "id": "rahul/demo",
        # "title": "Demo Notebook",
    }

    output = write_metadata(metadata)

    assert output.exists()
    assert output.name == "kernel-metadata.json"

    loaded = json.loads(output.read_text())

    assert loaded == metadata


###############################################################################
# Integration
###############################################################################

def test_build_and_write_metadata(tmp_path, monkeypatch):

    notebook_dir = tmp_path / "notebooks"
    notebook_dir.mkdir()

    notebook = notebook_dir / "demo.ipynb"
    notebook.write_text("{}")

    monkeypatch.setenv("NOTEBOOK", str(notebook))
    monkeypatch.setenv("SLUG", "rahul/demo")
    monkeypatch.setenv("TITLE", "Demo")
    monkeypatch.setenv("LANGUAGE", "python")
    monkeypatch.setenv("KERNEL_TYPE", "notebook")
    monkeypatch.setenv("IS_PRIVATE", "false")

    monkeypatch.setenv("ENABLE_GPU", "false")
    monkeypatch.setenv("ENABLE_TPU", "false")
    monkeypatch.setenv("ENABLE_INTERNET", "true")
    monkeypatch.setenv("MACHINE_SHAPE", "standard")

    monkeypatch.setenv("DATASET_SOURCES", "[]")
    monkeypatch.setenv("COMPETITION_SOURCES", "[]")
    monkeypatch.setenv("KERNEL_SOURCES", "[]")
    monkeypatch.setenv("MODEL_SOURCES", "[]")
    monkeypatch.setenv("KEYWORDS", '["ci"]')

    metadata = build_metadata()

    output = write_metadata(metadata)

    generated = json.loads(output.read_text())

    assert generated["id"] == "rahul/demo"
    assert generated["code_file"] == "demo.ipynb"
    assert generated["enable_internet"] is True
    assert generated["keywords"] == ["ci"]
