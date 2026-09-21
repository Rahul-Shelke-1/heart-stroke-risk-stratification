import os

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.feature_engineering.feature_imputer import (CustomImputer)


def get_data_path(path, levels=1):
    """Go up N directory levels"""
    # Start from current test file
    result = os.path.realpath(path)
    for _ in range(levels):
        result = os.path.dirname(result)
    return result

def raw_dataframe() -> pd.DataFrame:
    """Fixture: returns a dummy data"""
    # current file path
    current_path = __file__
    # csv file name
    file_name = "healthcare-dataset-stroke-data.csv"
    # travers outside the current path by 6 folders
    file_path = get_data_path(current_path, 1)
    # naviget to data path
    data_path = os.path.join(file_path, "notebooks", "data", file_name)
    # read data
    df = pd.read_csv(data_path)
    # sample data
    # test_size = 0.0195
    train, test = train_test_split(df, test_size=0.0195, stratify=df['stroke'])
    # return data
    return (train, test)

def build_schema_correction_pipeline() -> Pipeline:
    """
    Returns a fully defined sklearn Pipeline
    Safe to serialize and reuse across stages
    """
    from src.heart_stroke_prediction.data_correction.schema_correction import (
        ColumnNameCorrector, ValueCorrector)

    column_correction_dict = {
        'Residence_type': 'residence_type'
    }
    value_correction_dict = {
        'gender': {'Male': 'male', 'Female': 'female', 'Other': 'other'},
        'ever_married': {'Yes':'yes', 'No': 'no'},
        'residence_type': {'Urban': 'urban', 'Rural': 'rural'},
        'smoking_status': {'formerly smoked': 'formerly_smoked',
                                'never smoked': 'never_smoked',
                                'Unknown': 'unknown'},
        'work_type': {'Private':'private', 'self-employed': 'self_employed',
                                'Govt_job': 'govt_job', 'Never_worked': 'never_worked',
                                'children': 'children'},
    }

    pipeline = Pipeline(
        steps=[
            ("correct_column_name", ColumnNameCorrector(column_correction_dict)),
            ("correct_row_values", ValueCorrector(value_correction_dict))
        ]
    )

    return pipeline

def build_missing_values_imputer_pipeline() -> Pipeline:
    # numerical imputation
    num_column = ['bmi']

    # replace NaN with mean
    impute_numerical_cols = CustomImputer(
            columns=num_column,
            imputer=SimpleImputer(
                missing_values=np.nan,
                strategy="median",
            )
        )

    # categorical imputation
    cat_column = ['smoking_status']

    impute_categorical_cols = CustomImputer(
            columns=cat_column,
            imputer=SimpleImputer(
                missing_values='unknown',
                strategy="most_frequent"
            )
        )

    # create pipeline
    pipeline = Pipeline(
        steps=[
            ('numerical_imputer', impute_numerical_cols),
            ('categorical_imputer', impute_categorical_cols)
        ]
    )

    return pipeline

def build_outlier_handler_pipeline() -> Pipeline:
    # numrical columns
    pass

def build_feature_engineering_pipeline() -> Pipeline:
    # categorical variable

    # numerical variable
    pass


if __name__ == "__main__":
    df, _ = raw_dataframe()
    print(df.columns)
    print()
    print(df.head())
    print()
    print(df.tail())

    # get schema correction pipeline
    schema_correction_pipeline = build_schema_correction_pipeline()
    # get missing value imputer pipeline
    missing_values_imputer_pipeline = build_missing_values_imputer_pipeline()
    # get outlier handler pipeline
    # outlier_handler_pipeline = build_outlier_handler_pipeline()
    # get feature engineering pipeline
    # feature_engineering_pipeline = build_feature_engineering_pipeline()

    # add to column tranformation
    # preprocess = ColumnTransformer(
    #     [
              # schema correction pipeline
    #         ("schema_correction", build_data_cleaning_pipeline(), df.columns),
              # missing value imputer pipeline
    #         ("missing_value_imputer", build_missing_values_imputer_pipeline(), df.columns),
              # outlier handeling pipeline
    #         ("outlier_handler", build_outlier_handler_pipeline(), df.columns),
              # data preprocessing pipeline
    #         ("preprocessing", build_feature_engineering_pipeline(), df.columns),
    #     ]
    # )
    # d = preprocess.fit_transform(df)
    # print(d.columns)
    df_ = schema_correction_pipeline.fit_transform(df)

    print(df_.columns)
    print()

    df_ = missing_values_imputer_pipeline.fit_transform(df_)
    print(df_.head())
    print()
    print(df_.tail())
