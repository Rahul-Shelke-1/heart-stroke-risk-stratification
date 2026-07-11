from typing import List, Optional

import numpy as np
import pandas as pd
from IPython.display import display
from pyampute.exploration.mcar_statistical_tests import MCARTest
from scipy.stats import chi2_contingency, ttest_ind


class MissingDescriber:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_missing_report(self) -> pd.DataFrame:
        """Generates a summary table of missing values count and percentage."""
        missing_count = self.df.isnull().sum()
        missing_percent = 100 * self.df.isnull().sum() / len(self.df)
        report = pd.DataFrame({'Missing Count': missing_count, 'Percentage (%)': missing_percent})
        return report[report['Missing Count'] > 0].sort_values(by='Percentage (%)', ascending=False)

    def classify_missingness_mcar_mar(self, missing_col: str, related_cols: List[str]) -> pd.DataFrame:
        """
        Tests if missingness in 'missing_col' is related to values in a list of 'related_cols'.
        Returns a DataFrame summarizing the test results.
        P < 0.05 suggests MAR (dependent); P >= 0.05 suggests MCAR (independent).
        """
        if self.df[missing_col].isnull().sum() == 0:
            print(f"No missing values in {missing_col}.")
            return pd.DataFrame()

        # Create a boolean flag ONCE: True if missing, False if not
        is_missing_flag = self.df[missing_col].isnull()

        results = []

        print(f"\n--- Testing MCAR/MAR for '{missing_col}' against {len(related_cols)} related columns ---")

        for col in related_cols:
            p_value = np.nan
            test_name = "N/A"
            conclusion = "Cannot test"

            if pd.api.types.is_numeric_dtype(self.df[col]):
                # T-test for numerical 'related_col'
                group_missing = self.df[col][is_missing_flag].dropna()
                group_not_missing = self.df[col][~is_missing_flag].dropna()

                if len(group_missing) > 1 and len(group_not_missing) > 1:
                    stat, p_value = ttest_ind(group_missing, group_not_missing, nan_policy='omit')
                    test_name = "Independent T-test"

            elif pd.api.types.is_categorical_dtype(self.df[col]) or pd.api.types.is_object_dtype(self.df[col]):
                # Chi-squared test for categorical 'related_col'
                contingency_table = pd.crosstab(self.df[col], is_missing_flag)
                if min(contingency_table.shape) > 1: # Ensure valid test dimensions
                    chi2, p_value, _, _ = chi2_contingency(contingency_table)
                    test_name = "Chi-squared Test"

            # Determine conclusion based on P-value
            if not np.isnan(p_value):
                if p_value < 0.05:
                    conclusion = "MAR (Dependent/Related)"
                else:
                    conclusion = "MCAR (Independent/Random)"

            results.append({
                'Related Column': col,
                'Test Used': test_name,
                'P-value': round(p_value, 4),
                'Conclusion': conclusion
            })

        results_df = pd.DataFrame(results)
        # Sort by P-value to see most dependent variables first
        return results_df.sort_values(by='P-value', ascending=True)

    def run_littles_mcar_test(self, columns: Optional[List[str]] = None) -> dict:
        """Performs Little's MCAR test on the specified numerical columns."""
        # ... (implementation for this function remains the same as previous response) ...
        data_to_test = self.df[columns] if columns else self.df
        data_to_test = data_to_test.select_dtypes(include=[np.number]).dropna(how='all')
        mt = MCARTest(method="little")
        p_value = mt.little_mcar_test(data_to_test)
        conclusion = "MCAR (P >= 0.05). No evidence against completely random missingness."
        if p_value < 0.05:
            conclusion = "Not MCAR (P < 0.05). Missingness is systematic (MAR or MNAR)."
        return {'Test': "Little's MCAR Test", 'P-value': round(p_value, 4), 'Conclusion': conclusion}

    def final_missingness_conclusion(self, missing_col: str, related_cols: List[str]) -> str:
        """
        Integrates individual bivariate tests and Little's MCAR test to provide a final conclusion.
        """
        # 1. Run Little's Global Test (Requires only numerical columns)
        numeric_cols = self.df[related_cols].select_dtypes(include=[np.number]).columns.tolist()
        global_result = self.run_littles_mcar_test(columns=numeric_cols)

        print("\n--- Final Integrated Missing Data Conclusion ---")
        print(f"Global Test Result: {global_result['Conclusion']}")

        if global_result['P-value'] < 0.05:
            print("\nGlobal test REJECTS the MCAR assumption. Data is likely MAR or MNAR.")
            print(f"Check the individual test results below for {missing_col} to identify which variables predict the missingness:")

            # 2. If not MCAR globally, show which individual tests flagged as MAR
            individual_results_df = self.classify_missingness_mcar_mar(missing_col, related_cols)
            display(individual_results_df[individual_results_df['P-value'] < 0.05])
            return "Conclusion: MAR or MNAR."

        else:
            print("\nGlobal test FAILS TO REJECT the MCAR assumption. It is safe to assume MCAR.")
            print("Conclusion: MCAR (Missing Completely At Random).")
            return "Conclusion: MCAR."
