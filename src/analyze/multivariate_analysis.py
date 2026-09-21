from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.inspection import \
    PartialDependenceDisplay  # Added for visualization
from sklearn.inspection import partial_dependence
from sklearn.linear_model import \
    LogisticRegression  # Added Logistic Regression
from sklearn.preprocessing import LabelEncoder
from statsmodels.stats.outliers_influence import variance_inflation_factor


class MultivariateAnalyzer:

    def __init__(self, df: pd.DataFrame, columns: List[str], target: str):
        self.df = df
        self.columns = columns
        self.target_col = target
        self.trained_model = None
        self.feature_names = None # old + new after processing categories
        self.processed_df = None # data with encoded columns

    def _process_data(self, data: pd.DataFrame):
        # Handle categorical features within the model scope (RF handles some, but one-hot is cleaner)
        # We need a robust way to encode all features before running the model
        data_encoded = pd.get_dummies(data, drop_first=True)

        # Ensure target variable is handled correctly in the encoded DF
        if self.target_col + '_1' in data_encoded.columns: # for binary categorical targets
             y = data_encoded[self.target_col + '_1']
             X = data_encoded.drop(columns=[self.target_col + '_1', self.target_col + '_0'], errors='ignore')
        else: # for numerical targets or already numeric binary targets
             y = data_encoded[self.target_col]
             X = data_encoded.drop(columns=[self.target_col], errors='ignore')

        return X, y

    def get_feature_importance(self, target_col: str = None, feature_cols: Optional[List[str]] = None, model_type: str = 'logistic_regression', n_exp: int = 10):
        """
        Trains a simple Random Forest model to determine and plot the importance of features
        in predicting the target variable.
        """
        # Select all columns if none specified
        if target_col:
            self.target_col = target_col

        if feature_cols:
            self.columns

        data = self.df[self.columns + [self.target_col]]

        X, y = self._process_data(data)

        self.processed_df = X.copy()

        importances = []
        rng = np.random.default_rng()

        for _ in range(n_exp):

            seed = rng.integers(0, 10_000)

            # Choose model based on input
            if model_type.lower() == 'logistic_regression':
                model = LogisticRegression(random_state=seed, solver='liblinear')
            elif model_type.lower() == 'random_forest_clf':
                model = RandomForestClassifier(n_estimators=100, random_state=seed)
            elif model_type.lower() == 'random_forest_reg':
                model = RandomForestRegressor(n_estimators=100, random_state=seed)
            else:
                print("Invalid model_type. Use 'classification' or 'regression'.")
                return

            model.fit(X, y)

            # Extract importance metric appropriate for the model type
            if model_type.lower() == 'logistic_regression':
                # Use absolute value of coefficients as a simple measure of importance magnitude
                # If multi-class, take mean absolute coef across classes
                coefs = model.coef_
                if coefs.ndim > 1:
                   importances.append(np.mean(coefs, axis=0))
                else:
                   importances.append(coefs)
            else:
                # Use standard feature_importances_ for tree models
                importances.append(model.feature_importances_)

        self.feature_names = X.columns

        importance_df = pd.DataFrame({'Feature': self.feature_names,
                                      'Importance(mean)': np.mean(importances, axis=0) ,
                                      'Importance(std)': np.std(importances, axis=0)})
        importance_df = importance_df.sort_values(by='Importance(mean)', ascending=False)

        return importance_df

    def plot_errorbar(self, importance_df: pd.DataFrame):
        plt.figure(figsize=(10, len(importance_df) * 0.3 + 2))

        ax = sns.barplot(
            x='Importance(mean)',
            y='Feature',
            data=importance_df,
            errorbar=None
        )

        # Add error bars manually
        ax.errorbar(
            x=importance_df['Importance(mean)'],
            y=range(len(importance_df)),
            xerr=importance_df['Importance(std)'],
            fmt='none',
            c='black',
            capsize=3
        )

        plt.title(f'Feature Importance for predicting "{self.target_col}"')
        plt.tight_layout()
        plt.show()

    def plot_barplot(self, importance_df: pd.DataFrame):
        plt.figure(figsize=(10, len(importance_df) * 0.3 + 2))

        plt.barh(
            importance_df['Feature'],
            importance_df['Importance(mean)'],
            xerr=importance_df['Importance(std)'],
            capsize=3
        )

        plt.gca().invert_yaxis()  # highest importance on top
        plt.xlabel('Feature Importance (mean ± std)')
        plt.title(f'Feature Importance for predicting "{self.target_col}"')

        plt.tight_layout()
        plt.show()

    def plot_3d_scatterplot(self, x_col: str, y_col: str, z_col: str, color_col: str = None):
        """
        Plots an interactive 3D scatter plot using Plotly Express.
        Allows visualization of 3 numerical variables (x, y, z) colored by a
        fourth variable (color_col), which can be numerical or categorical (the target).
        """
        fig = px.scatter_3d(
            self.df,
            x=x_col,
            y=y_col,
            z=z_col,
            color=color_col, # Use the target variable for color coding
            title=f'Interactive 3D Scatter Plot: {x_col} vs {y_col} vs {z_col} (Colored by {color_col})',
            opacity=0.2 # Add some transparency to see overlapping points
        )

        # You can add hover data for more details on each point
        # fig.update_traces(marker=dict(size=5), selector=dict(mode='markers'))

        # Display the figure in the notebook using the base helper
        fig.show()

    def calculate_vif(self, feature_cols: Optional[List[str]] = None):
        """
        Calculates Variance Inflation Factor (VIF) for the given feature columns
        to detect multicollinearity.

        Returns a DataFrame with VIF values.
        """
        # Select features
        X = self.df[feature_cols] if feature_cols else self.df.copy()

        # Encode categorical variables
        X_encoded = pd.get_dummies(X, drop_first=True)

        # Drop rows with missing values (VIF cannot handle NaNs)
        X_encoded = X_encoded.dropna()

        # Add small constant to avoid division by zero issues
        X_encoded = X_encoded.astype(float)

        vif_data = pd.DataFrame()
        vif_data["Feature"] = X_encoded.columns
        vif_data["VIF"] = [
            variance_inflation_factor(X_encoded.values, i)
            for i in range(X_encoded.shape[1])
        ]

        vif_data = vif_data.sort_values(by="VIF", ascending=False)

        return vif_data

    def prune_correlated_features(self, feature_cols: Optional[List[str]] = None, threshold: float = 0.9, target_col: Optional[str] = None) -> List[str]:
        """
        Performs correlation pruning on features.

        Identifies highly correlated features and returns a list of features to keep.
        If a target_col is provided, it prioritizes keeping the feature more correlated
        with the target variable.

        Args:
            feature_cols: List of columns to check for correlation. If None, uses all columns in the DataFrame.
            threshold: The correlation threshold (absolute value) above which features are considered redundant.
            target_col: The name of the target variable column. If provided, helps decide which feature to keep.

        Returns:
            A list of feature names to keep.
        """
        data_subset = self.df[feature_cols] if feature_cols else self.df.copy()

        # We use get_dummies to handle potential categorical data before calculating correlations
        data_encoded = pd.get_dummies(data_subset, drop_first=True)
        corr_matrix = data_encoded.corr().abs()

        # Select upper triangle of correlation matrix
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

        # Find index of feature columns with correlation greater than threshold
        to_drop = set()

        if target_col:
            # If target provided, we use correlation to target to decide which of the pair to keep
            if target_col not in self.df.columns:
                 raise ValueError(f"Target column '{target_col}' not found in the original DataFrame.")

            # Combine target into encoded data temporarily to calculate correlations properly
            target_series = self.df[target_col]
            if target_series.dtype == 'object' or target_series.dtype.name == 'category':
                le = LabelEncoder()
                target_series = pd.Series(le.fit_transform(target_series), index=target_series.index, name=target_col)

            # Make sure indices align if the data was filtered
            target_series = target_series.loc[data_encoded.index]

            # Use correlation with target to decide which correlated feature to drop
            for col in upper.columns:
                if col not in to_drop:
                    # Find all highly correlated partners for the current column
                    correlated_partners = list(upper.index[upper[col] > threshold])
                    if correlated_partners:
                        # Calculate correlation of current col and its partners with the target
                        corr_with_target_col = data_encoded[col].corr(target_series)

                        for partner_col in correlated_partners:
                            if partner_col not in to_drop:
                                corr_with_target_partner = data_encoded[partner_col].corr(target_series)

                                # Drop the one with lower absolute correlation to the target
                                if abs(corr_with_target_partner) < abs(corr_with_target_col):
                                    to_drop.add(partner_col)
                                else:
                                    to_drop.add(col) # This might add the current col, breaking the outer loop logic, but the set logic handles it

        else:
            # Standard method: simply drop one of the pair arbitrarily
            for column in upper.columns:
                if any(upper[column] > threshold):
                    # Get the list of features to drop from this column comparison
                    features_to_drop_from_pair = list(upper.index[upper[column] > threshold])
                    # Add them to the set of columns to drop
                    for feature in features_to_drop_from_pair:
                        if feature not in to_drop: # Ensure we don't drop something already decided to keep
                            to_drop.add(feature)

        # Get the features to keep
        features_to_keep = [col for col in data_encoded.columns if col not in to_drop]

        print(f"Original feature count (after encoding): {data_encoded.shape[1]}")
        print(f"Features identified for dropping due to correlation > {threshold}: {to_drop}")
        print(f"Features to keep: {len(features_to_keep)}")

        return features_to_keep

    def plot_correlation_matrix(self, feature_cols: Optional[List[str]] = None):
        """
        Plots a Seaborn heatmap of the correlation matrix for the specified features.
        Handles one-hot encoding internally for categorical features.
        """
        data_subset = self.df[feature_cols] if feature_cols else self.df.copy()
        data_encoded = pd.get_dummies(data_subset, drop_first=True)

        # Calculate the correlation matrix
        corr_matrix = data_encoded.corr()

        # Plotting the heatmap
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=.5)
        plt.title('Correlation Matrix of Features')
        plt.show()

    def train_model(self, model_name: str = None):
        """
        Trains a specified model (Logistic Regression or Random Forest) and stores it internally.
        Handles data encoding to ensure X is dummy-encoded and y is 1D.
        """
        data = self.df[self.columns + [self.target_col]]

        X, y = self._process_data(data)

        if self.feature_names is None:
            self.feature_names = list(X.columns)

        if model_name.lower() == 'logistic_regression':
            self.trained_model = LogisticRegression(random_state=42, solver='liblinear')
            print("Training Logistic Regression Model...")
        elif model_name.lower() == 'random_forest_clf':
            self.trained_model = RandomForestClassifier(n_estimators=100, random_state=42)
            print("Training Random Forest Classifier Model...")
        elif model_name.lower() == 'random_forest_reg':
             self.trained_model = RandomForestRegressor(n_estimators=100, random_state=42)
             print("Training Random Forest Regressor Model...")
        else:
            raise ValueError(f"Unknown model name: {model_name}. Use 'logistic_regression', 'random_forest_clf', or 'random_forest_reg'.")

        self.trained_model.fit(X, y)
        print(f"Model trained successfully on {len(self.feature_names)} features.")
        return self.trained_model, self.feature_names

    def visualize_partial_dependence(self, features_to_plot: Optional[List[str]] = None, n_cols: int = 3):
        """
        Visualizes how specified features independently affect the prediction of the
        currently trained model using Partial Dependence Plots (PDPs).

        Requires `self.trained_model` to be fitted first using `train_model()`.
        """
        data = self.df[self.columns + [self.target_col]]
        X, _ = self._process_data(data)
        X = X[self.feature_names]

        # Calculate rows based on number of features
        n_features = len(self.feature_names)
        n_rows = (n_features // n_cols) + (1 if n_features % n_cols > 0 else 0)

        print(f"Generating Partial Dependence Plots for {len(self.feature_names)} features...")

        # Plotting the partial dependence
        fig, ax = plt.subplots(figsize=(15, 10))
        # fig, ax = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 4), squeeze=False)
        display = PartialDependenceDisplay.from_estimator(
            self.trained_model,
            X,
            self.feature_names,
            feature_names=self.feature_names,
            ax=ax,
            grid_resolution=100,
            kind='both',
            centered=True,
            n_cols=n_cols, # Control the grid width
            ice_lines_kw={'color': 'black', 'alpha': 0.1},
            pd_line_kw={"color": "red", "lw": 3, "linestyle": "--"},
            target=0 # Explicitly pass the target index if binary
        )
        # Adjust the resulting figure
        display.figure_.set_size_inches(n_cols * 4, n_rows * 3)
        display.figure_.suptitle(f"Partial Dependence Plots for {type(self.trained_model).__name__}", fontsize=16)
        plt.subplots_adjust(top=0.9, hspace=0.3)
        plt.show()

    def visualize_ice(self, features_to_plot: Optional[List[str]] = None):
        """
        Visualizes how specified features independently affect the prediction of the
        currently trained model using Partial Dependence Plots (ICE plots).

        Requires `self.trained_model` to be fitted first using `train_model()`.
        """
        data = self.df[self.columns + [self.target_col]]
        X, _ = self._process_data(data)

        # We must ensure X only contains the features the model was trained on
        X = X[self.feature_names]

        print(f"Shape: {X.shape}")

        print(f"Generating Partial Dependence Plots for {len(self.feature_names)} features...")

        # Plotting the partial dependence
        fig, ax = plt.subplots(figsize=(15, 10))
        display = PartialDependenceDisplay.from_estimator(
            self.trained_model,
            X,
            self.feature_names,
            # feature_names=self.feature_names,
            ax=ax,
            grid_resolution=100,
            kind='both',
            centered=True,
            target=1 # Explicitly pass the target index if binary
        )
        plt.suptitle(f"Partial Dependence Plots for {type(self.trained_model).__name__}")
        plt.subplots_adjust(top=0.9)
        plt.show()

    def visualize_grouped_ice(
        self,
        features_to_plot: Optional[List[str]] = None,
        n_cols: int = 3,
        group_feature: str = 'car_type', # Pass your target column name here
        colors: List[str] = ['tab:blue', 'tab:red', 'tab:green'],
        labels: List[str] = ['normal', 'classic'],
        alpha: float = 0.1
    ):
        # 1. Setup data - X must only contain features the model was trained on
        data = self.df[self.columns + [self.target_col]]
        X_processed, _ = self._process_data(data)
        X_subset = X_processed[self.feature_names]

        features = features_to_plot if features_to_plot else self.feature_names
        n_features = len(features)
        n_rows = (n_features // n_cols) + (1 if n_features % n_cols > 0 else 0)

        # 2. FIX: Access the group feature from the original self.df to avoid KeyError
        # This allows you to use the target column for coloring
        group_values = self.df[group_feature].values

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 4), squeeze=False)
        axes = axes.flatten()

        for i, feature in enumerate(features):
            ax = axes[i]

            # Calculate PD/ICE
            results = partial_dependence(
                self.trained_model, X_subset, [feature],
                grid_resolution=100, kind='both'
            )

            grid_values = results['grid_values'][0]
            ice_lines = results['individual'][0] # Shape (n_samples, grid_points) for 2025 scikit-learn

            # Centering logic
            centered_ice = ice_lines - ice_lines[:, 0][:, np.newaxis]

            # Plot ICE lines
            for idx in range(len(centered_ice)):
                # Handle non-integer categories by mapping them to indices
                val = group_values[idx]
                # Simple mapping if group_values are labels; otherwise use as int index
                g_idx = labels.index(val) if val in labels else int(val)
                color = colors[g_idx % len(colors)]

                ax.plot(grid_values, centered_ice[idx], color=color, alpha=alpha, linewidth=0.8)

            # Plot Average (PDP) line
            avg_line = results['average'][0]
            centered_avg = avg_line - avg_line[0]
            ax.plot(grid_values, centered_avg, color='red', linestyle='--', linewidth=2.5, zorder=10)

            ax.set_title(f'Effect of {feature}')
            ax.set_xlabel(feature)
            if i % n_cols == 0: ax.set_ylabel('Partial Dep. (Centered)')

        # Cleanup and Legend
        for j in range(i + 1, len(axes)): fig.delaxes(axes[j])

        legend_handles = [plt.Line2D([0], [0], color=colors[k % len(colors)], label=labels[k]) for k in range(len(labels))]
        fig.legend(handles=legend_handles, loc='upper center', bbox_to_anchor=(0.5, 1.02), ncol=len(labels), title=group_feature)

        plt.tight_layout()
        plt.show()
