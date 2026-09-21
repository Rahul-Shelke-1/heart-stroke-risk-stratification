
import numpy as np
import pandas as pd


class OutlierTreater:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def remove_outliers(self, column: str, indices: pd.Index) -> pd.DataFrame:
        """
        Removes entire rows identified as outliers. Use with caution as data is lost.
        """
        df_cleaned = self.df.drop(indices, axis=0).reset_index(drop=True)
        print(f"Removed {len(indices)} rows containing outliers in '{column}'. Original shape: {self.df.shape}, New shape: {df_cleaned.shape}")
        return df_cleaned

    def cap_outliers(self, column: str, lower_bound: float, upper_bound: float, using_iqr: bool = True) -> pd.DataFrame:
        """
        Replaces outlier values with the upper or lower boundary value (Winsorization/Capping).
        This method retains all data points but limits extreme influence.
        """
        df_capped = self.df.copy()
        # column with new name
        if using_iqr:
            # create new column
            new_column_name = column+str('_cap_iqr')
            # copy existing values to column
            df_capped[new_column_name] = df_capped[column]
            # capping outlier in column
            df_capped[new_column_name] = np.where(df_capped[new_column_name] < lower_bound, lower_bound, df_capped[new_column_name])
            df_capped[new_column_name] = np.where(df_capped[new_column_name] > upper_bound, upper_bound, df_capped[new_column_name])
        else:
            # create new column
            new_column_name = column+str('_cap_zscore')
            # copy existing values to column
            df_capped[new_column_name] = df_capped[column]
            # capping outlier in column
            df_capped[new_column_name] = np.where(df_capped[new_column_name] < lower_bound, lower_bound, df_capped[new_column_name])
            df_capped[new_column_name] = np.where(df_capped[new_column_name] > upper_bound, upper_bound, df_capped[new_column_name])

        print(f"Capped outliers in '{column}' between [{lower_bound:.2f}, {upper_bound:.2f}] (Winsorization).")
        return df_capped

    def impute_outliers(self, column: str, indices: pd.Index, strategy: str = 'median', using_iqr: bool = True) -> pd.DataFrame:
        """
        Replaces outlier values with a central tendency measure (mean or median).
        This treats outliers like missing values.
        """
        df_imputed = self.df.copy()
        if strategy == 'median':
            fill_value = self.df[column].median()
        elif strategy == 'mean':
            fill_value = self.df[column].mean()
        else:
            print("Unknown imputation strategy. Use 'median' or 'mean'.")
            return self.df

        # column with new name
        if using_iqr:
            # create new column
            new_column_name = column+str('_impute_iqr')
            df_imputed[new_column_name] = df_imputed[column]
            df_imputed.loc[indices, new_column_name] = fill_value
        else:
            # create new column
            new_column_name = column+str('_impute_zscore')
            df_imputed[new_column_name] = df_imputed[column]
            df_imputed.loc[indices, new_column_name] = fill_value

        print(f"Imputed {len(indices)} outliers in '{column}' with the {strategy} value of {fill_value:.2f}.")
        return df_imputed
