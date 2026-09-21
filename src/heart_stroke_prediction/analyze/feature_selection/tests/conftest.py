import os

import cloudpickle
import pandas as pd
import pytest
from notebooks.artifacts.pipeline_functions import create_interaction
from sklearn.model_selection import train_test_split

CAT_FEATURES = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
NUM_FEATURES = ['age', 'avg_glucose_level', 'bmi']
TARGET_COL = ['stroke']
ALREADY_PROCESSED = ['hypertension', 'heart_disease',]
ID_COL = ['id']

def get_data_path(path, levels=1):
    """Go up N directory levels"""
    # Start from current test file
    result = os.path.realpath(path)
    for _ in range(levels):
        result = os.path.dirname(result)
    return result

# ---------- data for test -----------
@pytest.fixture
def raw_dataframe() -> pd.DataFrame:
    """Fixture: returns a dummy data"""
    # current file path
    current_path = __file__
    # csv file name
    file_name = "healthcare-dataset-stroke-data.csv"
    # travers outside the current path by 6 folders
    file_path = get_data_path(current_path, 5)
    # naviget to data path
    data_path = os.path.join(file_path, "notebooks", "data", file_name)
    # read data
    df = pd.read_csv(data_path)
        # sample data
    train, test = train_test_split(df, test_size=0.195, stratify=df['stroke'])
    # return data
    return test

@pytest.fixture
def get_raw_dataframe() -> pd.DataFrame:
    """Fixture: returns a dummy data"""
    # current file path
    current_path = __file__
    # csv file name
    file_name = "heart_stroke_data.csv"
    # travers outside the current path by 6 folders
    file_path = get_data_path(current_path, 5)
    # naviget to data path
    data_path = os.path.join(file_path, "notebooks", "data", file_name)
    # read data
    df = pd.read_csv(data_path)
    # sample data
    train, test = train_test_split(df, test_size=0.195, stratify=df['stroke'])
    # return data
    return test

@pytest.fixture
def get_handled_missing_dataframe() -> pd.DataFrame:
    """Fixture: returns a dummy data"""
    # current file path
    current_path = __file__
    # csv file name
    # file_name = "healthcare-dataset-stroke-data.csv"
    file_name = "heart_stroke_data_handled_missing_values.csv"
    # travers outside the current path by 6 folders
    file_path = get_data_path(current_path, 5)
    # naviget to data path
    data_path = os.path.join(file_path, "notebooks", "data", file_name)
    # read data
    df = pd.read_csv(data_path)
    # sample data
    train, test = train_test_split(df, test_size=0.195, stratify=df['stroke'])
    # return data
    return test

@pytest.fixture
def get_preprocessor():
    """
    load the ColumnarTransformer pipeline
    """
    current_path = __file__

    file_name = "feature_engineering_pipeline_v1.pkl"

    file_path = get_data_path(current_path, 5)
    # naviget to data path
    preprocessor_path = os.path.join(file_path, "notebooks", "artifacts", file_name)

    # Manually inject the function into the __main__ module
    import __main__
    __main__.create_interaction = create_interaction

    with open(preprocessor_path, "rb") as f:
        preprocessor = cloudpickle.load(f)

    return preprocessor

@pytest.fixture
def get_config(raw_dataframe, get_preprocessor):
    """
    Docstring for get_config
    """
    config = {
            "df": raw_dataframe,
            "scaler_type": "standard",
            "preprocessor": get_preprocessor,
            "shuffle": True,
            "n_splits": 5,
            "n_repeats": 10,
            "seed": 42,
            "model_type": "classification",
            "bins": 10,
    }

    return config

@pytest.fixture
def base_config():
    """Centralized configuration values"""
    return {
        "scaler_type": "standard",
        "use_smote": "smote",
        "primary_scoring": 'recall',
        "secondary_scoring": ['f1', 'recall', 'precision'],
        "shuffle": True,
        "n_splits": 3,
        "n_repeats": 2,
        "seed": 42,
        "model_type": "classification",
        "bins": None,
    }

def get_dataframe() -> pd.DataFrame:
    """returns a dummy data"""
    # current file path
    current_path = __file__
    # csv file name
    file_name = "healthcare-dataset-stroke-data.csv"
    # travers outside the current path by 6 folders
    file_path = get_data_path(current_path, 5)
    # naviget to data path
    data_path = os.path.join(file_path, "notebooks", "data", file_name)
    # read data
    df = pd.read_csv(data_path)
    # sample data
    _, test = train_test_split(df, test_size=0.0195, stratify=df['stroke'])
    # return data
    return test

# if __name__ == "__main__":
#     print(get_dataframe().columns)
