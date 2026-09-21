
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import \
    glm  # Generalized Linear Model for log-linear

from .base_analyzer import BaseAnalyzer


class MultivariateAnalyzer(BaseAnalyzer):
    # ... (Keep existing functions: plot_feature_importance, plot_3d_scatterplot, etc.) ...

    # --- CAT-CAT-CAT Analysis Functions ---

    def create_three_way_contingency_table(self, col1: str, col2: str, col3: str, normalize: str = None) -> pd.DataFrame:
        """
        Creates a 3-way contingency table, potentially normalized.
        Normalization options: 'all' (total %), 'index' (row %), 'columns' (column %).
        """
        # pd.crosstab can only handle two variables in index/columns directly.
        # For full 3-way, groupby is cleaner for outputting a multi-index Series/DF.
        if normalize is None:
             table = self.df.groupby([col1, col2, col3], observed=True).size().unstack(fill_value=0)
        else:
             # This requires more complex calculation to normalize correctly for 3 dimensions
             total_count = len(self.df)
             table = self.df.groupby([col1, col2, col3], observed=True).size().div(total_count).unstack(fill_value=0) * 100
             print("Note: Table normalized by total count of observations.")

        print(f"\n--- 3-Way Contingency Table ({col1} vs {col2} conditioned on {col3}) ---")
        return table


    def plot_faceted_bar_plots(self, x_col: str, hue_col: str, facet_col: str):
        """
        Uses Seaborn FacetGrid (catplot) to visualize the interaction:
        x_col vs hue_col, repeated for each level of facet_col.
        """
        # Seaborn's catplot handles this complex layout nicely
        g = sns.catplot(
            data=self.df,
            kind="count",
            x=x_col,
            hue=hue_col,
            col=facet_col, # This creates separate panels for each category
            height=5,
            aspect=0.8,
            sharey=True # Share the Y axis scale
        )
        g.fig.suptitle(f'Frequency of {x_col} and {hue_col} Conditioned on {facet_col}', y=1.05)
        g.set_axis_labels(x_col, "Count")
        g.add_legend(title=hue_col)
        plt.show()

        # For guidance on how Seaborn catplots can visualize multiple categorical variables effectively:
# <layout>video(introSentence="For guidance on how Seaborn catplots can visualize multiple categorical variables effectively:", results=["1.2.11"])</layout>

    def perform_log_linear_analysis(self, col1: str, col2: str, col3: str):
        """
        Performs a Log-Linear Model analysis to test for three-way interactions
        between all categorical variables.
        Requires statsmodels and patsy: pip install statsmodels patsy
        """
        # The test requires a specific input format: a frequency table
        data_table = pd.crosstab(index=self.df[col1], columns=[self.df[col2], self.df[col3]])

        # Create a formula for the full interaction model
        formula = f'C({col1}) + C({col2}) + C({col3}) + C({col1}):C({col2}) + C({col1}):C({col3}) + C({col2}):C({col3}) + C({col1}):C({col2}):C({col3})'

        # GLM with Poisson assumes log-linear model form
        model = glm(formula=formula, data=self.df, family=sm.families.Poisson()).fit()

        print("\n--- Log-Linear Model Summary (Tests for 3-way interactions) ---")
        # Display the full summary for detailed p-values
        return model.summary()
