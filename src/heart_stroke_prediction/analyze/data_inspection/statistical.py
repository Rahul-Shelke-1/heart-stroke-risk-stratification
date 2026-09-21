import pandas as pd

"""Statistical analysis methods"""

def describe_numerical(self) -> pd.DataFrame:
    """Extended statistics for numerical columns"""
    return self.df.describe(include=[np.number]).T

def describe_categorical(self) -> dict:
    """Stats for categorical columns"""
    stats = {}
    for col in self.categorical_columns:
        stats[col] = {
            "unique_count": self.df[col].nunique(),
            "unique_values": self.df[col].unique().tolist(),
            "top_value": self.df[col].mode().iloc[0] if not self.df[col].mode().empty else None,
            "top_frequency": self.df[col].value_counts().iloc[0] if not self.df[col].value_counts().empty else 0
        }
    return stats

def correlation_matrix(self, method='pearson'):
    """Correlation analysis"""
    return self.df.corr(method=method)
