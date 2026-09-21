from typing import List, Optional, Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array, check_is_fitted


class CustomConstantImputer(BaseEstimator, TransformerMixin):
    """
    Custome constant imputer, which replaces missing value with a provided constant value

    Parameters
    ----------
    columns : list of str
        pass the column names in list
    missing_value : float
        value which represented as missing in columns
    fill_value : float
        value which will replace missing value in column
    as_array : bool (default False)
        return as np.array or pd.DataFrame

    Attributes
    ----------
    missing_value_ : float
        storing value which represnts as missing in column
    fill_value_ : float
        storing value which will replace missing value in column

    Methods
    -------
    fit(X, y=None)
        fits data provided imputer object from sklearn.

    transform(X)
        Returns the imputed columns bases on parameter(return_array)

    Notes
    -----
    Author  : Rahul Shelke
    Created : 2025-07-24
    """
    def __init__(self, columns: List[str], missing_value: Optional[float]=0.0, fill_value: Optional[float]=np.nan, as_array: Optional[bool] = False):
        self.columns = columns
        self.missing_value = missing_value
        self.fill_value = fill_value
        self.as_array = as_array

    def fit(self, X, y=None):
        """
        storing values
        """
        self.columns_ = self.columns
        self.missing_value_ = self.missing_value
        self.fill_value_ = self.fill_value
        return self

    def transform(self, X):
        X_copy = X.copy()
        X_copy[self.columns_] = X_copy[self.columns_].replace(self.missing_value_, self.fill_value_)
        return X_copy.values if self.as_array else X_copy

class CustomImputer(BaseEstimator, TransformerMixin):
    """
    Custome imputer, which utilizes scikit-learn imputers

    Parameters
    ----------
    columns : list of str
        The columns list on which operation should be performed
    imputer : scikit-learn imputer object
        Define the imputation operation
    as_array : bool
        Want to return as np.array or pd.DataFrame

    Attributes
    ----------
    columns_ : list of str
        keeping the columns order in check

    Methods
    -------
    fit(X, y=None)
        fits data provided imputer object from sklearn.

    transform(X)
        Returns the imputed columns bases on parameter(return_array)

    Notes
    -----
    Author  : Rahul Shelke
    Created : 2025-07-24
    """

    def __init__(self, columns: List[str], imputer: Union[BaseEstimator, TransformerMixin], as_array: Optional[bool] = False):
        self.columns = columns
        self.imputer = imputer
        self.as_array = as_array

    def fit(self, X: pd.DataFrame, y=None):
        # Store column order during fitting
        self.columns_ = [col for col in self.columns if col in X.columns]
        if len(self.columns_) != len(self.columns):
            missing = set(self.columns) - set(self.columns_)
            raise ValueError(f"Missing columns in fit: {missing}")

        self.imputer.fit(X[self.columns_])
        return self

    def transform(self, X: pd.DataFrame):
        X_copy = X.copy()

        # Ensure input includes all fitted columns in same order
        if not all(col in X_copy.columns for col in self.columns_):
            missing = set(self.columns_) - set(X_copy.columns)
            raise ValueError(f"Missing columns in transform: {missing}")

        # Transform selected columns
        X_transformed_array = self.imputer.transform(X_copy[self.columns_])
        # Rewrap into DataFrame with correct column names
        X_transformed_df = pd.DataFrame(X_transformed_array, columns=self.columns_, index=X.index)
        # Replace the original columns with imputed values
        X_copy[self.columns] = X_transformed_df

        return X_copy.values if self.as_array else X_copy

class OutlierHandler(BaseEstimator, TransformerMixin):
    """Production-ready outlier handler with multiple strategies"""

    def __init__(self, method='clip', threshold=1.5, fill_value=None):
        self.method = method
        self.threshold = threshold
        self.fill_value = fill_value

    def fit(self, X, y=None):
        X = check_array(X)
        self.n_features_in_ = X.shape[1]

        if self.method in ['clip', 'remove', 'nan']:
            q1 = np.nanpercentile(X, 25, axis=0)
            q3 = np.nanpercentile(X, 75, axis=0)
            iqr = q3 - q1
            self.lower_bounds_ = q1 - self.threshold * iqr
            self.upper_bounds_ = q3 + self.threshold * iqr

        return self

    def transform(self, X):
        check_is_fitted(self)
        X = check_array(X)

        if self.method == 'clip':
            return np.clip(X, self.lower_bounds_, self.upper_bounds_)

        elif self.method == 'nan':
            X_out = X.copy()
            for i in range(X.shape[1]):
                outliers = (X[:, i] < self.lower_bounds_[i]) | (X[:, i] > self.upper_bounds_[i])
                X_out[outliers, i] = np.nan
            return X_out

        elif self.method == 'median':
            X_out = X.copy()
            for i in range(X.shape[1]):
                outliers = (X[:, i] < self.lower_bounds_[i]) | (X[:, i] > self.upper_bounds_[i])
                median_val = np.median(X[~outliers, i]) if np.any(~outliers) else 0
                X_out[outliers, i] = median_val
            return X_out

        else:  # 'remove' - not typically used in transform
            return X

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)
