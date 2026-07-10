import os.path
import sys

import cloudpickle
import numpy as np
import yaml

from src.exception.base import HeartStrokeException
from src.logger import logging


def read_yaml_file(file_path: str) -> dict:
    """
    read a YAML file and return its contents as a dictionary.

    Parameters
    ----------
    file_path : str
        Path to save YAML file.

    Returns
    -------
    dict
        Parsed content of the YAML file.

    Raises
    ------
    HeartStrokeException
        if there is any issue while reading or parsing the YAML file
        (e.g., file not found, invalid YAML format).
    """
    try:
        logging.info(f"Reading YAML file from: {file_path}")

        with open(file_path, "rb") as yaml_file:
            content = yaml.safe_load(yaml_file)

        logging.info("Successfully read YAML file")

        return content

    except Exception as e:
        logging.exception(f"Error occurred while reading YAML file: {file_path}")
        raise HeartStrokeException(e, sys) from e


def write_yaml_file(
        file_path: str,
        content: object,
        replace: bool = False
    ) -> None:
    """
    Write content to YAML file.

    Parameters
    ----------
    file_path : str
        Path where the YAML file will be written.

    content : object
        Python object to serialize and store in YAML format.

    replace : bool, optional
        Whether to replace the existing file if it already exists,
        by default False.

    Raises
    ------
    HeartStrokeException
        If there is any issue while creating directories,
        writing the YAML file, or serializing the content.
    """
    try:
        logging.info(f"Writing YAML file to: {file_path}")

        if replace:
            if os.path.exists(file_path):
                logging.info(f"Replacing existing YAML file: {file_path}")
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.safe_dump(content, file, default_flow_style=False)

        logging.info("Successfully wrote YAML file")

    except Exception as e:
        logging.exception(f"Error occured while writing YAML file: {file_path}")
        raise HeartStrokeException(e, sys) from e


def load_object(file_path: str) -> object:
    """
    Load a serialized Python object from a disk using cloudpickle.

    Parameters
    ----------
    file_path : str
        Path to the serialized object file.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    HeartStrokeException
        If there is any issue while loading the object such as
        file not found, corrupted file, or deserialization failure.
    """
    try:
        logging.info(f"Loading object from file: {file_path}")

        with open(file_path, "rb") as file_obj:
            obj = cloudpickle.load(file_obj)

        logging.info("Object loaded successfully")

        return obj

    except Exception as e:
        logging.exception(f"Error loading object from {file_path}")
        raise HeartStrokeException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.ndarray) -> None:
    """
    Save a NumPy array to disk.

    Parameters
    ----------
    file_path : str
        Path where the NumPy array file will be stored.

    array : np.ndarray
        NumPy array to serialize and save.

    Raises
    ------
    HeartStrokeException
        If there is any issue while creating directories,
        saving the NumPy array, or writing to disk.
    """
    try:
        logging.info(f"Saving NumPy array to file: {file_path}")

        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)

        logging.info("NumPy array saved successfully")

    except Exception as e:
        logging.exception(
            f"Error occurred while saving NumPy array to: {file_path}"
        )
        raise HeartStrokeException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.ndarray:
    """
    Load a NumPy array from disk.

    Parameters
    ----------
    file_path : str
        Path to the serialized NumPy array file.

    Returns
    -------
    np.ndarray
        Loaded NumPy array.

    Raises
    ------
    HeartStrokeException
        If there is any issue while loading the NumPy array
        such as file not found, corrupted file, or deserialization failure.
    """
    try:
        logging.info(f"Loading NumPy array from file: {file_path}")

        with open(file_path, "rb") as file_obj:
            array = np.load(file_obj)

        logging.info("NumPy array loaded successfully")

        return array

    except Exception as e:
        logging.exception(
            f"Error occurred while loading NumPy array from: {file_path}"
        )
        raise HeartStrokeException(e, sys) from e

def save_object(file_path: str, obj: object) -> None:
    """
    Serialize and save a Python object to disk using cloudpickle.

    Parameters
    ----------
    file_path : str
        Path where the serialized object will be stored.

    obj : object
        Python object to serialize and save.

    Raises
    ------
    HeartStrokeException
        If there is any issue while creating directories,
        serializing the object, or writing to disk.
    """
    try:
        logging.info(f"Saving object to file: {file_path}")

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file_obj:
            cloudpickle.dump(obj, file_obj)

        logging.info("Object saved successfully")

    except Exception as e:
        logging.exception(f"Error occurred while saving object to: {file_path}")
        raise HeartStrokeException(e, sys) from e
