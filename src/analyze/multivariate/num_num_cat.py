
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .base_analyzer import BaseAnalyzer


class MultivariateAnalyzer(BaseAnalyzer):
    # ... (Keep existing functions) ...

    # --- NUM-NUM-CAT Analysis Functions ---

    def create_correlation_pivot_table(self, num_col1: str, num_col2: str, cat_col: str) -> pd.DataFrame:
        """
        Calculates and displays the correlation coefficient between two numerical columns,
        separately for each category of the third variable.
        """
        # Group by the category and apply the correlation function
        def corr_func(x):
            return x[num_col1].corr(x[num_col2])

        correlation_by_group = self.df.groupby(cat_col).apply(corr_func).rename('Correlation').round(4)

        print(f"\n--- Pearson Correlation between '{num_col1}' and '{num_col2}' grouped by '{cat_col}' ---")
        return pd.DataFrame(correlation_by_group)

    def plot_faceted_scatterplots(self, x_col: str, y_col: str, facet_col: str):
        """
        Plots scatter plots of two numerical variables, repeated in a grid for
        each level of the categorical variable. Includes a regression line for visual guidance.
        """
        # Seaborn FacetGrid is perfect for this visualization
        g = sns.FacetGrid(
            self.df,
            col=facet_col,
            height=5,
            aspect=1 # Ensure aspect ratio is nice
        )
        # Map a regression plot onto each facet
        g.map(sns.regplot, x_col, y_col, color='skyblue', line_kws={'color': 'red', 'lw': 2})

        g.fig.suptitle(f'Scatter Plot of {y_col} vs {x_col} Conditioned on {facet_col}', y=1.05)
        plt.show()

    def plot_3d_interactive_with_color(self, x_col: str, y_col: str, z_col: str, color_col: str):
        """
        Uses Plotly 3D scatter plot (already defined, but emphasizing its use here)
        to visualize three numerical variables, colored by the category.
        """
        # This function definition already exists in your file structure
        self.plot_3d_scatterplot(x_col, y_col, z_col, color_col)

