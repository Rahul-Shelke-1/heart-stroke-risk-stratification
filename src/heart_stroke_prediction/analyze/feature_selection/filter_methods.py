from scipy import stats
import statsmodels.api as sm
import statistics as st
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
from .base_analyzer import BaseAnalyzer
from scipy.stats import mannwhitneyu
from sklearn.feature_selection import f_regression, f_classif, mutual_info_regression, mutual_info_classif, VarianceThreshold
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional

"""
    - VarianceThreshold: for unsupervised.
    - chi2 : non-negative features and class labels.
    - f_classif : anova f value when target is categorical.
    - f_regression : anova f value when target is numerical.
    - mutual_info_classif : Estimate mutual information for a discrete target variable. (with f_classif)
    - mutual_info_regression : Estimate mutual information for a continuous target variable. (with f_regression)
    - r_regression : Compute Pearson’s r for each features and the target.
"""

class Filter(BaseAnalyzer):

    # 1. Correlation Filter Method

    def _create_lower_triangular_mask(self, corr: pd.DataFrame, thresh:float = 40):
        # mask = np.triu(np.ones_like(corr, dtype=bool))
        mask = np.tril(np.ones_like(corr, dtype=bool))
        # shape of mask
        n = mask.shape[0]
        # Traverse the lower triangle
        for i in range(n):
            for j in range(i + 1):  # j goes from 0 to i (inclusive)
                val = np.abs(corr.iloc[i, j])
                if val > thresh and val < 100:
                    mask[i][j] = False
        return mask

    def _check_correlation(self, features: List[str], methods: List[str] = None, percent: bool = True) -> dict():
        # factor
        factor = 1
        if percent:
            factor = 100

        if methods is None:
            methods = ["pearson", "kendall", "spearman"]

        # calculating correlation
        corr = {}
        for method in methods:
            # round offing the correlation to 3 decimal places
            df_corr = np.round(self.df[features].corr(method=method) * factor, 3) # this counts fractional error
            corr[method] = df_corr

        return corr

    def plot_correlation(self, corr_dict: dict(), width:int=15, height:int=4, thresh:float = 40) -> None:
        # collect no of methods
        no_of_methods = list(corr_dict.keys())
        # collect total columns
        list_of_columns = list(corr_dict[no_of_methods[0]].columns)

        # decide we have to plot horizontally or vertically
        if len(list_of_columns) > 5: 
            # go vertical 
            fig, axes = plt.subplots(len(no_of_methods), 1, figsize=(height, width))

            # plotting all the methods
            for row_idx, method_name in enumerate(no_of_methods):
                # generate mask based on threshold
                mask = self._create_lower_triangular_mask(corr_dict[method_name], thresh)
                sns.heatmap(corr_dict[method_name], annot=True,
                            square=True, # square in plot
                            cmap='coolwarm', # color system
                            cbar_kws={"shrink": .8},
                            mask=mask, # hididng upper tiangular 
                            annot_kws={"size": 10, "color": "black"},  # Customize font size and color
                            ax=axes[row_idx])

                axes[row_idx].set_title(f"{method_name} Correlation (%) | Min threshold: {thresh}")

            plt.tight_layout()
            plt.show()        

        else: 
            # go horizontal
            fig, axes = plt.subplots(1, len(no_of_methods), figsize=(width, height))

            # plotting all the methods
            for col_idx, method_name in enumerate(no_of_methods):
                # generate mask based on threshold
                mask = self._create_lower_triangular_mask(corr_dict[method_name], thresh)
                sns.heatmap(corr_dict[method_name], annot=True, 
                            square=True, # square in plot
                            cmap='coolwarm', # color system
                            cbar_kws={"shrink": .8},
                            mask=mask, # hididng upper tiangular 
                            annot_kws={"size": 10, "color": "black"},  # Customize font size and color
                            ax=axes[col_idx])
                axes[col_idx].set_title(f"{method_name} Correlation (%)| Min threshold: {thresh}")

            plt.tight_layout()
            plt.show()    

    def plot_correlation_with_pywidget(self):
        pass

    # 2. Statistical Tests

    # normality check
    def _check_normality(self, column: str):
        """ 
        hypothesis test for normality check in continuous variable
        """
        stat, p_value = stats.shapiro(self.df[column].values)
        h_0 = "H0: data normally distributed"
        h_1 = "H1: data not normally distributed"
        result = ""
        if p_value < 0.05:
            result = "Reject null hypothesis"
        else:
            result = "Fail to reject null hypothesis"

        return {"h0":h_0, "h1":h_1,"p_val":p_value, "cc":result}
    
    # z-test - 2 category
    def _t_test_of_independence(self, x_col: str, y_col: str):
        """
        A t-test is a statistical test used to determine if there is a significant difference between 
        the means of two groups. It is commonly used when comparing the means of a numerical variable
        (dependent variable) across two categorical groups (independent variable).
        """
        h_0=f"H0: no differnce in mean's"
        h_1=f"H1: difference in mean's"
    
        # get unique categories
        categories = self.df[y_col].unique()
        # Separate numeric values by category
        group_A = self.df[self.df[y_col] == categories[0]][x_col]
        group_B = self.df[self.df[y_col] == categories[1]][x_col]

        # Perform independent t-test assuming equal variances
        t_stat, p_value = stats.ttest_ind(group_A, group_B)
        result = ""
        if np.round(p_value, 2) < 0.05:
            result = "Reject null hypothesis"
        else:
            result = "Fail to reject null hypothesis"
        return {"h0":h_0, "h1":h_1,"p_val":p_value, "cc":result}
    
    # mann whitney U test
    def _mannwhitneyu_test(self, x_col: str, y_col: str):
        """
        A t-test is a statistical test used to determine if there is a significant difference between 
        the means of two groups. It is commonly used when comparing the means of a numerical variable
        (dependent variable) across two categorical groups (independent variable).
        """
        h_0=f"H0: no differnce in mean's"
        h_1=f"H1: difference in mean's"
        categories = self.df[y_col].unique()
        # Separate numeric values by category
        group_A = self.df[self.df[y_col] == categories[0]][x_col]
        group_B = self.df[self.df[y_col] == categories[1]][x_col]

        # Perform independent t-test assuming equal variances
        u_stat, p_value = stats.mannwhitneyu(group_A, group_B, alternative='two-sided')

        result = ""
        if np.round(p_value, 2) < 0.05:
            result = "Reject null hypothesis"
        else:
            result = "Fail to reject null hypothesis"
        return {"h0":h_0, "h1":h_1,"p_val":p_value, "cc":result}
    
    # chi square goodness of fit test
    def _chisquare_test(self, x_col: str):
        """
        we compare the observed frequencies of categories within that variable 
        to the expected frequencies under a specified distribution or hypothesis
        """
        h_0="H0: observed == expected"
        h_1="H1: observed != expected"
        observed = np.array(self.df[x_col].value_counts())
        total_observed = np.sum(observed)
        expected = np.array([total_observed/self.df[x_col].nunique()] * self.df[x_col].nunique())
        # Perform chi-square goodness-of-fit test
        chi2_stat, p_value = stats.chisquare(f_obs=observed, f_exp=expected)
        result = ""
        if np.round(p_value, 2) < 0.05:
            result = "Reject null hypothesis"
        else:
            result = "Fail to reject null hypothesis"
        return {"h0":h_0, "h1":h_1,"p_val":p_value, "cc":result}

    # chi squre test of independence
    def _chisquare_independence_test(self, x_col: str, y_col: str):
        """
        To determine if there is a significant association or relationship between two categorical variables.
        """
        h_0=f"H0: no relation btween {x_col} & {y_col}" # both are independent
        h_1=f"H1: relation btween {x_col} & {y_col}" # there is a dependency
        contingency_table = pd.crosstab(self.df[x_col], self.df[y_col])
        # Perform Chi-square test of independence
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        result = ""
        if np.round(p_value, 2) < 0.05:
            result = "Reject null hypothesis"
        else:
            result = "Fail to reject null hypothesis"
        return {"h0":h_0, "h1":h_1,"p_val":p_value, "cc":result}
    
    # ANOVA test
    def _ANOVA(self, x_col: str, y_col: str):
        """
        A f-test is a statistical test used to determine if there is a significant difference between 
        the means of more than two groups. It is commonly used when comparing the means of a numerical variable
        (dependent variable) across more than two categorical groups (independent variable).
        """
        h_0=f"H0: no differnce in mean's"
        h_1=f"H1: difference in mean's"

        # Fit the model
        model = ols(f'{y_col} ~ C({x_col})', data=self.df).fit()
        
        # Perform ANOVA
        anova_table = anova_lm(model, typ=2)
        
        # Extract p-value for the categorical variable
        p_value = anova_table['PR(>F)'].iloc[0]

        result = ""
        if np.round(p_value, 2) < 0.05:
            result = "Reject null hypothesis"
        else:
            result = "Fail to reject null hypothesis"
        return {"h0":h_0, "h1":h_1, "p_val":p_value, "cc":result}
    
    # possible statstical method to filter all combination of feature and target
    def statistical_filtering(self, num_features:List[str], cat_features:List[str], target:str):
        """
        this function will filter numerical and categorical variables
        based on statstical test score if there is a significance 
        """
        # blank report 
        report_df = pd.DataFrame()

        # numrical features: int -> cat | float -> cat
        feature_names = []
        feature_type = []
        distribution_status = []
        test_performed = []
        pval = []
        is_selected = []
        for num_feature in num_features:
            DIST_STATUS = "Not Normal"
            TEST_PERFORMED = "None"
            # check normality
            norm_result = self._check_normality(num_feature)
            if norm_result["p_val"] < 0.05:
                DIST_STATUS = "Normal"
                # parametric
                test_results = self._t_test_of_independence(num_feature, target)
                TEST_PERFORMED = "t-test:2 sample"
            else:
                # non parametricsss
                test_results = self._mannwhitneyu_test(num_feature, target)
                TEST_PERFORMED = "mannwhitney"
            # collecting results
            feature_names.append(num_feature)
            feature_type.append("numerical")
            distribution_status.append(DIST_STATUS)
            test_performed.append(TEST_PERFORMED)
            pval.append(test_results["p_val"])
            if test_results["p_val"] < 0.05:
                is_selected.append("Yes")
            else:
                is_selected.append("No")

        # categorical features: binary -> cat | ordinal -> cat | nominal -> cat
        for cat_feature in cat_features:
            unique = self.df[cat_feature].nunique()
            DIST_STATUS = "Not Uniform"
            # TEST_PERFORMED = "None"

            # check uniformity
            uniform_result = self._chisquare_test(cat_feature)
            if uniform_result["p_val"] < 0.05:
                DIST_STATUS = "Uniform"
            TEST_PERFORMED = "None"
            if unique > 2:
                test_results = self._ANOVA(cat_feature, target)
                TEST_PERFORMED = "Anova test"
            else:
                test_results = self._chisquare_independence_test(cat_feature, target)
                TEST_PERFORMED = "Chi2 Test"
            # collecting results
            feature_names.append(cat_feature)
            feature_type.append("categorical")
            distribution_status.append(DIST_STATUS)
            test_performed.append(TEST_PERFORMED)
            pval.append(test_results["p_val"])
            if test_results["p_val"] < 0.05:
                is_selected.append("Yes")
            else:
                is_selected.append("No")
        # add to report
        report_df["Feature"] = feature_names
        report_df["Type"] = feature_type
        report_df["Distrbution"] = distribution_status
        report_df["Test Performed"] = test_performed
        report_df["P Value"] = pval
        report_df["Is Selected?"] = is_selected

        return report_df
    
    # 3. mutual information
    def _f_test(self, features: List[str], target: str, problem_type: str = 'classification'):
        """ 
        Compute normalized F-test scores for feature relevance.

        The F-test measures **linear dependency** between each input feature and
        the target variable. Higher scores indicate stronger linear relationships.

        For classification problems, ANOVA F-values are computed using
        `sklearn.feature_selection.f_classif`.
        For regression problems, F-values are computed using
        `sklearn.feature_selection.f_regression`.

        Parameters
        ----------
        features : List[str]
            List of feature column names used as predictors.
        target : str
            Name of the target column.
        problem_type : str, default='classification'
            Type of ML problem. Expected values:
            - 'classification' → uses ANOVA F-test
            - 'regression' → uses regression F-test

        Returns
        -------
        np.ndarray
            Normalized F-test scores for each feature, scaled to the range [0, 1].

        Notes
        -----
        - This method captures **only linear relationships** between features
        and the target.
        - Features with non-linear dependency may receive low scores.
        """
        if problem_type:
            f_test, _ = f_classif(self.df[features], self.df[target])
            f_test /= np.max(f_test)
            return f_test
        else:
            f_test, _ = f_regression(self.df[features], self.df[target])
            f_test /= np.max(f_test)
            return f_test

    def _mutual_information(self, features: List[str], target: str, problem_type: str = 'classification'):
        """
        Compute normalized mutual information scores for feature relevance.

        Mutual Information (MI) measures the **general dependency** between each
        feature and the target variable. Unlike F-tests, MI can capture
        **non-linear and non-monotonic relationships**.

        For classification problems, MI is estimated using
        `sklearn.feature_selection.mutual_info_classif`.
        For regression problems, MI is estimated using
        `sklearn.feature_selection.mutual_info_regression`.

        Parameters
        ----------
        features : List[str]
            List of feature column names used as predictors.
        target : str
            Name of the target column.
        problem_type : str, default='classification'
            Type of ML problem. Expected values:
            - 'classification' → uses mutual information for discrete targets
            - 'regression' → uses mutual information for continuous targets

        Returns
        -------
        np.ndarray
            Normalized mutual information scores for each feature, scaled to
            the range [0, 1].

        Notes
        -----
        - MI detects both linear and non-linear dependencies.
        - MI values are non-negative and do not indicate direction of effect.
        - Scores depend on entropy estimation and may vary with random state.
        """
        if problem_type:
            mi = mutual_info_classif(self.df[features], self.df[target])
            mi /= np.max(mi)
            return mi
        else:
            mi = mutual_info_regression(self.df[features], self.df[target])
            mi /= np.max(mi)
            return mi

    def mi_dataframe(
        self,
        numerical_list: List[str],
        categorical_list: List[str],
        target: str,
        problem_type: str = 'classification',
    ) -> pd.DataFrame:
        """
        Compute feature relevance scores using F-test and Mutual Information.

        This method evaluates both numerical and categorical features against
        the target variable and returns a unified DataFrame containing:
        - Feature name
        - Normalized F-test score
        - Normalized Mutual Information score
        - Binary selection flag

        Parameters
        ----------
        numerical_list : List[str]
            List of numerical feature column names.
        categorical_list : List[str]
            List of categorical feature column names.
        target : str
            Name of the target column.
        problem_type : str, default='classification'
            Type of ML problem ('classification' or 'regression').

        Returns
        -------
        pd.DataFrame
            DataFrame with columns:
            - 'feature'
            - 'f_test_score'
            - 'mi_score'
            - 'Is-selected ?'
        """
        # plt.style.use('dark_background')

        features = numerical_list + categorical_list

        # Compute scores
        f_scores = self._f_test(
            features=features,
            target=target,
            problem_type=problem_type
        )

        mi_scores = self._mutual_information(
            features=features,
            target=target,
            problem_type=problem_type
        )

        # Build DataFrame
        df_scores = pd.DataFrame({
            "feature": features,
            "f_test_score": f_scores,
            "mi_score": mi_scores
        })

        # Selection rule (can be replaced with threshold / top-k logic)
        df_scores["Is_selected?"] = np.where(
            (df_scores["f_test_score"] > 0) | (df_scores["mi_score"] > 0),
            "yes",
            "no"
        )

        return df_scores


    def visualize_mi_with_pywidget(
        self,
        numerical_list: List[str],
        categorical_list: List[str],
        target: str,
        width: int = 900,  # Plotly uses pixels
        height: int = 500
    ) -> None:
        import ipywidgets as widgets
        from IPython.display import display
        import plotly.express as px
        import plotly.graph_objects as go

        features = numerical_list + categorical_list

        f_scores = self._f_test(features=features, target=target, problem_type='classification')
        mi_scores = self._mutual_information(features=features, target=target, problem_type='classification')

        output_widgets = []

        for i, feature in enumerate(features):
            f_val = f_scores[i]
            f_str = f"{f_val:.4f}" if not np.isnan(f_val) else "N/A (Constant Feature)"

            # Create the interactive Plotly figure
            fig = px.scatter(
                self.df, 
                x=feature, 
                y=target,
                title=f"F-test = {f_str}, MI = {mi_scores[i]:.4f}",
                # template="plotly_dark", # Native dark mode
                color_discrete_sequence=["#d10e00"] # Neon teal
            )
            
            fig.update_layout(
                autosize=True,
                height=500, # Fixed height usually feels better in tabs
                # template="plotly_dark"
            )
            
            # Convert Figure to a Widget so it renders perfectly in Tabs
            fw = go.FigureWidget(fig)
            output_widgets.append(fw)

        # Create tabs
        tabs = widgets.Tab(children=output_widgets)
        
        for idx, feature in enumerate(features):
            tabs.set_title(idx, feature)

        display(tabs)

    # 4. variance threshold
    def variance_threshold(
            self,
            feature_list: List[str],
            data: pd.DataFrame = None,
            threshold: float = 0.0,
            )-> pd.DataFrame:
        """
        Compute feature importance based on Variance.

        This method identifies features with low variability. Features with zero 
        variance (constant values) provide no predictive power for any model.

        Parameters
        ----------
        feature_list : List[str]
            List of numerical feature column names.
        data: pd.DataFrame
            Data where categories also converted to numbers.
        threshold : float, default=0.0
            Features with variance lower than this threshold will be marked 'no'.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns:
            - 'feature'
            - 'variance'
            - 'std_dev' (Standard Deviation)
            - 'Is_selected?'
        """
        # Ensure we only process numerical features available in the DF
        if isinstance(data, pd.DataFrame):
            df_num = data[feature_list]
        else:   
            df_num = self.df[feature_list]

        # Initialize the selector
        selector = VarianceThreshold(threshold=threshold)
        
        # Fit to learn variances
        selector.fit(df_num)

        # Get variances directly from the selector
        variances = selector.variances_
        
        # Identify which features passed the threshold
        selection_mask = selector.get_support()

        # Build the resulting DataFrame
        df_variance = pd.DataFrame({
            "feature": feature_list,
            "variance": variances,
            "std_dev": np.sqrt(variances)
        })

        # Apply the selection flag
        df_variance["Is_selected?"] = np.where(
            selection_mask,
            "yes",
            "no"
        )

        # Sort by variance descending for better visibility
        return df_variance.sort_values(by="variance", ascending=False).reset_index(drop=True)