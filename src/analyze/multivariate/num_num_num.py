from typing import List, Optional

import plotly.express as px

from .base_analyzer import BaseAnalyzer


class MultivariateAnalyzer(BaseAnalyzer):
    # ... (Keep existing functions) ...

    # --- NUM-NUM-NUM Analysis Functions ---

    def plot_3d_scatterplot(self, x_col: str, y_col: str, z_col: str, color_col: Optional[str] = None):
        """
        Plots an interactive 3D scatter plot using Plotly Express.
        Allows visualization of 3 numerical variables (x, y, z) colored by an
        optional fourth variable (color_col), which can be the target.
        """
        # The base helper uses fig.show() which renders the interactive plot in the notebook
        fig = px.scatter_3d(
            self.df,
            x=x_col,
            y=y_col,
            z=z_col,
            color=color_col, # Optional: colors points based on this column
            title=f'Interactive 3D Scatter Plot: {x_col} vs {y_col} vs {z_col}',
            opacity=0.7
        )
        self._display_plotly_dynamic(fig)

    def plot_parallel_coordinates(self, columns: List[str], color_col: Optional[str] = None):
        """
        Plots a parallel coordinates chart using Plotly to compare many numerical features
        across an optional color dimension (e.g., the target variable).
        Excellent for spotting trends across multiple dimensions simultaneously.
        """
        # Ensure the color column is passed in if selected
        plot_columns = columns.copy()
        if color_col and color_col not in plot_columns:
            plot_columns.append(color_col)

        fig = px.parallel_coordinates(
            self.df,
            columns=columns,
            color=color_col, # Optional: color the lines based on this column
            title='Interactive Parallel Coordinates Plot'
        )
        self._display_plotly_dynamic(fig)

    def calculate_partial_correlation(self, num_col1: str, num_col2: str, control_col: str):
        """
        Calculates the partial correlation between num_col1 and num_col2,
        while controlling for the effects of a third numerical variable (control_col).
        Requires pingouin library: pip install pingouin
        """
        import pingouin as pg

        # Ensure only the required numerical columns are used
        data = self.df[[num_col1, num_col2, control_col]].dropna()

        pcorr = pg.pcorr(data)

        print(f"\n--- Partial Correlation Results (Controlling for '{control_col}') ---")
        return pcorr
