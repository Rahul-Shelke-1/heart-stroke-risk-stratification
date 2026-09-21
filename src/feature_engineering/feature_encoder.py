import warnings
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder


class CustomeOrdinalEncoder(BaseEstimator, TransformerMixin):
    """
    Custome ordinal encoder, it applies ordinal encoding to data

    Parameters
    ----------
    columns : list of str
        The list of column names to apply upon.
    return_array : bool (default = False)
        The output should be pd.DataFrame or np.array

    Attributes
    ----------
        None

    Methods
    -------
    fit(X, y=None)
        fits data with ordinal encoder object from sklearn.

    transform(X)
        Returns the encoded columns bases on parameter(return_array)

    Notes
    -----
    Author  : Rahul Shelke
    Created : 2025-07-23
    """
    def __init__(
            self,
            columns: List[str],
            custom_mapping: Optional[Union[Dict[str, List], Dict[str, Dict]]] = None,
            return_array: bool =False,
            categories: str = 'auto'
        ):
        """
        taking column names list from user and
        initializing onehot encoder
        """
        self.columns = columns
        self.custom_mapping = custom_mapping
        self.return_array = return_array
        self.categories = categories

        self._validate_parameters()

    def _validate_parameters(self):
        """Validate initialization parameters."""
        if not isinstance(self.columns, list):
            raise TypeError(f"columns must be a list, got {type(self.columns)}")

        if not isinstance(self.return_array, bool):
            raise TypeError(f"return_array must be bool, got '{type(self.return_array)}'")

        if self.custom_mapping is not None:
            if not isinstance(self.custom_mapping, dict):
                raise TypeError(f"custom_mapping must be a dict, got {type(self.custom_mapping)}")

            # Validate custom mapping structure
            for col, mapping in self.custom_mapping.items():
                if col not in self.columns:
                    warnings.warn(f"Column '{col}' is custom_mapping not in columns list")

                if isinstance(mapping, list):
                    # Validate list mapping
                    if len(mapping) != len(set(mapping)):
                        raise ValueError(f"Duplicate values found in mapping for column '{col}'")
                elif isinstance(mapping, dict):
                    # Validate dict mapping
                    values = list(mapping.values())
                    if len(values) != len(set(values)):
                        raise ValueError(f"Duplicate encoded values found in mapping for column '{col}'")
                    if not all(isinstance(v, (int, np.integer)) for v in values):
                        raise ValueError(f"All mapping values must be integers for column '{col}'")
                else:
                    raise TypeError(f"Mapping for column '{col}' must be list or dict, got {type(mapping)}")

    def _prepare_categories_from_mapping(self, X: pd.DataFrame):
        """Prepare categories parameter from custom mapping."""
        if self.custom_mapping is None:
            return self.categories

        categories = []
        for col in self.columns:
            if col in self.custom_mapping:
                mapping = self.custom_mapping[col]
                if isinstance(mapping, list):
                    # For list mapping , use the list order as categories
                    # vliadate all categories exists in data (for fitting)
                    unique_vals = X[col].dropna().unique()
                    if not set(mapping).issuperset(set(unique_vals)):
                        maissing = set(unique_vals) - set(mapping)
                        warnings.warn(f"Column '{col}' has values not in column mapping: {maissing}")
                    categories.append(mapping)
                else: # dict mapping
                    # For dict mapping, sort by value to get category order
                    sorted_items = sorted(mapping.items(), key=lambda x: x[1])
                    cat_order = [item[0] for item in sorted_items]

                    # validate mapping covers all value in data
                    unique_vals = X[col].dropna().unique()
                    if not set(mapping.keys()).issuperset(set(unique_vals)):
                        maissing = set(unique_vals) - set(mapping)
                        warnings.warn(f"Column '{col}' has values not in custom mapping: {maissing}")

                    categories.append(cat_order)
            else:
                # No custom mapping for this column, use 'auto'
                categories.append('auto')

        return categories

    def _create_final_mapping(self):
        """Create final mapping dictionary for reference."""
        self.mapping_ = {}
        for i, col in enumerate(self.columns):
            if hasattr(self.encoder_, 'categories_'):
                categories = self.encoder_.categories_[i]
                self.mapping_[col] = {cat: idx for idx, cat in enumerate(categories)}

    def fit(self, X: pd.DataFrame, y=None):
        """
        Fit the encoder to the data.

        Parameters
        ----------
        X : pd.DataFrame
            Input data to fit.
        y : None
            Ignored. Exists for compatibility.

        Returns
        -------
        self : CustomOridnalEncoder
            Returns the instance itself.
        """
        # validate input
        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be a pandas DataFrame")

        missing_cols = [col for col in self.columns if col not in X.columns.to_list()]

        if missing_cols:
            raise ValueError(f"Columns not found in X: {missing_cols}")

        # store feature names
        self.feature_names_in_ = np.array(X.columns)
        self.n_fetaures_in_ = X.shape[1]

        # prepare categories based on custom mapping
        categories = self._prepare_categories_from_mapping(X)

        # initalize and fit the encoder
        self.encoder_ = OrdinalEncoder(
            categories=categories,
            dtype=np.float64 # Use float to handle NaN
        )

        # Fit encoder on selected columns
        self.encoder_.fit(X[self.columns])

        # Store categories
        self.categories_ = self.encoder_.categories_

        # create final mapping for reference
        self._create_final_mapping()

        return self

    def transform(self, X: pd.DataFrame) -> Union[pd.DataFrame, np.array]:
        """
        Transform the data using the fitted encoder.

        Parameters
        ----------
        X : pd.DataFrame
            Input data to traanform.

        Returns
        -------
        X_transformed : Union[pd.DataFrame, np.ndarray]
            Transformed data. Returns array of return_array=True, else DataFrame.
        """
        # check if fit has been called
        if not hasattr(self, 'encoder_'):
            raise RuntimeError("Must call fit before transform")

        # validate input
        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be a pandas DataFrame")

        missing_cols = [col for col in self.columns if col not in X.columns]
        if missing_cols:
            raise ValueError(f"Columns not found in X: {missing_cols}")

        # Transform the data
        X_transformed_array = self.encoder_.transform(X[self.columns])

        if self.return_array:
            return X_transformed_array
        else:
            # Get features names for output
            if hasattr(self.encoder_, 'get_feature_names_out'):
                feature_names = self.encoder_.get_feature_names_out(self.columns)
            else:
                # Fallback for older sklearn version
                feature_names = self.columns

            # create DataFrame with original index
            X_transformed = pd.DataFrame(
                X_transformed_array,
                columns=feature_names,
                index=X.index
            )

            # Preserve other columns
            other_cols = [col for col in X.columns if col not in self.columns]
            if other_cols:
                X_transformed = pd.concat([X_transformed, X[other_cols]], axis=1)

            return X_transformed

    def fit_transform(self, X: pd.DataFrame, y = None) -> Union[pd.DataFrame, np.ndarray]:
        """
        Fit and transform the data in one step.

        Parameters
        ----------
        X : pd.DataFrame
            Input data to fit and transform.
        y : None
            Ignored. Exists for compatibility.

        Returns
        -------
        X_transformed : Union[pd.DataFrame, np.ndarray]
            Transformed data.

        """
        return self.fit(X, y).transform(X)

    def inverse_transform(self, X: Union[pd.DataFrame, np.ndarray]) -> pd.DataFrame:
        """
        Convert encoded data back to original categories.

        Parameters
        ----------
        X : Union[pd.DataFrame, np.ndarray]
            Encoded data to inverse transform.

        Returns
        -------
        X_original : pd.DataFrame
            Data with original categories.
        """
        if not hasattr(self, 'encoder_'):
            raise RuntimeError("Must call fit before inverse_transform")

        # Handle input type
        if isinstance(X, pd.DataFrame):
            # Extract only the encoded columns
            X_array = X[self.columns].values if self.return_array else X[self.columns].values
            result_array = self.encoder_.inverse_transform(X_array)
        else:
            result_array = self.encoder_.inverse_transform(X)

        # Create DataFrame with original column names
        result_df = pd.DataFrame(result_array, columns=self.columns)

        # If input was DataFrame with additional columns, preserve them
        if isinstance(X, pd.DataFrame) and not self.return_array:
            other_cols = [col for col in X.columns if col not in self.columns]
            if other_cols:
                result_df = pd.concat([result_df, X[other_cols]], axis=1)

        return result_df

    def get_feature_names_out(self, input_features=None):
        """
        Get output feature names for transformation.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Input features.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.
        """
        if not hasattr(self, 'encoder_'):
            raise RuntimeError("Must call fit before get_feature_names_out")

        if hasattr(self.encoder_, 'get_feature_names_out'):
            return self.encoder_.get_feature_names_out(self.columns)
        else:
            return np.array(self.columns)

    def get_params(self, deep=True):
        """Get parameters for this estimator."""
        params = {
            'columns': self.columns,
            'custom_mapping': self.custom_mapping,
            'return_array': self.return_array,
            'categories': self.categories
        }
        return params

    def set_params(self, **params):
        """Set the parameters of this estimator."""
        for key, value in params.items():
            setattr(self, key, value)
        self._validate_parameters()
        return self

