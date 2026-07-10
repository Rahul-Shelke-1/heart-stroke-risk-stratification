from abc import ABC, abstractmethod
from typing import List

import pandas as pd


# Abstract Base Class for Data Inspection Strategies
# --------------------------------------------------
# This class defines a common interface for data inspection strategies.
# Subclasses must implement the inspect method.
class DataInspectionStrategy(ABC):
    @abstractmethod
    def inspect(self, df: pd.DataFrame):
        """
        Perform a specific type of data inspection.

        Parameters:
        df (pd.DataFrame): The dataframe on which the inspection is to be performed.

        Returns:
        None: This method prints the inspection results directly.
        """
        pass


# Concrete Strategy for Data Types Inspection
# --------------------------------------------
# This strategy inspects the data types of each column and counts non-null values.
class DataTypesInspectionStrategy(DataInspectionStrategy):
    def inspect(self, df: pd.DataFrame):
        """
        Inspects and prints the data types and non-null counts of the dataframe columns.

        Parameters:
        df (pd.DataFrame): The dataframe to be inspected.

        Returns:
        None: Prints the data types and non-null counts to the console.
        """
        print("\nData Types and Non-null Counts:")
        print(df.info())


# Concrete Strategy for Summary Statistics Inspection
# -----------------------------------------------------
# This strategy provides summary statistics for both numerical and categorical features.
class SummaryStatisticsInspectionStrategy(DataInspectionStrategy):
    def inspect(self, df: pd.DataFrame):
        """
        Prints summary statistics for numerical and categorical features.

        Parameters:
        df (pd.DataFrame): The dataframe to be inspected.

        Returns:
        None: Prints summary statistics to the console.
        """
        print("\nSummary Statistics (Numerical Features):")
        print(df.describe())
        print("\nSummary Statistics (Categorical Features):")
        print(df.describe(include=["O"]))


class CategoricalColumnInspectionStartegy(DataInspectionStrategy):

    def set_categorical_columns(self, cat_col_list: List[str]):
        self.cat_col_list = cat_col_list

    def inspect(self, df):
        """
        Prints columns name, number of uqniue values it has and unique values

        Parameters:
        df (pd.DataFrame): The dataframe to be inspected.

        Returns:
        None: Prints columns name, nunique and uniques to the console.
        """
        if self.cat_col_list is None:
            raise ValueError("Categorical column name list is not set.")

        try:
            for col in self.cat_col_list:
                print('-'*25)
                print(f"\ncolumn name: {col}")
                print(f"\n# unique: {df[col].nunique()}")
                print(f"\nunique values: {df[col].unique()}")
            print('-'*25)
        except Exception:
            raise ValueError(f"Column name {col} might not be present in datafarme")

class NumericalColumnInspectionStartegy(DataInspectionStrategy):

    def set_numerical_columns(self, num_col_list: List[str]):
        self.num_col_list = num_col_list

    def inspect(self, df):
        """
        Prints columns name, number of uqniue values it has and unique values

        Parameters:
        df (pd.DataFrame): The dataframe to be inspected.

        Returns:
        None: Prints columns name, nunique and uniques to the console.
        """
        if self.num_col_list is None:
            raise ValueError("Categorical column name list is not set.")

        try:
            for col in self.num_col_list:
                print('-'*25)
                print(f"\ncolumn name: {col}")
                print(f"\n# unique: {df[col].nunique()}")
                positive_list = []
                zero = []
                negative_list = []
                null_list = []
                for i in df[col].unique():
                    if i > 0:
                        positive_list.append(i)
                    elif i < 0:
                        negative_list.append(i)
                    elif i == 0:
                        zero.append(i)
                    else:
                        null_list.append(i)
                print(f"\n+ve values: {positive_list}")
                print(f"\nzeros: {zero}")
                print(f"\n-ve values: {negative_list}")
                print(f"\nnull values: {null_list}")
            print('-'*25)
        except Exception:
            raise ValueError(f"Column name {col} might not be present in datafarme")

# Context Class that uses a DataInspectionStrategy
# ------------------------------------------------
# This class allows you to switch between different data inspection strategies.
class DataInspector:
    def __init__(self, strategy: DataInspectionStrategy):
        """
        Initializes the DataInspector with a specific inspection strategy.

        Parameters:
        strategy (DataInspectionStrategy): The strategy to be used for data inspection.

        Returns:
        None
        """
        self._strategy = strategy

    def set_strategy(self, strategy: DataInspectionStrategy):
        """
        Sets a new strategy for the DataInspector.

        Parameters:
        strategy (DataInspectionStrategy): The new strategy to be used for data inspection.

        Returns:
        None
        """
        self._strategy = strategy

    def execute_inspection(self, df: pd.DataFrame):
        """
        Executes the inspection using the current strategy.

        Parameters:
        df (pd.DataFrame): The dataframe to be inspected.

        Returns:
        None: Executes the strategy's inspection method.
        """
        self._strategy.inspect(df)
