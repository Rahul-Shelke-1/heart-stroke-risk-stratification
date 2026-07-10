import os

import pandas as pd
import pytest


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
    # _, test = train_test_split(df, test_size=0.0195, stratify=df['stroke'])
    # return data
    return df
