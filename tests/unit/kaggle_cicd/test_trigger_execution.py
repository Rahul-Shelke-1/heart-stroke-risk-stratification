from unittest.mock import MagicMock, patch

import pytest

from scripts.kaggle_cicd.trigger_execution import (get_env, main,
                                                   trigger_execution)


def test_get_env_returns_value(monkeypatch):
    monkeypatch.setenv("SLUG", "heart-stroke")

    assert get_env("SLUG") == "heart-stroke"

def test_get_env_missing():
    with pytest.raises(RuntimeError):
        get_env("DOES_NOT_EXIST")

@patch("scripts.kaggle_cicd.trigger_execution.KaggleApi")
def test_trigger_execution_success(mock_api_cls):
    api = MagicMock()
    mock_api_cls.return_value = api

    trigger_execution("rahul", "heart-stroke")

    api.authenticate.assert_called_once()
    api.kernels_push_cli.assert_called_once_with(
        folder=".",
        metadata=None,
    )

@patch("scripts.kaggle_cicd.trigger_execution.KaggleApi")
def test_trigger_execution_auth_failure(mock_api_cls):
    api = MagicMock()
    api.authenticate.side_effect = RuntimeError("Bad credentials")

    mock_api_cls.return_value = api

    with pytest.raises(RuntimeError):
        trigger_execution("rahul", "heart-stroke")

@patch("scripts.kaggle_cicd.trigger_execution.KaggleApi")
def test_trigger_execution_push_failure(mock_api_cls):
    api = MagicMock()
    api.kernels_push_cli.side_effect = RuntimeError("Upload failed")

    mock_api_cls.return_value = api

    with pytest.raises(RuntimeError):
        trigger_execution("rahul", "heart-stroke")

@patch("scripts.kaggle_cicd.trigger_execution.trigger_execution")
def test_main_success(mock_trigger, monkeypatch):
    monkeypatch.setenv("KAGGLE_USERNAME", "rahul")
    monkeypatch.setenv("SLUG", "heart-stroke")

    assert main() == 0

    mock_trigger.assert_called_once_with(
        "rahul",
        "heart-stroke",
    )

@patch("scripts.kaggle_cicd.trigger_execution.trigger_execution")
def test_main_failure(mock_trigger, monkeypatch):
    monkeypatch.setenv("KAGGLE_USERNAME", "rahul")
    monkeypatch.setenv("SLUG", "heart-stroke")

    mock_trigger.side_effect = RuntimeError("boom")

    assert main() == 1
