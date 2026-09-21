

from scripts.kaggle_cicd.inject_github_metadata import (
    create_env_cell, github_metadata, inject_environment_cell,
    inject_github_metadata, load_notebook, save_notebook)

###############################################################################
# load_notebook() / save_notebook()
###############################################################################


def test_save_and_load_notebook(tmp_path):
    notebook = {
        "cells": [],
        "metadata": {},
    }

    path = tmp_path / "notebook.ipynb"

    save_notebook(notebook, path)

    loaded = load_notebook(path)

    assert loaded == notebook


###############################################################################
# github_metadata()
###############################################################################


def test_github_metadata(monkeypatch):
    monkeypatch.setenv("GITHUB_REPOSITORY", "rahul/test")
    monkeypatch.setenv("GITHUB_WORKFLOW", "CI")
    monkeypatch.setenv("GITHUB_SHA", "abcdef")
    monkeypatch.setenv("GITHUB_REF_NAME", "main")
    monkeypatch.setenv("GITHUB_RUN_ID", "123")
    monkeypatch.setenv("GITHUB_RUN_NUMBER", "45")
    monkeypatch.setenv("GITHUB_ACTOR", "rahul")
    monkeypatch.setenv("GITHUB_EVENT_NAME", "push")

    metadata = github_metadata()

    assert metadata == {
        "repository": "rahul/test",
        "workflow": "CI",
        "sha": "abcdef",
        "branch": "main",
        "run_id": "123",
        "run_number": "45",
        "actor": "rahul",
        "event": "push",
    }


def test_github_metadata_defaults(monkeypatch):
    variables = [
        "GITHUB_REPOSITORY",
        "GITHUB_WORKFLOW",
        "GITHUB_SHA",
        "GITHUB_REF_NAME",
        "GITHUB_RUN_ID",
        "GITHUB_RUN_NUMBER",
        "GITHUB_ACTOR",
        "GITHUB_EVENT_NAME",
    ]

    for var in variables:
        monkeypatch.delenv(var, raising=False)

    metadata = github_metadata()

    assert metadata == {
        "repository": "",
        "workflow": "",
        "sha": "",
        "branch": "",
        "run_id": "",
        "run_number": "",
        "actor": "",
        "event": "",
    }


###############################################################################
# create_env_cell()
###############################################################################


def test_create_env_cell(monkeypatch):
    monkeypatch.setenv("DAGSHUB_USERNAME", "user")
    monkeypatch.setenv("DAGSHUB_TOKEN", "token")
    monkeypatch.setenv("KAGGLE_USERNAME", "rahul")
    monkeypatch.setenv("KAGGLE_DATASET_NAME", "dataset")

    cell = create_env_cell()

    assert cell["cell_type"] == "code"
    assert cell["execution_count"] is None
    assert cell["outputs"] == []

    source = "".join(cell["source"])

    assert 'os.environ["DAGSHUB_USERNAME"] = "user"' in source
    assert 'os.environ["DAGSHUB_TOKEN"] = "token"' in source
    assert 'os.environ["KAGGLE_USER"] = "rahul"' in source
    assert 'os.environ["KAGGLE_DATASET_NAME"] = "dataset"' in source

    assert cell["metadata"]["jupyter"]["source_hidden"] is True


###############################################################################
# inject_github_metadata()
###############################################################################


def test_inject_github_metadata(monkeypatch):
    monkeypatch.setenv("GITHUB_SHA", "abcdef")

    notebook = {
        "cells": [],
        "metadata": {},
    }

    inject_github_metadata(notebook)

    assert "github" in notebook["metadata"]
    assert notebook["metadata"]["github"]["sha"] == "abcdef"


def test_inject_github_metadata_creates_metadata(monkeypatch):
    monkeypatch.setenv("GITHUB_SHA", "abcdef")

    notebook = {
        "cells": [],
    }

    inject_github_metadata(notebook)

    assert "metadata" in notebook
    assert "github" in notebook["metadata"]


###############################################################################
# inject_environment_cell()
###############################################################################


def test_inject_environment_cell():
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": ["Hello"],
            }
        ]
    }

    inject_environment_cell(notebook)

    assert len(notebook["cells"]) == 2
    assert notebook["cells"][0]["cell_type"] == "code"
    assert notebook["cells"][1]["cell_type"] == "markdown"


def test_inject_environment_cell_creates_cells():
    notebook = {}

    inject_environment_cell(notebook)

    assert "cells" in notebook
    assert len(notebook["cells"]) == 1
    assert notebook["cells"][0]["cell_type"] == "code"
