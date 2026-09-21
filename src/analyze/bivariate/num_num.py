
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import seaborn as sns
from scipy.stats import pearsonr

from .base_analyzer import BaseAnalyzer


class NumericalNumericalBivariate(BaseAnalyzer):
    """
    Methods for analyzing the relationship between two numerical columns.
    """
    # --- Descriptive Analysis & Visual Analysis ---
    def plot_scatterplot_sns(self, x_col: str, y_col: str, hue: str = None):
        """Plots a static Seaborn scatter plot."""
        self._plot_static(
            sns.scatterplot,
            data=self.df,
            x=x_col,
            y=y_col,
            hue=hue
        )

    def plot_scatterplot_plotly(self, x_col: str, y_col: str, hue: str = None):
        """Plots an interactive Plotly scatter plot."""
        fig = px.scatter(
            self.df,
            x=x_col,
            y=y_col,
            color=hue,
            title=f'Interactive Scatter Plot: {x_col} vs {y_col}'
        )
        self._plot_dynamic(fig)

    def plot_jointplot_sns(
        self,
        x_col: str,
        y_col: str,
        kind: str = 'reg',
        line_color: str = 'red',
        alpha: float = 0.3,
        ci: int = 95
    ):
        """
        Plots a Seaborn joint plot (scatter + marginals) with hue support and regression lines.
        Kind can be 'scatter', 'reg', 'hist', 'hex', 'kde'.
        A legend is automatically added when hue is used.
        """
        # JointGrid manages its own figure, so we don't use _plot_sns_static
        sns.jointplot(
            data=self.df,
            x=x_col,
            y=y_col,
            kind=kind,
            line_kws={"color": line_color},
            ci=ci,
            scatter_kws={"alpha": alpha},
            )
        plt.show()

    def plot_correlation_heatmap(self, columns: list = None):
        """Plots a heatmap of correlations for a list of numerical variables."""
        data_to_plot = self.df[columns] if columns else self.df.select_dtypes(include=[np.number])
        corr = data_to_plot.corr(method='pearson')
        self._plot_static(
            sns.heatmap,
            data=corr,
            annot=True,
            cmap='coolwarm',
            fmt=".2f"
        )

    # --- Inferential Analysis ---
    def calculate_correlations(self, x_col: str, y_col: str):
        """
        Calculates Pearson (linear) and Spearman (rank-based) correlation coefficients.
        """
        pearson_corr = self.df[[x_col, y_col]].corr(method='pearson').iloc[0, 1]
        spearman_corr = self.df[[x_col, y_col]].corr(method='spearman').iloc[0, 1]
        print(f"--- Correlation Coefficients for {x_col} and {y_col} ---")
        print(f"Pearson (Linear):  {pearson_corr:.4f}")
        print(f"Spearman (Rank):   {spearman_corr:.4f}")
        return pearson_corr, spearman_corr

    def test_pearson_significance(self, col1: str, col2: str):
        """
        Performs a statistical test for Pearson correlation significance (p-value).
        """
        # Drop NaNs for the test
        temp_df = self.df[[col1, col2]].dropna()
        stat, p_value = pearsonr(temp_df[col1], temp_df[col2])

        print("\n--- Pearson Correlation Significance Test ---")
        print(f"Statistic: {stat:.4f}, P-value: {p_value:.4f}")
        if p_value < 0.05:
            print("Result: Significant correlation (reject null hypothesis of no correlation).")
        else:
            print("Result: Insignificant correlation (fail to reject null hypothesis).")

     # --- Predictive Analysis (Simple Baseline Modeling) ---
    def plot_linear_regression(self, x_col: str, y_col: str):
        """
        Plots a simple linear regression line using Seaborn regplot,
        providing a visual baseline for prediction.
        """
        sns.regplot(
            data=self.df,
            x=x_col,
            y=y_col,
            line_kws=dict(color="r")
        )
        plt.title(f'Linear Regression Fit: {y_col} vs {x_col}')
