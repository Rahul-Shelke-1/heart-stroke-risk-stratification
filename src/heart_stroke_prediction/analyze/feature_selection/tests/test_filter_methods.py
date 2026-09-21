import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

from heart_stroke_prediction.analyze.feature_selection.filter_methods import \
    Filter

CAT_FEATURES = ['gender', 'ever_married', 'work_type', 'residence_type', 'smoking_status']
NUM_FEATURES = ['age', 'avg_glucose_level', 'bmi']
ALREADY_PROCESSED = ['hypertension', 'heart_disease',]
ID_COL = ['id']

pipeline = Pipeline(
    steps=[
        ('preprocessing',
         ColumnTransformer(
             transformers=[
                 ('drop', 'drop', ID_COL),
                 ('ordinal_encode', OrdinalEncoder(), CAT_FEATURES),
                 ('dont_pass', 'passthrough', ALREADY_PROCESSED),
             ],
             remainder='passthrough',
             verbose_feature_names_out=False,
         )
         ),
    ]
)
pipeline.set_output(transform='pandas')

def test_check_correlation(get_handled_missing_dataframe):
    """
    Checking the correlation
    """
    filter = Filter(get_handled_missing_dataframe)

    df_corr = filter._check_correlation(features=['age', 'avg_glucose_level'])

    assert len(df_corr) > 0
    assert len(df_corr) == 3

def test_check_normality(get_handled_missing_dataframe):
    """
    Checking the normality in feature
    """
    filter = Filter(get_handled_missing_dataframe)

    result = filter._check_normality('age')

    assert result['p_val'] < 0.05

def test_t_test_of_independence(get_handled_missing_dataframe):
    """
    testing t-test of independence
    """
    filter = Filter(get_handled_missing_dataframe)

    result = filter._t_test_of_independence('age', 'stroke')

    assert result['p_val'] < 0.05

def test_mannwhitneyu_test(get_handled_missing_dataframe):
    """
    testing mannwhitneyu test
    """
    filter = Filter(get_handled_missing_dataframe)

    result = filter._mannwhitneyu_test('age', 'stroke')

    assert result['p_val'] < 0.05

def test_chisquare_test(get_handled_missing_dataframe):
    """
    testing chisquare test
    """
    filter = Filter(get_handled_missing_dataframe)

    result = filter._chisquare_test('gender')

    assert result['p_val'] < 0.05

def test_chisquare_independence_test(get_handled_missing_dataframe):
    """
    testing chisquare independent test
    """
    filter = Filter(get_handled_missing_dataframe)

    result = filter._chisquare_independence_test('age', 'stroke')

    assert result['p_val'] < 0.05

def test_ANOVA(get_handled_missing_dataframe):
    """
    testing anova test
    """
    filter = Filter(get_handled_missing_dataframe)

    result = filter._ANOVA('age', 'stroke')

    assert result['p_val'] < 0.05

def test_statistical_filtering(get_raw_dataframe):
    """
    testing filtering functionality
    """
    filter = Filter(get_raw_dataframe)

    result = filter.statistical_filtering(NUM_FEATURES, CAT_FEATURES, 'stroke')

    assert isinstance(result, pd.DataFrame), f"Expected DataFrame, got {type(result)}"

def test_f_test(get_handled_missing_dataframe):
    """
    testing f_test functionality
    """
    df = pipeline.fit_transform(get_handled_missing_dataframe)

    filter = Filter(df)

    result = filter._f_test(NUM_FEATURES+CAT_FEATURES, 'stroke')

    assert isinstance(df, pd.DataFrame), f"Expected DataFrame, got {type(df)}"
    assert isinstance(result, np.ndarray), f"Expected Array, got {type(result)}"

def test_mutual_information(get_handled_missing_dataframe):
    """
    testing mututal information functionality
    """
    df = pipeline.fit_transform(get_handled_missing_dataframe)

    filter = Filter(df)

    result = filter._mutual_information(NUM_FEATURES+CAT_FEATURES, 'stroke')

    assert isinstance(df, pd.DataFrame), f"Expected DataFrame, got {type(df)}"
    assert isinstance(result, np.ndarray), f"Expected Array, got {type(result)}"

def test_mi_dataframe(get_handled_missing_dataframe):
    """
    testing mututal information functionality
    """
    df = pipeline.fit_transform(get_handled_missing_dataframe)

    filter = Filter(df)

    result = filter.mi_dataframe(NUM_FEATURES, CAT_FEATURES, 'stroke')

    assert isinstance(result, pd.DataFrame), f"Expected DataFrame, got {type(result)}"
