import pandas as pd
import numpy as np
from typing import List, Optional

class OutlierDetector:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def find_outliers_iqr(self, column: str) -> dict:
        """
        Detects outliers using the Tukey IQR method (1.5 * IQR rule), 
        suitable for both normal and skewed data distributions.
        Returns bounds and a DataFrame of outlier indices.
        """
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers_indices = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)].index
        
        print(f"\n--- IQR Outlier Report for '{column}' ---")
        print(f"Total Rows: {len(self.df)}")
        print(f"Bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
        print(f"Outliers Found (Count/Percent): {len(outliers_indices)} ({(len(outliers_indices)/len(self.df)*100):.2f}%)")
        
        return {
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outlier_indices': outliers_indices
        }

    def find_outliers_zscore(self, column: str, threshold: float = 3.0) -> dict:
        """
        Detects outliers using the Z-score method (standard deviation rule), 
        best for normally distributed data.
        Returns bounds and a DataFrame of outlier indices.
        """
        mean = self.df[column].mean()
        std = self.df[column].std()
        lower_bound = mean - threshold * std
        upper_bound = mean + threshold * std

        # Calculate Z-scores and find indices where abs(Z) > threshold
        z_scores = (self.df[column] - mean) / std
        outliers_indices = self.df[np.abs(z_scores) > threshold].index

        print(f"\n--- Z-Score Outlier Report for '{column}' (Threshold +/- {threshold} SD) ---")
        print(f"Total Rows: {len(self.df)}")
        print(f"Bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
        print(f"Outliers Found (Count/Percent): {len(outliers_indices)} ({(len(outliers_indices)/len(self.df)*100):.2f}%)")

        return {
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outlier_indices': outliers_indices
        }
    
    # You could add visual methods here using your existing visualize modules

