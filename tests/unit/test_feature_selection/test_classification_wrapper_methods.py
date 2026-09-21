from pprint import pprint

import pandas as pd
import pytest
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.datasets import make_classification
from sklearn.ensemble import (AdaBoostClassifier, ExtraTreesClassifier,
                              GradientBoostingClassifier,
                              HistGradientBoostingClassifier,
                              RandomForestClassifier)
from sklearn.linear_model import (LogisticRegression, RidgeClassifier,
                                  SGDClassifier)
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier, XGBRFClassifier

from heart_stroke_prediction.analyze.feature_selection.wrapper_methods import \
    Wrapper_Methods

# --------------------- config --------------------------

@pytest.fixture
def fe_config() -> dict:
    """Fixture: return full feature engineering config values as dict for testing."""

    X, y = make_classification(
        n_samples=200,
        n_features=6,
        n_informative=4,
        n_redundant=1,
        n_classes=2,
        random_state=42
    )

    # Convert to DataFrame and attach target column
    feature_names = [f"f{i}" for i in range(X.shape[1])]
    df = pd.DataFrame(X, columns=feature_names)
    df["stroke"] = y  # target must exist in df for your code

    # Use all generated feature names as feature list
    features = feature_names

    return {
        "df": df,
        "features": features,
        "target": 'stroke',
        "scoring": 'f1',
        "n_splits": 5,
        "seed": 42,
        "shuffle": True,
        "n_repeats": 3,
        "model_type": "classification",
        "problem_type": "balanced",
        "bins": None
    }

def test_generate_random_seeds(fe_config):
    wm = Wrapper_Methods(**fe_config)
    seed_values = wm._generate_random_seeds()
    # pprint(f"seed_values : {seed_values}")
    assert len(seed_values) == fe_config["n_repeats"]

def test_load_data_shapes(fe_config):
    wm = Wrapper_Methods(**fe_config)
    assert wm.X.shape[0] == wm.y.shape[0]

@pytest.mark.parametrize("model_tag, model_name, model_object, expect_error", [
    ("LR",     "Logistic Regression",      LogisticRegression(),            False),
    ("RDG",    "Ridge Classifier",         RidgeClassifier(),               False),
    ("SGD",    "SGD Classifier",           SGDClassifier(),                 False),
    ("NB",     "Naive Bayes",              GaussianNB(),                    False),
    ("SVM",    "Support Vector Machine",   SVC(),                           False),
    ("KNN",    "K-Neighbors Classifier",   KNeighborsClassifier(),          False),
    ("DT",     "Decision Tree",            DecisionTreeClassifier(),        False),
    ("RF",     "Random Forest",            RandomForestClassifier(),        False),
    ("ETC",    "Extra Trees Classifier",   ExtraTreesClassifier(),          False),
    ("GB",     "Gradient Boosting",        GradientBoostingClassifier(),    False),
    ("AB",     "AdaBoost",                 AdaBoostClassifier(),            False),
    ("HGB",    "HistGradient Boosting",    HistGradientBoostingClassifier(),False),
    ("XGB",    "XGBoost",                  XGBClassifier(),                 False),
    ("XGBRF",  "XGB (Random Forest)",      XGBRFClassifier(),               False),
    ("LGBC",   "LGBM Classifier",          LGBMClassifier(),                False),
    ("CB",     "CatBoost",                 CatBoostClassifier(),            False),
])
def test_get_model_success(fe_config, model_tag, model_name, model_object, expect_error):
    wm = Wrapper_Methods(**fe_config)

    model_tuple = wm._get_model(model_tag)

    if expect_error:
        with pytest.raises(ValueError, match=f"Unknown model_tag: '{model_tag}'"):
            wm._get_model(model_tag)
        return  # stop test here for error case

    # Ensure key exists and value is a (name, model) tuple
    assert len(model_tuple) == 2

    # Validate returned model name
    assert model_name in model_tuple[0]

    model = model_tuple[1]

    assert callable(getattr(model, "fit", None))
    assert callable(getattr(model, "predict", None))
    assert isinstance(model.get_params(), dict)

def test_get_model_unknown_tag(fe_config):
    wm = Wrapper_Methods(**fe_config)
    tag = "XYZ"
    with pytest.raises(RuntimeError, match=f"Unknown model_tag: '{tag}'"):
        wm._get_model(tag)

def test_get_model_unsupported_model(fe_config):
    fe_config["model_type"] = "regression"
    wm = Wrapper_Methods(**fe_config)
    tag = "HGB"
    with pytest.raises(RuntimeError, match=f"Unknown model_tag: '{tag}'"):
        wm._get_model(tag)

def test_get_model_invalid_params(fe_config):
    wm = Wrapper_Methods(**fe_config)

    with pytest.raises(RuntimeError):
        wm._get_model("RF", {"not_a_real_param": 123})

@pytest.mark.slow
def test_directional_feature_selection(fe_config):
    wm = Wrapper_Methods(**fe_config)
    model_config={
        "LR": None,
        "DT": None,
    }
    report = wm.directional_feature_selection(
        use_balanced_data=True,
        model_configs=model_config,
    )
    pprint(f"report: {report}")
    assert isinstance(report, dict)

def test_directional_feature_selection_verbose(fe_config):
    wm = Wrapper_Methods(**fe_config)
    model_config={
        "LR": None,
        "DT": None,
    }
    report = wm.directional_feature_selection(
        use_balanced_data=True,
        model_configs=model_config,
        print_status=True
    )
    pprint(f"report: {report}")
    assert isinstance(report, dict)

@pytest.mark.slow
def test_backward_feature_elimination(fe_config):
    wm = Wrapper_Methods(**fe_config)
    model_config={
        "LR": None,
        "DT": None,
    }
    report = wm.backward_feature_elimination(
        use_balanced_data=True,
        model_configs=model_config,
    )
    pprint(f"report: {report}")
    assert isinstance(report, dict)

@pytest.mark.print
def test_backward_feature_elimination(fe_config):
    wm = Wrapper_Methods(**fe_config)
    model_config={
        "LR": None,
        "DT": None,
    }
    report = wm.backward_feature_elimination(
        use_balanced_data=True,
        model_configs=model_config,
        print_status=True
    )
    # pprint(f"report: {report}")
    assert isinstance(report, dict)

@pytest.mark.print_scores
def test_get_report_to_df(fe_config):
    wm = Wrapper_Methods(**fe_config)
    model_config={
        "LR": None,
        "DT": None,
    }
    report = wm.directional_feature_selection(
        use_balanced_data=True,
        model_configs=model_config,
        print_status=True
    )
    report = wm.get_report_to_df(report)
    pprint(f"report: {wm.model_report}")
