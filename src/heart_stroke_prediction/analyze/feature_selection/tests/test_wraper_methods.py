import pandas as pd
import pytest
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.pipeline import Pipeline

from heart_stroke_prediction.analyze.feature_selection.wrapper_methods import \
    Wrapper_Methods

CAT_FEATURES = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
NUM_FEATURES = ['age', 'avg_glucose_level', 'bmi']
ALREADY_PROCESSED = ['hypertension', 'heart_disease',]
ID_COL = ['id']
TARGET_COL = ['stroke']

def get_full_config(get_config):
    """
    load config for Wrapper class
    """
    config = get_config.copy()

    config["features"] = ID_COL+NUM_FEATURES+CAT_FEATURES+ALREADY_PROCESSED+TARGET_COL
    config["target"] = TARGET_COL

    return config

def test_get_config(get_config):
    """
    load config
    """
    config = get_config.copy()

    config["features"] = ID_COL+NUM_FEATURES+CAT_FEATURES+ALREADY_PROCESSED+TARGET_COL
    config["target"] = TARGET_COL

    assert isinstance(config, dict)
    assert isinstance(config["df"], pd.DataFrame)
    assert isinstance(config["scaler_type"], str)
    assert isinstance(config["n_splits"], int)
    assert isinstance(config["shuffle"], bool)
    assert isinstance(config["n_repeats"], int)
    assert isinstance(config["seed"], int)
    assert isinstance(config["model_type"], str)
    assert isinstance(config["bins"], int)
    assert isinstance(config['preprocessor'], Pipeline)
    assert isinstance(config['features'], list)
    assert isinstance(config['target'], list)

def test_generate_random_seeds(get_config):
    """
    testing generate random seeds
    """
    config = get_full_config(get_config)
    wrapper = Wrapper_Methods(**config)
    result = wrapper._generate_random_seeds(
        base_seed=config['seed'],
        n_seeds=config['n_repeats']
    )
    assert len(result) == config['n_repeats']

def test_load_data(get_config):
    """
    testing _load_data functionality
    """
    config = get_full_config(get_config)

    wrapper = Wrapper_Methods(**config)

    X, y = wrapper._load_data()

    assert isinstance(X, pd.DataFrame), f"Expected DataFrame, got {type(X)}"
    assert isinstance(y, pd.Series), f"Expected Series, got {type(y)}"

def test_get_model(get_config):
    """
    testing _get_model functionality
    """
    # initalize
    config = get_full_config(get_config)
    wrapper = Wrapper_Methods(**config)

    model_name, full_pipeline = wrapper._get_model(
        tag = "RF",
        random_state=42
    )

    preprocessor_len = len(config['preprocessor'].steps)
    # print(f"\npreprocessor length: {preprocessor_len}")

    preprocessor = full_pipeline[:-1]

    # print(f"\npreprocessor: {preprocessor}")

    model = full_pipeline[-1]
    # print(f"\nmodel: {model}")

    assert callable(getattr(model, "fit", None))
    assert callable(getattr(model, "predict", None))
    assert isinstance(model.get_params(), dict)
    assert isinstance(full_pipeline, ImbPipeline)
    assert isinstance(model_name, str)

@pytest.mark.test_this
def test_directional_feature_selection(get_config):
    # initalize
    config = get_full_config(get_config)
    wrapper = Wrapper_Methods(**config)

    model_configs = {
        "RF": {}
    }

    report = wrapper.directional_feature_selection(
        model_configs=model_configs,
        print_metric=True
    )

    assert isinstance(report, dict)
