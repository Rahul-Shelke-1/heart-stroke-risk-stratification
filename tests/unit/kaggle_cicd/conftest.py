
import pytest


@pytest.fixture
def fixtures_dir(request):
    return request.config.rootpath / "tests" / "fixtures" / "kaggle_cicd"

@pytest.fixture
def valid_notebook(fixtures_dir):
    return fixtures_dir / "notebook_valid.ipynb"

@pytest.fixture
def invalid_notebook(fixtures_dir):
    return fixtures_dir / "notebook_invalid.ipynb"

@pytest.fixture
def empty_notebook(fixtures_dir):
    return fixtures_dir / "notebook_empty.ipynb"

@pytest.fixture
def valid_config():
    return {
        "execute": True,
        "slug": "heart-stroke",
        "title": "heart-stroke",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": False,
        "enable_tpu": False,
        "enable_internet": True,
        "machine_shape": "NvidiaTeslaT4",
        "dataset_sources": ["owner/dataset"],
        "competition_sources": [],
        "kernel_sources": [],
        "model_sources": [],
        "keywords": [],
    }
