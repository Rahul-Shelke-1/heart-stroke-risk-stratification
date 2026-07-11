from typing import Optional

import matplotlib.pyplot as plt
import missingno as msno
import pandas as pd
import seaborn as sns

# Make sure to install missingno: pip install missingno

class MissingVisualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def plot_missing_matrix(self, figsize: tuple = (10, 6)):
        """
        Visualizes the missing data pattern as a matrix.
        Shows where data is present (lines) and missing (white spaces).
        """
        plt.figure(figsize=figsize)
        msno.matrix(self.df, ax=plt.gca())
        plt.title('Missing Value Matrix')
        plt.show()

    def plot_missing_barplot(self, figsize: tuple = (10, 6)):
        """Visualizes missing value counts per column in a bar plot."""
        plt.figure(figsize=figsize)
        msno.bar(self.df, ax=plt.gca())
        plt.title('Missing Value Counts Bar Plot')
        plt.show()

    def plot_missing_heatmap(self, figsize: tuple = (10, 6)):
        """
        Visualizes the correlation between missingness of different columns.
        """
        plt.figure(figsize=figsize)
        msno.heatmap(self.df, ax=plt.gca())
        plt.title('Missing Value Correlation Heatmap')
        plt.show()

    def plot_missing_dendrogram(self):
        """
        Visualizes the hierarchy of missing data.
        Groups columns whose missingness pattern is most correlated.
        """
        # Dendrogram handles its own plotting context
        msno.dendrogram(self.df)
        plt.title('Missing Value Dendrogram')
        plt.show()

    def plot_missing_frequency_displot(self, threshold: Optional[float] = 0.4, figsize: tuple = (10, 8)):
        """
        Visualizes missing value frequency using a Seaborn displot (melted format).
        Helps visualize the proportion of missing vs. present values per variable.
        Can specify a red vertical line threshold for visual guidance (e.g., 0.4 or 40%).
        """
        # Melt the DataFrame to long format for easier plotting with Seaborn
        data_melted = self.df.isnull().melt(value_name='missing')

        g = sns.displot(
            data=data_melted,
            y='variable',
            hue='missing',
            multiple='fill', # Stack bars to 100%
            height=figsize[1],
            aspect=figsize[0] / figsize[1]
        )
        g.fig.suptitle('Proportion of Missing Data per Variable', y=1.02)

        # Add a threshold line if specified (e.g., a policy that >40% missing data means dropping the column)
        if threshold is not None:
            g.ax.axvline(threshold, color='r', linestyle='--', label=f'Threshold ({threshold*100:.0f}%)')
            g.ax.legend()

        plt.show()

    def plot_comparison_by_missingness(self, missing_col: str, compare_col: str, plot_type: str = 'boxplot'):
        """
        Visualizes the distribution of 'compare_col' across groups: those missing 'missing_col' vs those not missing it.
        Plot types: 'boxplot', 'kde', 'count' (for categorical compare_col).
        """
        if self.df[missing_col].isnull().sum() == 0:
            print(f"No missing values in {missing_col} to compare.")
            return

        # Create a temporary dataframe with a flag for missingness
        temp_df = self.df.copy()
        temp_df['is_missing'] = temp_df[missing_col].isnull().map({True: 'Missing', False: 'Observed'})

        plt.figure(figsize=(10, 6))

        if pd.api.types.is_numeric_dtype(temp_df[compare_col]):
            # If comparing against a numerical column (use boxplot or KDE)
            if plot_type == 'boxplot':
                # Assign the plot result to an 'ax' variable
                ax = sns.boxplot(
                    data=temp_df,
                    x='is_missing',
                    y=compare_col,
                    hue='is_missing', # Use hue here to generate legend handles
                    dodge=False # Dodge must be False because x and hue are the same
                )
                plt.title(f'Distribution of {compare_col} by Missingness of {missing_col}')
                # Explicitly call the legend on the returned ax object
                # ax.legend(title=f'{missing_col} Status')
            elif plot_type == 'kde':
                sns.kdeplot(data=temp_df, x=compare_col, hue='is_missing', fill=True, common_norm=False, alpha=0.5)
                plt.title(f'KDE of {compare_col} by Missingness of {missing_col}')
            else:
                print("Use 'boxplot' or 'kde' for a numerical comparison column.")
                return

        elif pd.api.types.is_categorical_dtype(temp_df[compare_col]) or pd.api.types.is_object_dtype(temp_df[compare_col]):
            # Handling categorical comparison column
            if plot_type == 'count':
                sns.countplot(data=temp_df, x=compare_col, hue='is_missing')
                plt.title(f'Counts of {compare_col} by Missingness of {missing_col}')
                plt.legend(title=f'{missing_col} Status')

            elif plot_type == 'stacked_percent_bar':
                # Create the proportions table (normalized within each missingness group)
                proportions = pd.crosstab(
                    temp_df[compare_col],
                    temp_df['is_missing'],
                    normalize='index' # Normalize so each bar (Missing/Observed) sums to 1 (100%)
                ) * 100

                # Plot the stacked bar chart using pandas plotting
                ax = proportions.plot(kind='bar', stacked=True, figsize=(10, 6), width=0.7)
                plt.title(f'Percentage Stacked Bar of {compare_col} by Missingness of {missing_col}')
                plt.ylabel('Percentage (%)')
                plt.xticks(
                    rotation=0,
                    ha='right')
                # plt.ylim(0, 110) # Ensure Y-axis goes exactly from 0 to 100

                # Add percentages within bars for clarity
                for container in ax.containers:
                    ax.bar_label(container, fmt='%.1f%%', label_type='center')

            else:
                 print("Use 'count' or 'stacked_percent_bar' for a categorical comparison column.")
                 return
        else:
            print(f"Unsupported dtype for {compare_col}.")
            return
