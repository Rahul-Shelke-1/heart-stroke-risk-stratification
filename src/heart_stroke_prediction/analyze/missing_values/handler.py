from typing import Optional

import numpy as np
import pandas as pd


class MissingImputer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def impute_values(self, column: str, strategy: str = 'median', group_col: Optional[str] = None):
        """
        Performs imputation based on a chosen strategy. Modifies DataFrame in place.
        Strategies: 'median', 'mean', 'mode', 'group_median'.
        """
        if strategy == 'group_median' and group_col:
            # Impute based on the median of another group
            self.df[column] = self.df.groupby(group_col)[column].transform(lambda x: x.fillna(x.median()))
            print(f"Imputed '{column}' using '{group_col}' group median strategy.")
            return self.df

        if strategy == 'median':
            fill_value = self.df[column].median()
        elif strategy == 'mean':
            fill_value = self.df[column].mean()
        elif strategy == 'mode':
            fill_value = self.df[column].mode()[0] if not self.df[column].mode().empty else np.nan
        else:
            print("Unknown strategy.")
            return self.df

        self.df[column] = self.df[column].fillna(fill_value)
        print(f"Imputed '{column}' with global {strategy} value {fill_value}.")
        return self.df
