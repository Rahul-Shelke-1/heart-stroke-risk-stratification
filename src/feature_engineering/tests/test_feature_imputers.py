import numpy as np
from sklearn.impute import SimpleImputer

from src.feature_engineering.feature_imputer import (CustomConstantImputer,
                                                     CustomImputer)


def test_custom_constant_imputer(raw_dataframe):
    column = 'bmi'
    imputer = CustomConstantImputer(
        columns=[column],
        missing_value=0.0,
        fill_value=np.nan
        )

    imputer.fit(raw_dataframe)
    output = imputer.transform(raw_dataframe)

    assert output[column].isna().sum() > 0

def test_custom_imputer(raw_dataframe):
    column = 'bmi'
    imputer = CustomImputer(
        columns=[column],
        imputer=SimpleImputer(missing_values=np.nan, strategy='mean')
    )
    imputer.fit(raw_dataframe)
    output = imputer.transform(raw_dataframe)

    assert output[column].isna().sum() == 0
