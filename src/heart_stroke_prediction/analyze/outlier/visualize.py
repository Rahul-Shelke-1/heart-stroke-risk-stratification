import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from typing import List

class OutlierVisualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def plot_boxplot(self, column: str):
        """
        Plots a box plot to visually identify outliers (points beyond the whiskers).
        Outliers are explicitly marked as individual points.
        """
        plt.figure(figsize=(8, 6))
        # Seaborn automatically plots outliers as points using the IQR method
        sns.boxplot(data=self.df, x=column)
        plt.title(f'Box Plot of {column} (Outliers shown as points)')
        plt.show()
        
    def plot_histogram_kde(self, column: str):
        """
        Plots a histogram and Kernel Density Estimate (KDE) to show the distribution shape.
        Outliers appear as isolated bars or long tails far from the main peak.
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.df, x=column, kde=True, bins=30)
        plt.title(f'Histogram and KDE Plot of {column}')
        plt.show()

    def plot_distribution_with_bounds(self, column: str, lower_bound: float, upper_bound: float):
        """
        Plots a histogram with vertical lines marking calculated outlier bounds (e.g., from IQR or Z-score).
        """
        plt.figure(figsize=(10, 6))
        ax = sns.histplot(data=self.df, x=column, kde=True, bins=30)
        
        # Add vertical lines for the calculated bounds
        ax.axvline(lower_bound, color='red', linestyle='--', lw=2, label=f'Lower Bound: {lower_bound:.2f}')
        ax.axvline(upper_bound, color='red', linestyle='--', lw=2, label=f'Upper Bound: {upper_bound:.2f}')
        
        plt.title(f'Distribution of {column} with Outlier Bounds')
        plt.legend()
        plt.show()
        
    def plot_scatterplot_bivariate(self, x_col: str, y_col: str):
        """
        Plots a scatter plot to identify bivariate outliers (points far from the main cluster/trend).
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=self.df, x=x_col, y=y_col)
        plt.title(f'Scatter Plot: {x_col} vs {y_col} (Bivariate Outliers)')
        plt.show()

    def plot_multi_boxplots_static(self, columns: List[str]):
        """
        Plots multiple horizontal box plots for specified columns in a single static figure.
        Outliers are shown as points.
        """
        # Melt the DataFrame to long format for Seaborn compatibility
        df_long = self.df[columns].melt(var_name='Variable', value_name='Value')

        plt.figure(figsize=(12, max(4, len(columns) * 1.5))) # Dynamic figure height
        
        # Plot horizontal boxplots using Seaborn
        sns.boxplot(data=df_long, x='Value', y='Variable', orient='h', palette='Set3')
        
        plt.title('Outlier Visualization via Box Plots (Multiple Columns)')
        plt.xlabel('Value')
        plt.ylabel('Variable')
        plt.show()

    def plot_multi_boxplots_interactive(self, columns: List[str]):
        """
        Plots multiple horizontal box plots for specified columns in a single interactive figure using Plotly.
        Outliers can be hovered over.
        """
        # Melt the DataFrame to long format for Plotly compatibility
        df_long = self.df[columns].melt(var_name='Variable', value_name='Value')

        # Plotly Express automatically handles the horizontal orientation
        fig = px.box(
            df_long,
            x='Value',
            y='Variable',
            orientation='h',
            title='Interactive Outlier Visualization via Box Plots'
        )
        # Display the figure in the notebook
        fig.show()