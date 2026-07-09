from __future__ import annotations

import re
from typing import Dict, Optional

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class ColumnNameCorrector(BaseEstimator, TransformerMixin):
    """
    Column correction

    Responsibility
    --------------

    - Enforce naming conventions
    - Remove ambiguity
    - Ensure downstream transformers never break

    Examples
    --------

    "Avg Height"  → "avg_height"
    "Heart Rate" → "heart_rate"
    "chol%"      → "chol_pct"

    Bahviour
    --------

    1. if mapping exists -> apply mapping

    2. Else -> apply normalization rule:
        - strip
        - lower case
        - replace spaces/symbols
        - enforce snake_case
    """
    def __init__(self, mapping: Optional[Dict[str, str]] = None):
        self.mapping = mapping or {}

    def fit(self, X: pd.DataFrame, y=None):
        return self

    @staticmethod
    def _to_snake_case(name: str) -> str:
        name = name.strip().lower()
        name = re.sub(r"[^\w\s]", "", name)
        name = re.sub(r"\s+", "_", name)
        name = re.sub(r"_+", "_", name)
        return name

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()

        # Step 1: explicit renaming
        if self.mapping:
            X = X.rename(columns=self.mapping)

        # Step 2: enforce snake_case
        X.columns = [self._to_snake_case(col) for col in X.columns]

        return X

    def get_feature_names_out(self, input_features=None):
        return input_features

class ValueCorrector(BaseEstimator, TransformerMixin):
    """
    Value standardizer

    Responsibility
    --------------
    - Normalize inconsistent categorical represntations
    - Remove sematoc noise

    Examples:
    ---------
    "m", "M", "male", "Male" → "male"
    "f", "F", "female"      → "female"
    "yes", "Y", "1"         → 1


    Why column-wise:
    - semantic are column-specific
    - global mapping is dangerous
    """
    def __init__(self, column_mappings: dict[str, dict]):
        """
        column_mappings: dic[str, str]
        {
          "sex": {"m": "male", "f": "female"},
          "smoker": {"yes": 1, "no": 0}
        }
        """
        self.column_mappings = column_mappings
        self.original_to_snake_case: dict[str, str] = {}  # Store mapping

    def fit(self, X: pd.DataFrame, y=None):
        # Store mapping from original to snake_case
        for col in X.columns:
            snake_col = ColumnNameCorrector._to_snake_case(col)
            self.original_to_snake_case[col] = snake_col
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()

        for column in X.columns:
            # Find if this column (or its snake_case version) has a mapping
            snake_column = ColumnNameCorrector._to_snake_case(column)

            # Check both original and snake_case version
            mapping_key = None
            if column in self.column_mappings:
                mapping_key = column
            elif snake_column in self.column_mappings:
                mapping_key = snake_column

            if mapping_key:
                mapping = self.column_mappings[mapping_key]
                X[column] = (
                    X[column]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .replace(mapping)
                )

        return X

    def get_feature_names_out(self, input_features=None):
        return input_features

class MissingValueNormalizer(BaseEstimator, TransformerMixin):
    def __init__(self, missing_tokens=None):
        self.missing_tokens = missing_tokens or ["unknown"]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        for token in self.missing_tokens:
            X[X == token] = np.nan
        return X

    def get_feature_names_out(self, input_features=None):
        return input_features

class FrequencyFilter(BaseEstimator, TransformerMixin):
    """
    """
    def __init__(self, threshold=1, action='drop', fill_value='other'):
        self.threshold = threshold
        self.action = action
        self.fill_value = fill_value
        self.columns_ = None

    def fit(self, X, y=None):
        # Identify categorical columns to check
        self.columns_ = X.select_dtypes(include=['object', 'category']).columns
        return self

    def transform(self, X):
        X = X.copy()
        for col in self.columns_:
            counts = X[col].value_counts()
            # Identify values that appear only 'threshold' times or fewer
            low_freq_mask = X[col].isin(counts[counts <= self.threshold].index)

            if self.action == 'drop':
                X = X[~low_freq_mask]
            elif self.action == 'group':
                X.loc[low_freq_mask, col] = self.fill_value
        return X

    def get_feature_names_out(self, input_features=None):
        return input_features
