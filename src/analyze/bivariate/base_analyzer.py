import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class BaseAnalyzer:
    """Base class providing shared methods and configuration."""
    def __init__(self, df: pd.DataFrame):
        self.df = df
        sns.set_style("whitegrid")
        # Add shared plotting utilities here (e.g., _save_static_plot, _display_dynamic_plot)

    def _plot_static(self, plot_func, *args, **kwargs):
        plt.figure(figsize=(10, 6))
        plot_func(*args, **kwargs)
        plt.show()

    def _plot_dynamic(self, fig):
        fig.show()
