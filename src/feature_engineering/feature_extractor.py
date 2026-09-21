from typing import List, Optional

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class CustomFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Custome feature extractor

    Notes
    -----
    Author  : Rahul Shelke
    Created : 2025-07-24
    """

    def __init__(self, columns: List[str], new_column: List[str], as_array: Optional[bool] = False):
        self.columns = columns
        self.new_column = new_column
        self.as_array = as_array

    def fit(self, X: pd.DataFrame, y=None):
        # Store column order during fitting
        self.columns_ = [col for col in self.columns if col in X.columns]
        if len(self.columns_) != len(self.columns):
            missing = set(self.columns) - set(self.columns_)
            raise ValueError(f"Missing columns in fit: {missing}")

        self.new_column_ = self.new_column
        return self

    def transform(self, X: pd.DataFrame):
        X_copy = X.copy()

        # Ensure input includes all fitted columns in same order
        if not all(col in X_copy.columns for col in self.columns_):
            missing = set(self.columns_) - set(X_copy.columns)
            raise ValueError(f"Missing columns in transform: {missing}")

        # Transform selected columns
        X_transformed_array = X_copy[self.columns_[0]]/X_copy[self.columns_[1]]
        # Rewrap into DataFrame with correct column names
        X_transformed_df = pd.DataFrame(X_transformed_array, columns=self.new_column_, index=X.index)
        # Replace the original columns with imputed values
        X_copy[self.new_column_] = X_transformed_df

        return X_copy[self.new_column_].values if self.as_array else X_copy[self.new_column_]
