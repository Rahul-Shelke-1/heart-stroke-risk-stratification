import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import chi2_contingency

from .base_analyzer import BaseAnalyzer


class CategoricalCategoricalBivariate(BaseAnalyzer):
    """
    Methods for analyzing the relationship between two categorical columns.
    """

    # --- Descriptive Analysis & Visualization ---

    def create_contingency_table(self, col1: str, col2: str, normalize: bool = False) -> pd.DataFrame:
        """
        Creates a contingency (cross-tabulation) table of counts or proportions.
        If normalize=True, proportions are shown (normalized by all observations).
        """
        table = pd.crosstab(self.df[col1], self.df[col2], normalize=normalize)
        if normalize:
            table = table.round(4) * 100
            print(f"\n--- Proportions Table (%) for {col1} vs {col2} ---")
        else:
            print(f"\n--- Contingency Table (Counts) for {col1} vs {col2} ---")
        return table

    def plot_stacked_barplot_sns(self, col1: str, col2: str):
        """
        Plots a stacked or grouped bar chart to visualize conditional frequencies.
        Note: Seaborn countplot handles this best when setting `hue` and adjusting `multiple`.
        """
        sns.countplot(
            data=self.df,
            x=col1,
            hue=col2
        )
        plt.title(f'Stacked Bar Plot of {col1} by {col2}')
        plt.legend(title=col2)

    def plot_heatmap_contingency(self, col1: str, col2: str, normalize: bool = 'index'):
        """
        Plots a heatmap of the contingency table, normalized by 'index' (rows) or 'columns'.
        Useful for visualizing conditional probabilities (e.g., P(col2|col1)).
        """
        # Normalize to see proportions within each group (e.g., what percentage of Males are in HR?)
        # normalize='index' normalizes rows to 100%
        # normalize='columns' normalizes columns to 100%
        # normalize=False uses counts
        table = pd.crosstab(self.df[col1], self.df[col2], normalize=normalize)

        sns.heatmap(
            data=table,
            annot=True,
            cmap="YlGnBu",
            fmt=".2%" if normalize else "d"
        )
        plt.title(f'Heatmap of Proportions ({col1} normalized)')


    # --- Inferential Analysis (Statistical Tests of Association) ---

    def test_chi_squared_independence(self, col1: str, col2: str):
        """
        Performs a Chi-squared test for independence between two categorical variables.
        Null Hypothesis (H0): The variables are independent (no relationship).
        """
        contingency_table = pd.crosstab(self.df[col1], self.df[col2])
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)

        print(f"\n--- Chi-squared Test for Independence ({col1} vs {col2}) ---")
        print(f"Chi2 Statistic: {chi2:.4f}")
        print(f"P-value: {p_value:.4f}")
        print(f"Degrees of Freedom: {dof}")

        if p_value < 0.05:
            print("Result: Significant dependence found (reject H0). There IS a relationship between the variables.")
        else:
            print("Result: No significant dependence found (fail to reject H0). Variables are likely independent.")

    def calculate_cramers_v(self, col1: str, col2: str) -> float:
        """
        Calculates Cramer's V, a measure of association strength for categorical variables.
        Ranges from 0 (no association) to 1 (perfect association).
        """
        contingency_table = pd.crosstab(self.df[col1], self.df[col2])
        chi2 = chi2_contingency(contingency_table)[0]
        n = contingency_table.sum().sum()
        min_dim = min(contingency_table.shape) - 1

        # Calculate Cramer's V statistic
        v = np.sqrt(chi2 / (n * min_dim))

        print(f"\n--- Cramer's V Association Strength ({col1} vs {col2}) ---")
        print(f"Cramer's V: {v:.4f}")
        return v
