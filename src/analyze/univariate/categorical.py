import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import chisquare

from .base_analyzer import BaseAnalyzer


class CategoricalUnivariate(BaseAnalyzer):
    """Methods for analyzing a single categorical column."""

    # --- Descriptive Analysis ---
    def value_counts_table(self, column: str, normalize=False) -> pd.Series:
        """Returns frequency or proportion table."""
        return self.df[column].value_counts(normalize=normalize)

    # --- Visual Analysis
    def plot_counts(self, column: str):
        self._plot_static(sns.countplot, data=self.df, x=column)

    def plot_categorical_summary(self, df: pd.DataFrame, column: str):
        """
        this function is here to plot countplot and pie chart for categories
        """
        fig, axs = plt.subplots(1, 2, figsize=(10, 4))
        df_dict=self.chi2_goodness_of_fit_test(df, column)
        df_hypo_title = "{}\n{}\np-value:{} alpha: 0.05\n Result: {}".format(df_dict["h0"],
                                                                            df_dict["h1"],
                                                                            df_dict["p_val"],
                                                                            df_dict["cc"])
        fig.suptitle(df_hypo_title)

        # Calculate subtotals per category
        subtotals = df.groupby(column, sort=False).size().reset_index(name='Subtotal')
        subtotals = subtotals.sort_values(by='Subtotal') # sorting values, but not index
        subtotals = subtotals.reset_index(drop=True) # sorting index

        # add expected horizontal line in count plot
        y = df[column].shape[0]/df[column].nunique()
        axs[0].axhline(y=y, color='red', linestyle='--', label='expected')

        # count plot: observed vs expected
        sns.countplot(data=df, x=column, ax=axs[0], order=subtotals[column], hue_order=subtotals[column])

        axs[0].legend()
        # Add subtotals as annotations
        for index, row in subtotals.iterrows():
            axs[0].text(index, row['Subtotal'] + 1, row['Subtotal'], ha='center', va='bottom', fontsize=10)
        # pie chart
        df[column].value_counts(ascending=True).plot(kind="pie", autopct="%.2f", ax=axs[1])
        plt.tight_layout()
        plt.show()

    # --- Inferential Analysis ---
    def chi2_goodness_of_fit_test(self, df: pd.DataFrame, column: str):
        """
        we compare the observed frequencies of categories within that variable
        to the expected frequencies under a specified distribution or hypothesis.
        in short:
        - Observed = What you got (from your sample).
        - Expected = What you should have gotten (if the null hypothesis were true).

        Example:
        If you roll a die 60 times (sample), and you're testing if the die is fair (population assumption),
        you'd expect each face to appear 10 times (expected). You compare that to what you actually observed — that's the essence of the test.
        """
        h_0="H0: observed == expected"
        h_1="H1: observed != expected"
        observed = np.array(df[column].value_counts())
        total_observed = np.sum(observed)
        expected = np.array([total_observed/df[column].nunique()] * df[column].nunique())
        # Perform chi-square goodness-of-fit test
        chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
        result = ""
        if np.round(p_value, 2) < 0.05:
            result = "Reject null hypothesis"
        else:
            result = "Fail to reject null hypothesis"
        return {"h0":h_0, "h1":h_1,"p_val":np.round(p_value,3), "cc":result}

    def bootstrap_expected_distribution(self, df: pd.DataFrame, column: str, n_iterations:int =1000):
        value_counts_list = []
        for _ in range(n_iterations):
            sample = df[column].sample(frac=0.5, replace=True)
            counts = sample.value_counts(normalize=True)  # Get proportion
            value_counts_list.append(counts)

        # Combine all bootstrapped proportions and average them
        bootstrapped_df = pd.DataFrame(value_counts_list).fillna(0)
        expected_distribution = bootstrapped_df.mean()

        return expected_distribution
