import pandas as pd
import pytest


@pytest.fixture
def raw_dataframe() -> pd.DataFrame:
    "fixture: returns raw data frame"
    df = pd.DataFrame({
        "":[]
    })
    return df
