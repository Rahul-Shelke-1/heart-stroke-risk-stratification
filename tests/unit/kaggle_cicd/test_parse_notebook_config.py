import subprocess

import pytest

from scripts.kaggle_cicd.parse_notebook_config import (CONFIG_PATTERN,
                                                       get_git_sha,
                                                       parse_value,
                                                       read_config, set_output)

###############################################################################
# parse_value()
###############################################################################

@pytest.mark.parametrize(
    "raw, expected",
    [
        ("True", True),
        ("False", False),
        ("true", True),
        ("false", False),
        ("123", 123),
        ("3.14", 3.14),
        ('"hello"', "hello"),
        ("['a', 'b']", ["a", "b"]),
        ("{'x': 1}", {"x": 1}),
        ("plain_text", "plain_text"),
    ],
)
def test_parse_value(raw, expected):
    assert parse_value(raw) == expected
###############################################################################
# CONFIG_PATTERN
###############################################################################

def test_config_pattern_matches():
    line = "# KAGGLE_CONFIG: enable_gpu = true"

    match = CONFIG_PATTERN.match(line)

    assert match is not None
    assert match.group(1) == "enable_gpu"
    assert match.group(2) == "true"

###############################################################################
# read_config()
###############################################################################

def test_read_config(valid_notebook):

    config = read_config(valid_notebook)

    assert config["execute"] is True
    assert config["slug"] == "my-demo-slug"
    assert config["language"] == "python"
    assert config["kernel_type"] == "notebook"
    assert config["is_private"] is True
    assert config["enable_gpu"] is False
    assert config["enable_tpu"] is False
    assert config["enable_internet"] is True
    assert config["machine_shape"] == ""
    assert config["dataset_sources"] == ["rahulshelke98/datasource"]
    assert config["competition_sources"] == []
    assert config["kernel_sources"] == []
    assert config["model_sources"] == []
    assert config["keywords"] == ["tag1", "tag2", "tag-tag3"]

def test_read_config_empty(empty_notebook):

    config = read_config(empty_notebook)

    assert config == {}

###############################################################################
# set_output()
###############################################################################

def test_set_output(tmp_path, monkeypatch):
    output = tmp_path / "github_output.txt"

    monkeypatch.setenv("GITHUB_OUTPUT", str(output))

    set_output("enable_gpu", True)
    set_output("language", "python")

    text = output.read_text()

    assert 'enable_gpu=true' in text
    assert 'language="python"' in text

###############################################################################
# get_git_sha()
###############################################################################

def test_get_git_sha_from_env(monkeypatch):

    monkeypatch.setenv("GITHUB_SHA", "abcdef123456789")

    assert get_git_sha() == "abcdef123456789"

def test_get_git_sha_from_git(monkeypatch):

    monkeypatch.delenv("GITHUN_SHA", raising=False)

    monkeypatch.setattr(
        subprocess,
        "check_output",
        lambda *args, **kwargs: "123456789abcdef\n"
    )

    assert get_git_sha() == "123456789abcdef"

def test_get_git_sha_git_failure(monkeypatch):

    monkeypatch.delenv("GITHUB_SHA", raising=False)

    def raise_error(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "git")

    monkeypatch.setattr(
        subprocess,
        "check_output",
        raise_error,
    )

    assert get_git_sha() == "unknown"
