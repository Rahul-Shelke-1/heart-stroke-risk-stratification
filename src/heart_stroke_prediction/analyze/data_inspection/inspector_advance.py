from typing import List

import pandas as pd


class InspectData:
    """Main DataInspector class"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def summary(self) -> dict:
        """Returns comprehensive summary"""
        return {
            "shape": self.df.shape,
            "memory_usage": self.df.memory_usage().sum(),
            "duplicates": self.df.duplicated().sum(),
            "missing_values": self.df.isnull().sum().sum(),
            "data_types": self.df.dtypes.to_dict()
        }

    def columns(self) -> dict:
        """Categorize columns by type"""
        num_cols = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        cat_cols = self.df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        datetime_cols = self.df.select_dtypes(include=['datetime64', 'timedelta']).columns.tolist()

        return {
            "numerical": {"count": len(num_cols), "columns": num_cols},
            "categorical": {"count": len(cat_cols), "columns": cat_cols},
            "datetime": {"count": len(datetime_cols), "columns": datetime_cols}
        }

    def numerical_column_inspect(self, columns: List[str]) -> pd.DataFrame:
        """
        Inspect numerical columns with positive/negative/zero/null counts.

        Parameters:
        -----------
        columns : List[str]
            List of numerical column names to inspect

        Returns:
        --------
        pd.DataFrame
            DataFrame with inspection results for each column
        """
        results = []

        for col in columns:
            # Validate column exists and is numerical
            if col not in self.df.columns:
                warnings.warn(f"Column '{col}' not found in DataFrame", UserWarning)
                continue

            # Get the series once for efficiency
            series = self.df[col]

            # Calculate counts (using count() for efficiency)
            positive_count = (series > 0).sum()
            negative_count = (series < 0).sum()
            zero_count = (series == 0).sum()
            null_count = series.isna().sum()
            unique_count = series.nunique()

            # Build row dictionary
            row = {
                "column_name": col,
                "dtype": str(series.dtype),
                "unique_count": unique_count,
                "has_positive": True if positive_count > 0 else False,
                "has_negative": True if negative_count > 0 else False,
                "has_zero": True if zero_count > 0 else False,
                "positive_count": positive_count,
                "negative_count": negative_count,
                "zero_count": zero_count,
                "null_count": null_count,
                "total_count": len(series),
                "non_null_count": series.count(),
                "null_percentage": (null_count / len(series)) * 100 if len(series) > 0 else 0
            }

            results.append(row)

        # Create DataFrame with consistent column order
        columns_order = [
            "column_name", "dtype", "unique_count", "total_count",
            "non_null_count", "null_count", "null_percentage",
            "has_positive", "positive_count",
            "has_negative", "negative_count",
            "has_zero", "zero_count"
        ]

        df_result = pd.DataFrame(results)

        # Reorder columns and handle empty result
        if not df_result.empty:
            # Keep only columns that exist in the DataFrame
            existing_cols = [col for col in columns_order if col in df_result.columns]
            df_result = df_result[existing_cols]

        return df_result

    def categorical_column_inspect(self, columns: List[str]) -> pd.DataFrame:
        """
        Inspect categorical columns with appropriate metrics.

        Parameters:
        -----------
        columns : List[str]
            List of categorical column names to inspect

        Returns:
        --------
        pd.DataFrame
            DataFrame with categorical inspection results
        """
        results = []

        for col in columns:
            if col not in self.df.columns:
                warnings.warn(f"Column '{col}' not found in DataFrame", UserWarning)
                continue

            series = self.df[col]

            # Get value counts
            value_counts = series.value_counts(dropna=False)

            # Calculate metrics
            null_count = series.isna().sum()
            unique_count = series.nunique(dropna=False)  # Include NaN as a category if needed

            # Get top categories
            top_value = series.mode().iloc[0] if not series.mode().empty else None
            top_count = value_counts.iloc[0] if len(value_counts) > 0 else 0

            # Build result row
            row = {
                "column_name": col,
                "dtype": str(series.dtype),
                "total_count": len(series),
                "non_null_count": series.count(),
                "null_count": null_count,
                "null_percentage": (null_count / len(series) * 100) if len(series) > 0 else 0,
                "unique_count": unique_count,
                "cardinality": f"High ({unique_count})" if unique_count > 20 else f"Low ({unique_count})",
                "top_value": top_value,
                "top_count": top_count,
                "top_percentage": (top_count / len(series) * 100) if len(series) > 0 else 0,
                "has_null": "Yes" if null_count > 0 else "No"
            }

            results.append(row)

        return pd.DataFrame(results)
