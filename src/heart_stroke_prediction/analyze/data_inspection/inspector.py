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
        for col in columns:
            nunique = self.df[col].nunique()
            positive_value_count = self.df[self.df[col] > 0][col].nunique()
            positive_values = f"True | ({positive_value_count})" if positive_value_count > 0 else "False | (0)"
            negative_value_count = self.df[self.df[col] < 0][col].nunique()
            negative_values = f"True | ({negative_value_count})" if negative_value_count > 0 else "False | (0)"
            zero_count = self.df[self.df[col] == 0][col].nunique()
            null_count = self.df[col].isna().sum()
            print('-'*25)
            print()
            print(f"column name: {col}\n")
            print(f"# unique: {nunique}\n")
            print(f"+ve values: {positive_values}\n")
            print(f"zeros: {zero_count}\n")
            print(f"-ve values: {negative_values}\n")
            print(f"null values: {null_count}\n")
        print('-'*25)

    def categorical_column_inspect(self, columns: List[str]) -> pd.DataFrame:
        for col in columns:
            nunique = self.df[col].nunique()
            unique = self.df[col].unique()
            max_count = self.df[col].dropna().value_counts().idxmax()
            min_count = self.df[col].dropna().value_counts().idxmin()
            null_count = self.df[col].isna().sum()
            print('-'*25)
            print()
            print(f"column name: {col}\n")
            print(f"# unique: {nunique}\n")
            print(f"unique values: {unique}\n")
            print(f"max: {max_count}\n")
            print(f"min: {min_count}\n")
            print(f"null count: {null_count}\n")
        print('-'*25)