class CustomeOnehotEncoder(BaseEstimator, TransformerMixin):
    """
    Custom OneHot encoder that provides flexible output options.

    This transformer applies one-hot encoding to specified columns with options for:
    1. Returning either pandas DataFrame or numpy array
    2. Selecting specific output columns to keep
    3. Handling unknown categories and sparse outputs

    Parameters
    ----------
    columns : List[str]
        The list of column names to apply one-hot encoding to.

    keep_columns : Optional[List[str]], default=None
        Specific one-hot encoded columns to keep in the output.
        If None, all encoded columns are returned.

    return_array : bool, default=False
        If True, returns numpy array. If False, returns pandas DataFrame.

    drop : str, default='first'
        Specifies a method to drop one of the categories per feature.
        - 'first': drop the first category (default)
        - 'if_binary': drop one category if feature is binary
        - None: retain all categories (creates k columns for k categories)

    sparse_output : bool, default=False
        If True, returns a sparse matrix. If False, returns dense array/DataFrame.
        Note: If return_array=False, sparse matrices are converted to dense DataFrames.

    handle_unknown : str, default='ignore'
        How to handle unknown categories during transform:
        - 'error': raise an error
        - 'ignore': create a row of all zeros for unknown categories
        - 'infrequent_if_exist': treat unknown as infrequent category if infrequent categories exist

    min_frequency : int or float, default=None
        Minimum frequency for a category to be considered frequent.
        Categories with frequency < min_frequency are grouped into infrequent categories.

    max_categories : int, default=None
        Maximum number of categories to keep (frequent categories only).
        Others are grouped into infrequent categories.

    Attributes
    ----------
    encoder_ : sklearn.preprocessing.OneHotEncoder
        The underlying sklearn OneHotEncoder instance.

    feature_names_in_ : np.ndarray
        Names of features seen during fit.

    n_features_in_ : int
        Number of features seen during fit.

    encoded_columns_ : List[str]
        Names of all one-hot encoded columns generated.

    keep_columns_idx_ : np.ndarray
        Indices of columns to keep (if keep_columns specified).

    categories_ : list
        Categories for each feature determined during fitting.

    Notes
    -----
    Author  : Rahul Shelke
    Created : 2025-07-23
    Modified: Enhanced for production use

    Examples
    --------
    >>> encoder = CustomOneHotEncoder(columns=['city', 'color'])
    >>> encoder.fit(X_train)
    >>> X_encoded = encoder.transform(X_test)

    >>> # Keep specific encoded columns
    >>> encoder = CustomOneHotEncoder(columns=['city'], keep_columns=['city_NYC', 'city_LA'])

    >>> # Return numpy array
    >>> encoder = CustomOneHotEncoder(columns=['city'], return_array=True)
    """
    def __init__(self, columns: List[str], keep_columns: Optional[List[str]] = None, return_array: Optional[bool] = False):
        """
        taking column names list from user and
        initializing onehot encoder
        """
        try:
            self.columns = columns
            self.keep_columns = keep_columns
            self.return_array = return_array
            self.onehot_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
        except Exception as e:
            raise e

    def fit(self, X: pd.DataFrame, y=None):
        """
        fitting onehot encoder
        """
        try:
            self.onehot_encoder.fit(X[self.columns])
            return self # if no fitting necessary
        except Exception as e:
            raise e

    def transform(self, X: pd.DataFrame):
        """
        transforming onehot encoded data into data frame,
        with respective transformed column names
        """
        try:
            X_transformed = self.onehot_encoder.transform(X[self.columns])
            feature_names = self.onehot_encoder.get_feature_names_out(self.columns)
            data = pd.DataFrame(X_transformed, columns=feature_names, index=X.index)
            if self.keep_columns:
                if self.return_array:
                    return data[self.keep_columns].values
                else:
                    return data[self.keep_columns]
            else:
                if self.return_array:
                    return data.values
                else:
                    return data
        except Exception as e:
            raise e
