import numpy as np
import pytest
import yaml

from src.exception.base import HeartStrokeException
from src.utils.main_utils import (load_numpy_array_data, load_object,
                                  read_yaml_file, save_numpy_array_data,
                                  save_object, write_yaml_file)

#-----------------------------------------
# testing: write_yaml_file, read_yaml_file
#-----------------------------------------

def test_write_yml_file_creates_yaml_successfully(tmp_path):
    """
    Test whether the YAML file is created successfully
    and content is written correctly.
    """
    file_path = tmp_path / "config.yml"

    test_content = {
        "model": "RandomForest",
        "accuracy": 0.95
    }

    write_yaml_file(str(file_path), test_content)

    assert file_path.exists()

    with open(file_path, "r") as file:
        loaded_content = yaml.safe_load(file)

    assert loaded_content == test_content

def test_write_yaml_file_replaces_existing_file(tmp_path):
    """
    Test whether existing YAML file is replaced
    when replace=True is passed.
    """
    file_path = tmp_path / "config.yaml"

    old_content = {"version": 1}
    new_content = {"version": 2}

    write_yaml_file(str(file_path), old_content)

    write_yaml_file(str(file_path), new_content, replace=True)

    loaded_content = read_yaml_file(str(file_path))

    assert loaded_content == new_content

def test_write_yaml_file_creates_nested_directories(tmp_path):
    """
    Test whether nested directories are created automatically.
    """
    file_path = tmp_path / "configs" / "training" / "config.yaml"

    test_content = {"epochs": 100}

    write_yaml_file(str(file_path), test_content)

    assert file_path.exists()

def test_write_yaml_file_rasies_heartstroke_exception():
    """
    Test whether HeartStrokeException is raised
    for invalid file paths.
    """
    invalid_path = None

    with pytest.raises(HeartStrokeException):
        write_yaml_file(invalid_path, {"test": 1})

def test_read_yaml_file_returns_dictionary(tmp_path):
    file_path = tmp_path / "config.yaml"

    test_content = {
        "batch_size": 32,
        "epochs": 100
    }

    with open(file_path, "w") as file:
        yaml.safe_dump(test_content, file)

    result = read_yaml_file(str(file_path))

    assert result == test_content

#----------------------------------
# testing: save_object, load_object
#----------------------------------

def test_save_object_creates_serialized_file(tmp_path):
    """
    Test whether save_object successfully creates
    a serialized object file.
    """
    file_path = tmp_path / "artifacts" / "model.pkl"

    test_object = {
        "model_name": "RandomForest",
        "accuracy": 0.95
    }

    save_object(str(file_path), test_object)

    assert file_path.exists()

def test_load_object_returns_correct_object(tmp_path):
    """
    Test whether load_object correctly loads
    the serialized Python object.
    """
    file_path = tmp_path / "model.pkl"

    test_object = {
        "feature_count": 11,
        "target_column": "stroke"
    }

    save_object(str(file_path), test_object)

    loaded_object = load_object(str(file_path))

    assert loaded_object == test_object

def test_save_and_load_object_integration(tmp_path):
    """
    Test end-to-end serialization and deserialization
    workflow using save_object and load_object.
    """
    file_path = tmp_path / "pipeline.pkl"

    test_object = [1, 2, 3, {"model": "XGBoost"}]

    save_object(str(file_path), test_object)

    loaded_object = load_object(str(file_path))

    assert loaded_object == test_object

def test_load_object_raises_heartstroke_exception_for_invalid_path():
    """
    Test whether load_object raises HeartStrokeException
    for invalid file paths.
    """
    invalid_path = "invalid/path/model.pkl"

    with pytest.raises(HeartStrokeException):
        load_object(invalid_path)


def test_save_object_raises_heartstroke_exception_for_invalid_path():
    """
    Test whether save_object raises HeartStrokeException
    for invalid file paths.
    """
    invalid_path = None

    with pytest.raises(HeartStrokeException):
        save_object(invalid_path, {"test": 1})

#------------------------------------------------------
# testing: save_numpy_array_data, load_numpy_array_data
#------------------------------------------------------

def test_save_numpy_array_creates_file(tmp_path):
    """
    Test whether NumPy array file is created successfully.
    """
    file_path = tmp_path / "arrays" / "train.npy"

    test_array = np.array([1, 2, 3, 4, 5])

    save_numpy_array_data(str(file_path), test_array)

    assert file_path.exists()


def test_load_numpy_array_returns_correct_array(tmp_path):
    """
    Test whether load_numpy_array_data correctly
    loads the saved NumPy array.
    """
    file_path = tmp_path / "test.npy"

    test_array = np.array([[1, 2], [3, 4]])

    save_numpy_array_data(str(file_path), test_array)

    loaded_array = load_numpy_array_data(str(file_path))

    assert np.array_equal(loaded_array, test_array)


def test_save_and_load_numpy_array_integration(tmp_path):
    """
    Test end-to-end NumPy array serialization
    and deserialization workflow.
    """
    file_path = tmp_path / "pipeline" / "features.npy"

    test_array = np.random.rand(10, 5)

    save_numpy_array_data(str(file_path), test_array)

    loaded_array = load_numpy_array_data(str(file_path))

    assert np.array_equal(loaded_array, test_array)


def test_load_numpy_array_raises_heartstroke_exception():
    """
    Test whether load_numpy_array_data raises
    HeartStrokeException for invalid file paths.
    """
    invalid_path = "invalid/path/array.npy"

    with pytest.raises(HeartStrokeException):
        load_numpy_array_data(invalid_path)


def test_save_numpy_array_raises_heartstroke_exception():
    """
    Test whether save_numpy_array_data raises
    HeartStrokeException for invalid file paths.
    """
    invalid_path = None

    test_array = np.array([1, 2, 3])

    with pytest.raises(HeartStrokeException):
        save_numpy_array_data(invalid_path, test_array)
