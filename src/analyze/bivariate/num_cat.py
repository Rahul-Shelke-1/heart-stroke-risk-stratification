import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
from scipy.stats import f_oneway, ttest_ind  # T-test and ANOVA

from .base_analyzer import BaseAnalyzer


class CategoricalNumericalBivariate(BaseAnalyzer):
    """
    Methods for analyzing the relationship between one categorical and one numerical column.
    """

    # --- Descriptive Analysis & Visualization ---

    def create_agg_table(self, cat_col: str, num_col: str, metrics: list = None) -> pd.DataFrame:
        """
        Creates a grouped aggregation table showing specified metrics (mean, median, std, etc.)
        of the numerical column for each category.
        """
        if metrics is None:
            metrics = ['mean', 'median', 'std', 'count', 'min', 'max']

        # Use pandas groupby and agg to create the desired table
        agg_table = self.df.groupby(cat_col)[num_col].agg(metrics).round(2)

        print(f"\n--- Aggregation Table for '{num_col}' grouped by '{cat_col}' ---")
        # Display the table cleanly in the notebook
        return agg_table

    def plot_boxplot_sns(self, cat_col: str, num_col: str):
        """Plots a static Seaborn box plot to compare numerical distribution across categories."""
        sns.boxplot(
            data=self.df,
            x=cat_col,
            y=num_col
        )
        plt.title(f'Box Plot of {num_col} by {cat_col}')

    def plot_violinplot_sns(self, cat_col: str, num_col: str):
        """Plots a static Seaborn violin plot for distribution comparison."""
        sns.violinplot(
            data=self.df,
            x=cat_col,
            y=num_col
        )
        plt.title(f'Violin Plot of {num_col} by {cat_col}')

    def plot_barplot_agg(self, cat_col: str, num_col: str, estimator=np.mean):
        """
        Plots a static Seaborn bar plot showing the mean/median of numerical variable
        for each category, with confidence intervals.
        """
        sns.barplot(
            data=self.df,
            x=cat_col,
            y=num_col,
            estimator=estimator, # Can be np.mean or np.median
            errorbar='sd' # Shows standard deviation
        )
        plt.title(f'Mean {num_col} by {cat_col}')

    def plot_boxplot_plotly(self, cat_col: str, num_col: str):
        """Plots an interactive Plotly box plot."""
        fig = px.box(
            self.df,
            x=cat_col,
            y=num_col,
            title=f'Interactive Box Plot: {num_col} by {cat_col}'
        )
        self._plot_dynamic(fig)

    def plot_density_by_category(self, cat_col: str, num_col: str):
        """Plots overlapping density plots for a deeper look at distributions."""
        sns.kdeplot(
            data=self.df,
            x=num_col,
            hue=cat_col,
            fill=True,
            common_norm=False,
            alpha=0.5
        )
        plt.title(f'Density Plot of {num_col} by {cat_col}')

    # --- Inferential Analysis (Statistical Tests) ---

    def test_group_means(self, cat_col: str, num_col: str):
        """
        Performs appropriate test (T-test for 2 groups, ANOVA for 3+ groups)
        to see if numerical means differ across categories.
        """
        groups = [self.df[num_col][self.df[cat_col] == g].dropna() for g in self.df[cat_col].unique()]
        num_groups = len(groups)

        print(f"\n--- Testing Mean Difference for {num_col} across {cat_col} groups ---")

        if num_groups == 2:
            stat, p_value = ttest_ind(groups[0], groups[1], equal_var=True)
            test_name = "Independent Samples T-test"
        elif num_groups >= 3:
            stat, p_value = f_oneway(*groups)
            test_name = "ANOVA (Analysis of Variance) F-test"
        else:
            print("Error: Need at least 2 categories to compare means.")
            return

        print(f"Test used: {test_name}")
        print(f"Statistic: {stat:.4f}, P-value: {p_value:.4f}")

        if p_value < 0.05:
            print("Result: Significant difference found between at least two group means.")
        else:
            print("Result: No significant difference found (means are likely similar).")

        # For tips on how to use ANOVA to test differences in means when there are more than two groups:
        # <layout>video(introSentence="For tips on how to use ANOVA to test differences in means when there are more than two groups:", results=["1.4.10"])</layout>

    # --- Prescriptive Analysis ---

    def suggest_imputation_strategy(self, cat_col: str, num_col: str):
        """
        Suggests an imputation strategy for the numerical column based on the
        relationship with the categorical variable (if a strong relationship exists).
        """
        # A simple check for significant difference using p-value threshold of 0.05
        # (This is a simplified check for demonstration)
        groups = [self.df[num_col][self.df[cat_col] == g].dropna() for g in self.df[cat_col].unique()]
        if len(groups) >= 2:
            _, p_value = f_oneway(*groups) if len(groups) >= 3 else ttest_ind(groups[0], groups[1], equal_var=True)

            if p_value < 0.05:
                print(f"Prescriptive Insight: There is a significant difference in {num_col} across {cat_col}.")
                print(f"Recommendation: Impute missing values in {num_col} using group-specific means/medians (e.g., impute HR salaries with the HR mean salary).")
            else:
                print(f"Prescriptive Insight: The means for {num_col} are similar across {cat_col}.")
                print(f"Recommendation: Impute missing values in {num_col} using the overall mean/median of the column.")
