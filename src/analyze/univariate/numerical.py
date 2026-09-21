import statistics as st

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from scipy import stats
from scipy.stats import ttest_1samp

from .base_analyzer import BaseAnalyzer


class NumericalUnivariate(BaseAnalyzer):
    """Methods for analyzing a single numerical column."""

    # --- Descriptive Analysis ---
    def summary_table(self, column: str) -> pd.Series:
        """Returns key descriptive stats."""
        return self.df[column].describe()

    def get_skew_kurtosis(self, column: str):
        return {
            'skew': self.df[column].skew(),
            'kurtosis': self.df[column].kurtosis()
        }

    def plot_histogram(self, column: str):
        """
        Plots histogram to see distribution of data
        with mean, median, mode
        """
        sns.histplot(data=self.df, x=column, kde=True, alpha=0.25, line_kws={'linewidth': 3})
        # measure of central tendency
        mean_max = np.round(st.mean(self.df[column]), 2)
        median_max = np.round(st.median(self.df[column]), 2)
        mode_max = np.round(st.mode(self.df[column]), 2)
        plt.title(f"Mean: {mean_max} | Median: {median_max} | Mode: {mode_max}")
        plt.axvline(ymin=0,ymax=mode_max,x=self.df[column].mean(), color="red",label="Mean")
        plt.axvline(ymin=0,ymax=mode_max,x=self.df[column].median(), color="green",label="Median")
        plt.xlabel(column)
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_qq(self, column: str):
        """
        Plots QQ plot to visually chech normal distribution
        """
        sm.qqplot(self.df[column], line='45')
        plt.title("Q-Q Plot")

    def plot_horizontal_boxplot(self, column: str):
        """
        Plots horizontal box plot
        """
        plt.boxplot(self.df[column], vert=False, patch_artist=True,
        boxprops=dict(facecolor='lightblue', color='blue'),
        whiskerprops=dict(color='blue'),
        capprops=dict(color='blue'),
        # meanprops=dict(color='red'),
        medianprops=dict(color='green'))
        plt.xlabel('Value')
        plt.title('Horizontal Box Plot')
        plt.grid(True)
        plt.show()

    def plot_ci(self, column: str):
        """
        Plots confidence interval
        """
        # Compute mean and standard error of the mean
        mean = np.mean(self.df[column])
        sem = stats.sem(self.df[column])
        # Compute 95% confidence interval
        confidence = 0.95
        ci = stats.t.interval(confidence, len(self.df)-1, loc=mean, scale=sem)
        # plotting diagram
        plt.errorbar(mean, 1, xerr=[[mean-ci[0]], [ci[1]-mean]], fmt='o', capsize=10, capthick=2, ecolor='red', linestyle='none')
        plt.axvline(mean, color='gray', linestyle='--', label=f'Mean = {mean:.2f}')
        plt.set_ylim(0.5, 1.5)
        plt.set_xlim(ci[0] - 1, ci[1] + 1)
        # Customize labels and title
        plt.set_xlabel('Mean Value')
        plt.set_title(f'Mean: {mean:.2f} | 95% Confidence Interval: ({ci[0]:.2f}, {ci[1]:.2f})')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_numerical_summary(self, column: str):
        """
        plots numerical summary with 4 plots
        1. QQ Plot
        2. Histogram
        3. CI plot
        4. Box plot
        With normality test
        """
        fig, axs = plt.subplots(2, 2, figsize=(10, 7))

        df_dict=self.check_normality(self.df, column)
        df_hypo_title = "{}\n{}\np-value:{} alpha: 0.05\n Result: {}".format(df_dict["h0"],
                                                                                df_dict["h1"],
                                                                                df_dict["p_val"],
                                                                                df_dict["cc"])

        fig.suptitle(df_hypo_title)

        # plot 1 : QQ plot
        sm.qqplot(self.df[column], line='45', ax=axs[0][0])
        axs[0][0].set_title("Q-Q Plot")
        axs[0][0].grid(True)

        # plot 2 : hist plot
        sns.histplot(data=self.df, x=column, kde=True, ax=axs[0][1], alpha=0.25, line_kws={'linewidth': 3})
        # measure of central tendency
        mean_max = np.round(st.mean(self.df[column]), 2)
        median_max = np.round(st.median(self.df[column]), 2)
        mode_max = np.round(st.mode(self.df[column]), 2)
        axs[0][1].set_title(f"Mean: {mean_max} | Median: {median_max} | Mode: {mode_max}")
        axs[0][1].axvline(ymin=0,ymax=mode_max,x=self.df[column].mean(), color="red",label="Mean")
        axs[0][1].axvline(ymin=0,ymax=mode_max,x=self.df[column].median(), color="green",label="Median")
        axs[0][1].set_xlabel(column)
        axs[0][1].legend()
        axs[0][1].grid(True)

        # plot 3 : confidence interval
        # Compute mean and standard error of the mean
        mean = np.mean(self.df[column])
        sem = stats.sem(self.df[column])
        # Compute 95% confidence interval
        confidence = 0.95
        ci = stats.t.interval(confidence, len(self.df)-1, loc=mean, scale=sem)
        # plotting diagram
        axs[1][0].errorbar(mean, 1, xerr=[[mean-ci[0]], [ci[1]-mean]], fmt='o', capsize=10, capthick=2, ecolor='red', linestyle='none')
        axs[1][0].axvline(mean, color='gray', linestyle='--', label=f'Mean = {mean:.2f}')
        axs[1][0].set_ylim(0.5, 1.5)
        axs[1][0].set_xlim(ci[0] - 1, ci[1] + 1)
        # Customize labels and title
        axs[1][0].set_xlabel('Mean Value')
        axs[1][0].set_title(f'Mean: {mean:.2f} | 95% Confidence Interval: ({ci[0]:.2f}, {ci[1]:.2f})')
        axs[1][0].legend()
        axs[1][0].grid(True)


        # plot 4 : box plot
        axs[1][1].boxplot(self.df[column], vert=False, patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                whiskerprops=dict(color='blue'),
                capprops=dict(color='blue'),
                # meanprops=dict(color='red'),
                medianprops=dict(color='green'))
        axs[1][1].set_xlabel('Value')
        axs[1][1].set_title('Horizontal Box Plot')
        axs[1][1].grid(True)

        plt.tight_layout()
        plt.show()

    # --- Inferential Analysis ---
    def check_normality(self, df: pd.DataFrame, column: str):
        """
        hypothesis test for normality check in continuous variable
        """
        stat, p_value = stats.shapiro(df[column])
        h_0 = "H0: data normally distributed"
        h_1 = "H1: data not normally distributed"
        result = ""
        if p_value < 0.05:
            result = "Reject null hypothesis"
        else:
            result = "Fail to reject null hypothesis"

        return {"h0":h_0, "h1":h_1,"p_val":np.round(p_value,3), "cc":result}

    def perform_one_sample_ttest(self, column: str, population_mean: float):
        """Performs a one-sample T-test."""
        stats, p_value = ttest_1samp(self.df[column].dropna(), popmean=population_mean)
        print(f"T-statistic: {stats:.2f}, P-value: {p_value:.3f}")
        # Add interpretation logic here
