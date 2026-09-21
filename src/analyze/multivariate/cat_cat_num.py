from typing import List, Optional

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

from .base_analyzer import BaseAnalyzer


class CatCatNumAnalyzer(BaseAnalyzer):
    # ... (Keep existing functions: plot_feature_importance, plot_3d_scatterplot, etc.) ...

    # --- CAT-CAT-NUM Analysis Functions ---

    def create_mean_pivot_table(self, cat_col1: str, cat_col2: str, num_col: str) -> pd.DataFrame:
        """
        Creates a pivot table showing the mean of the numerical variable
        across the intersections of the two categorical variables.
        """
        pivot_table = self.df.pivot_table(
            values=num_col,
            index=cat_col1,
            columns=cat_col2,
            aggfunc='mean'
        ).round(2)
        print(f"\n--- Mean of '{num_col}' by '{cat_col1}' and '{cat_col2}' ---")
        return pivot_table

    def plot_interaction_boxplot(self, cat_col1: str, cat_col2: str, num_col: str):
        """
        Uses nested box plots to visualize the distribution of the numerical variable
        across all combinations of the two categories.
        """
        plt.figure(figsize=(12, 7))
        # This groups the 'x' variable by the 'hue' variable automatically
        sns.boxplot(data=self.df, x=cat_col1, y=num_col, hue=cat_col2)
        plt.title(f'Interaction Plot: Distribution of {num_col} by {cat_col1} and {cat_col2}')
        plt.legend(title=cat_col2, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()

    def plot_interaction_lineplot(self, cat_col1: str, cat_col2: str, num_col: str):
        """
        Plots the mean of the numerical variable using a line plot to easily see
        interaction effects (non-parallel lines indicate interaction).
        """
        plt.figure(figsize=(10, 6))
        # Uses mean as default estimator with confidence intervals
        sns.pointplot(data=self.df, x=cat_col1, y=num_col, hue=cat_col2, dodge=True, errorbar='sd')
        plt.title(f'Interaction Plot: Mean of {num_col} by {cat_col1} and {cat_col2}')
        plt.legend(title=cat_col2)
        plt.ylabel(f'Mean {num_col}')
        plt.show()

    def perform_two_way_anova(self, cat_col1: str, cat_col2: str, num_col: str):
        """
        Performs a two-way ANOVA test to statistically determine if there are main effects
        and an interaction effect between the two categorical variables on the numerical variable.
        Requires statsmodels: pip install statsmodels patsy
        """
        # Create a formula for the OLS model: Num ~ Cat1 + Cat2 + Cat1:Cat2 (interaction term)
        formula = f'{num_col} ~ C({cat_col1}) + C({cat_col2}) + C({cat_col1}):C({cat_col2})'
        model = ols(formula, data=self.df).fit()
        anova_table = anova_lm(model, typ=2) # Type 2 ANOVA table

        print(f"\n--- Two-Way ANOVA Results for {num_col} ---")
        print(f"Independent Variables: {cat_col1}, {cat_col2}")
        # The P-values for each effect will indicate significance
        return anova_table

    def _get_feature_importance_data(self, target_col: str, feature_cols: Optional[List[str]] = None, model_type: str = 'classification') -> pd.DataFrame:
        """
        Helper that runs a Random Forest model internally to get the feature importance DataFrame.
        """
        data = self.df[feature_cols + [target_col]] if feature_cols else self.df.copy()
        data_encoded = pd.get_dummies(data, drop_first=True)

        # Ensure target variable is handled correctly in the encoded DF
        y = data_encoded[target_col] if target_col in data_encoded.columns else data_encoded.iloc[:, -1]
        X = data_encoded.drop(columns=[c for c in data_encoded.columns if c.startswith(f'{target_col}_') or c == target_col], errors='ignore')

        if model_type == 'classification':
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == 'regression':
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            return pd.DataFrame()

        model.fit(X, y)
        importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_})
        return importance_df.sort_values(by='Importance', ascending=False).reset_index(drop=True)


    def plot_multivariate_summary_composite(self, cat_col1_target: str, cat_col2: str, num_col: str):
        """
        Generates a single figure with 3 plots:
        1. Top (2 columns wide): Interaction Box plot (CAT1 x NUM, Hue=CAT2)
        2. Bottom Left: Interaction Line plot (CAT1 x NUM, Hue=CAT2)
        3. Bottom Right: Feature Importance Bar plot (Predicting CAT1 using CAT2 and NUM)

        Note: cat_col1_target is treated as the target variable for the importance plot.
        """
        fig = plt.figure(figsize=(15, 8))
        gs = gridspec.GridSpec(2, 2, height_ratios=[1.5, 1])

        # --- Plot 1: Interaction Box plot (Top, spans 2 columns) ---
        ax1 = fig.add_subplot(gs[0, :])
        sns.boxplot(data=self.df, x=cat_col1_target, y=num_col, hue=cat_col2, ax=ax1)
        ax1.set_title(f'1. Distribution of {num_col} by {cat_col1_target} and {cat_col2}')
        ax1.legend(title=cat_col2, bbox_to_anchor=(1.05, 1), loc='upper left')

        # --- Plot 2: Interaction Line plot (Bottom Left) ---
        ax2 = fig.add_subplot(gs[1, 0])
        sns.pointplot(data=self.df, x=cat_col1_target, y=num_col, hue=cat_col2, dodge=True, errorbar='sd', ax=ax2)
        ax2.set_title('2. Mean Interaction Plot')
        ax2.set_ylabel(f'Mean {num_col}')
        ax2.legend().remove()

        # --- Plot 3: Feature Importance (Bottom Right) ---
        ax3 = fig.add_subplot(gs[1, 1])

        # Pass the correct variables to the helper function:
        importance_df = self._get_feature_importance_data(
            target_col=cat_col1_target,
            feature_cols=[cat_col2, num_col],
            model_type='classification' # Since cat_col1 is usually a classification target
        )
        sns.barplot(x='Importance', y='Feature', data=importance_df.head(10), ax=ax3)
        ax3.set_title(f'3. Feature Importance for predicting "{cat_col1_target}"')

        plt.tight_layout(rect=[0, 0, 0.95, 1])
        plt.show()
