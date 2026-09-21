import pytest

from scripts.kaggle_cicd.validate_config import (ValidationError, validate,
                                                 validate_config,
                                                 validate_required_config,
                                                 validate_types)

##############################################################################
# validate_config()
################################################################################

def test_validate_config_accepts_valid(valid_config):
    validate_config(valid_config)

def test_validate_config_unknown_key(valid_config):
    valid_config["enable_gpp"] = True

    with pytest.raises(
        ValidationError,
        match="Did you mean 'enable_gpu'",
    ):
        validate_config(valid_config)

def test_validate_config_unknown_key_without_match(valid_config):
    valid_config["banana"] = True

    with pytest.raises(
        ValidationError,
        match="Unknown config key",
    ):
        validate_config(valid_config)

################################################################################
# validate_required_config()
################################################################################

def test_validate_required_success(valid_config):
    validate_required_config(valid_config)

def test_validate_required_missing(valid_config):
    del valid_config["slug"]

    with pytest.raises(
        ValidationError,
        match="slug",
    ):
        validate_required_config(valid_config)

################################################################################
# validate_types()
################################################################################

@pytest.mark.parametrize(
    "key,value",
    [
        ("execute", "True"),
        ("enable_gpu", "yes"),
        ("language", 123),
        ("dataset_sources", "owner/data"),
        ("keywords", "ml"),
    ],
)
def test_validate_types(key, value, valid_config):
    valid_config[key] = value

    with pytest.raises(ValidationError):
        validate_types(valid_config)

################################################################################
# validate_slug()
################################################################################

@pytest.mark.parametrize(
    "slug",
    [
        "HeartStroke",
        "heart stroke",
        "heart_stroke",
        "heart@stroke",
    ],
)
def test_validate_invalid_slug(slug, valid_config):
    valid_config["slug"] = slug

    with pytest.raises(ValidationError):
        validate(valid_config)

################################################################################
# validate_sources()
################################################################################

def test_validate_duplicate_sources(valid_config):
    valid_config["dataset_sources"] = [
        "owner/data",
        "owner/data",
    ]

    with pytest.raises(
        ValidationError,
        match="Duplicate",
    ):
        validate(valid_config)

@pytest.mark.parametrize(
    "source",
    [
        "owner",
        "owner/",
        "/dataset",
        "owner/data/extra",
        "owner data",
    ],
)
def test_validate_invalid_source(source, valid_config):
    valid_config["dataset_sources"] = [source]

    with pytest.raises(ValidationError):
        validate(valid_config)

################################################################################
# validate_machine()
################################################################################

def test_validate_machine_choice(valid_config):
    valid_config["machine_shape"] = "INVALID"

    with pytest.raises(
        ValidationError,
        match="machine_shape",
    ):
        validate(valid_config)
