import time
import warnings
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# from heart_stroke_prediction.analyze.feature_selection.custom_balanced_baggig_classifier import BalancedBaggingClassifierCustom
# from heart_stroke_prediction.analyze.feature_selection.custom_balanced_baggig_regressor import BalancedBaggingRegressorCustom
from imblearn.combine import SMOTEENN, SMOTETomek
from imblearn.ensemble import (BalancedBaggingClassifier)
from imblearn.over_sampling import (ADASYN, SMOTE, SMOTEN, SMOTENC, SVMSMOTE,
                                    BorderlineSMOTE, KMeansSMOTE)
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.base import BaseEstimator
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_selection import RFE, SequentialFeatureSelector
from sklearn.metrics import (average_precision_score, make_scorer, roc_auc_score)
from sklearn.model_selection import (StratifiedKFold, train_test_split)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from src.analyze.registry import MODEL_REGISTRY

# Filter out the specific Scikit-Learn Parallel/delayed UserWarning
warnings.filterwarnings(
    "ignore",
    message="`sklearn.utils.parallel.delayed` should be used with `sklearn.utils.parallel.Parallel`"
)

class Wrapper_Methods:
    """
    This wrapper method is customized to handle classification problem with 5% prevalanced in data.
    """

    def __init__(
            self,
            df: pd.DataFrame,
            features: List[str],
            target: List[str],
            preprocessor: Pipeline,
            scaler_type: str = "standard",
            model_type: str = "classification",
            shuffle: bool = True,
            n_splits:int = 5,
            n_repeats: int = 10,
            seed: int = 42,
            bins: int = 10,
            device: str = 'cpu'
        ):
        # data param
        self.df = df                                # dataframe
        self.features = features                    # feature from dataframe
        self.target = target                        # target name from dataframe
        # model param
        self.preprocessor = preprocessor            # preprocessor pipeline
        self.scaler_type = scaler_type              # scalar to scale data
        self.model_type = model_type
        # experiment param
        self.shuffle = shuffle                      # shiffle data before making split
        self.n_splits = n_splits                    # The standard 5 folds
        self.n_repeats = n_repeats                  # Your N unique experiments
        self.seed = seed                            # One seed controls all N repetitions
        self.bins = bins                            # binning for calibration
        # tags/abbrivations of all regression models
        self.model_clf_tags = ["LR", "RDG", "NB", "SVM", "KNN", "DT", "RF", "SGD", "GB", "AB", "ETC", "XGB", "XGBRF", "LGB", "CB"]
        self.model_report = dict()
        self.device = device

        self._validate_parameters()

        self.X, self.y = self._load_data()

    def _validate_parameters(self):
        """Validate initialization parameters."""

        valid_scalers = ['minmax', 'standard']
        valid_model_type = ['classification', 'regression']
        valid_device = ['cpu', 'gpu']

        # data param validation
        if not isinstance(self.df, pd.DataFrame):
            raise TypeError(f"df must be a pd.DataFrame, got {type(self.df)}")

        if not isinstance(self.features, list):
            raise TypeError(f"features must be a list of string, got {type(self.features)}")

        for col in self.features:
            if not isinstance(col, str):
                warnings.warn(f"Column '{col}' must be a str, got {type(col)}")
            elif col not in self.df.columns.to_list():
                warnings.warn(f"Column '{col}' is not in dataframe")

        if not isinstance(self.target, list):
            raise TypeError(f"target must be a list, got {type(self.target)}")

        for col in self.target:
            if not isinstance(col, str):
                warnings.warn(f"Column '{col}' must be a str, got {type(col)}")
            elif col not in self.df.columns.to_list():
                warnings.warn(f"Column '{col}' is not in dataframe")

        # model param validation
        if not isinstance(self.preprocessor, Pipeline):
            raise TypeError(f"preprocessor must be sklearn.pipeline, got '{type(self.preprocessor)}'")

        if not isinstance(self.scaler_type, str):
            raise TypeError(f"scaler_type must be a str, got {type(self.scaler_type)}")

        if self.scaler_type not in valid_scalers:
            warnings.warn(
                f"scaler_type '{self.scaler_type}' is not recognized. "
                f" Valid options are: {valid_scalers}"
            )

        if not isinstance(self.model_type, str):
            raise TypeError(f"model_type must be a str, got {type(self.model_type)}")

        if self.model_type not in valid_model_type:
            warnings.warn(
                f"model_type '{self.model_type}' is not recognized. "
                f" Valid options are: {valid_model_type}"
            )

        # experiment param validation
        if not isinstance(self.shuffle, bool):
            raise TypeError(f"shuffle must be bool, got {type(self.shuffle)}")

        if not isinstance(self.n_splits, int):
            raise TypeError(f"n_splits must be int, got {type(self.n_splits)}")

        if not isinstance(self.n_repeats, int):
            raise TypeError(f"n_repeats must be int, got {type(self.n_repeats)}")

        if not isinstance(self.seed, int):
            raise TypeError(f"seed must be int, got {type(self.seed)}")

        if not isinstance(self.device, str):
            raise TypeError(f"device must be str, got {type(self.device)}")

        if self.device not in valid_device:
            warnings.warn(
                f"device '{self.device}' is not recognized. "
                f" Valid optiona are: {valid_device}"
            )

        if not isinstance(self.bins, int):
            raise TypeError(f"bins must be int, got {type(self.bins)}")

    def _generate_random_seeds(
        self,
        base_seed: int,
        n_seeds: int,
        low: int = 0,
        high: int = 2**32 - 1,
        ) -> List[int]:
        """
        Generate reproducible random seeds from a base seed.

        Parameters
        ----------
        base_seed : int
            Master seed for reproducibility
        n_seeds : int
            Number of random seeds to generate
        low : int
            Minimum seed value (inclusive)
        high : int
            Maximum seed value (exclusive)

        Returns
        -------
        List[int]
            List of deterministic random seeds
        """
        rng = np.random.default_rng(base_seed)
        return rng.integers(low=low, high=high, size=n_seeds).tolist()

    def _load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        try:
            X = self.df[self.features]
            y = self.df[self.target[0]]
            return X, y
        except Exception as e:
            raise e

    def _load_preprocessor(self, random_state: int = None) -> Pipeline:
        try:
            # assemble model
            steps = []

            # 1. preprocessor
            # steps.append(('preprocessor', self.preprocessor))

            # 2. scaler
            if self.scaler_type == 'standard':
                self.preprocessor.steps.append(('scaler', StandardScaler()))
            else:
                self.preprocessor.steps.append(('scaler', MinMaxScaler()))

            # 3. smote
            # if self.smote_strategy:
            #     self.preprocessor.steps.append(('smote', self._handle_imbalance_data(random_state=random_state)))

            full_pipeline = ImbPipeline(self.preprocessor.steps)

            return full_pipeline
        except Exception as e:
            raise RuntimeError(f"Error in _load_preprocessor : {e}")

    def _get_model(self, tag: str, params: dict | None = None) -> [str, Pipeline, Any]:
        try:
            # 1. Validate model_type
            if self.model_type not in MODEL_REGISTRY:
                raise KeyError(f"Unknown model_type: '{self.model_type}'")

            registry = MODEL_REGISTRY[self.model_type]

            # 2. Validate tag existence
            if tag not in registry:
                raise KeyError(f"Unknown model_tag: '{tag}'")

            model_name, model_obj = registry[tag]

            # 3. Validate availability
            # if model_cls is None:
            #     raise ValueError(
            #         f"Model '{tag}' is not supported in the current environment"
            #     )

            model = model_obj(**(params or {}))

            # assemble model
            steps = []

            # 1. scaler
            if self.scaler_type == 'standard':
                steps.append(('scaler', StandardScaler()))
            else:
                steps.append(('scaler', MinMaxScaler()))

            # 2. smote
            # if self.smote_strategy:
            #     steps.append(('smote', self._handle_imbalance_data(random_state=random_state)))

            # 3. model : list level -1
            # steps.append(('model', model))

            full_pipeline = Pipeline(steps=self.preprocessor.steps+steps)

            full_pipeline.set_output(transform="pandas")

            return model_name, full_pipeline, model
        except Exception as e:
            raise RuntimeError(f"Error in _get_model: {e}")

    def _handle_imbalance_data(
            self,
            random_state: int
        ):
        if self.smote_strategy == 'smote':
            return SMOTE(random_state=random_state)
        elif self.smote_strategy == 'smoten':
            return SMOTEN(random_state=random_state)
        elif self.smote_strategy == 'smotenc':
            return SMOTENC(random_state=random_state)
        elif self.smote_strategy == 'adasyn':
            return ADASYN(random_state=random_state)
        elif self.smote_strategy == 'border_line_smote':
            return BorderlineSMOTE(random_state=random_state)
        elif self.smote_strategy == 'kmeans_smote':
            return KMeansSMOTE(random_state=random_state)
        elif self.smote_strategy == 'svm_smote':
            return SVMSMOTE(random_state=random_state)
        elif self.smote_strategy == 'smoteenn':
            return SMOTEENN(random_state=random_state)
        elif self.smote_strategy == 'smote_tetomek':
            return SMOTETomek(random_state=random_state)

    def recall_at_percent_func(self, y_true, y_probs, percent):
        # Ensure we use probability of the positive class (column index 1)
        if len(y_probs.shape) == 2:
            y_probs = y_probs[:, 1]

        n = len(y_true)
        k = int(np.ceil(n * percent))
        # Sort indices by descending probability
        indices = np.argsort(y_probs)[::-1]
        top_k = indices[:k]

        # Handle pandas series vs numpy arrays
        y_true_array = y_true.values if hasattr(y_true, "values") else y_true
        return y_true_array[top_k].sum() / y_true_array.sum()

    def precision_at_percent_func(self, y_true, y_probs, percent):
        if len(y_probs.shape) == 2:
            y_probs = y_probs[:, 1]

        n = len(y_true)
        k = int(np.ceil(n * percent))
        indices = np.argsort(y_probs)[::-1]
        top_k = indices[:k]

        y_true_array = y_true.values if hasattr(y_true, "values") else y_true
        return y_true_array[top_k].sum() / k

    def nns_at_percent_func(self, y_true, y_probs, percent):
        # NNS is 1 / Precision
        precision = self.precision_at_percent_func(y_true, y_probs, percent)
        if precision == 0:
            return np.inf  # Lower is better for NNS
        return 1 / precision

    def _evaluate_selected_features(self, X_train, y_train, X_test, y_test, model):
        """
        Docstring for _evaluate_selected_features
        """
        try:
            metrics = {
                "roc_auc": [],
                "pr_auc": [],
                "recall_10": [],
                "recall_15": [],
                "recall_20": [],
                "precision_10": [],
                "nns_10": []
            }

            # fit the model
            model.fit(X_train, y_train)
            y_scores = model.predict_proba(X_test)[:, 1]

            # Core metrics
            metrics["roc_auc"].append(roc_auc_score(y_test, y_scores))
            metrics["pr_auc"].append(average_precision_score(y_test, y_scores))

            # Ranking metrics
            metrics["recall_10"].append(self.recall_at_percent_func(y_test.values, y_scores, 0.10))
            metrics["recall_15"].append(self.recall_at_percent_func(y_test.values, y_scores, 0.15))
            metrics["recall_20"].append(self.recall_at_percent_func(y_test.values, y_scores, 0.20))

            metrics["precision_10"].append(self.precision_at_percent_func(y_test.values, y_scores, 0.10))
            metrics["nns_10"].append(self.nns_at_percent_func(y_test.values, y_scores, 0.10))

            return metrics
        except Exception as e:
            raise RuntimeError(f"Error in _evaluate_model: {e}")

    def _print_scores(self, metrics: Dict, model_name:str, selected_features: List[str]):
        try:
            # print model name
            print('='*15, model_name,'='*15)

            print(f"Selected Fetaures: {selected_features}\n")

            for key, values in metrics.items():
                print(f"{key}: {np.mean(values):.4f} ({np.std(values):.4f})")

            print()
        except Exception as e:
            raise e

    def _get_all_scores(self, X_test, y_test, model, model_type,  metrics: List[str]) -> dict:
        """
        returns all calculated scores for provided model, on test score with all metrics
        """
        try:
            if model_type == 'classification':
                from sklearn.metrics import classification_report
                report = classification_report(y_test, model.predict(X_test))
                return report
            else:
                pass
        except Exception as e:
            raise e

    def box_plot(self, names: Optional[List[str]] = None, results: Optional[List[List[float]]]= None) -> None:
        """
        Plots a box plot to compare model performance across different feature combinations.

        Args:
            names (List[str]): List of model or feature combination names (used as x-axis labels).
            results (List[List[float]]): A list of score lists, where each sublist contains
                                        cross-validation scores for a model or feature set.

        Returns:
            None

        Raises:
            ValueError: If the input lengths of `names` and `results` do not match.
            Exception: For any unexpected errors during plotting.
        """
        try:
            if names is None and results is None:
                names = self.model_report.keys()
                results = self.model_report.values()

            if len(names) != len(results):
                raise ValueError("Length of 'names' must match the number of result sets.")

            plt.boxplot(results, labels=names, showmeans=True, vert=False)
            plt.ylabel("Models")
            plt.xlabel(f"Score: {self.primary_scoring}")
            plt.title("Performance of Models")
            plt.grid()
            plt.show()

        except Exception as e:
            print(f"An error occurred while plotting the box plot: {e}")
            raise

    def get_report_to_df(self, metric: str, scores: List[List[Dict]], columns: List[str] = ["model_name", "cv_scores"]):
        try:
            df = pd.DataFrame()

            # model names
            df[columns[0]] = scores['model_name']

            # mean scores
            df[columns[1]] = [np.mean(d[0][f'test_{metric}']) for d in scores['cv_scores']]

            # return sorted report
            return df.sort_values(by=columns[1], ascending=False).reset_index(drop=True)
        except Exception as e:
            raise e

    def get_weighted_features(self, report: List[List[Dict]]):
        """
        For experiment e:

        - Let S_e = selected feature set

        - Let k_e = |S_e|

        - Let score_e = mean CV score

        Feature contribution per experiment

        For feature f:

            contribution(f, e) =
                score_e / k_e        if f ∈ S_e
                0                    if f ∉ S_e

        Final SFS feature score

            SFS_score(f) = Σ_e contribution(f, e)

        Optional normalization:

            SFS_score(f) /= number_of_experiments
        """
        try:
            pass
        except Exception as e:
            raise e

    def get_ranked_fetaures(self, report: List[List[Dict]]):
        """
        For experiment e:

        - rank_e(f) from rfe.ranking_

        - score_e from CV

        Feature contribution:

            contribution(f, e) = score_e / rank_e(f)

        Aggregate:

            RFE_score(f) = Σ_e (score_e / rank_e(f))

        Stability metric:

            selection_frequency(f) = (# times f selected) / total_experiments
        """
        try:
            # blank dataframe
            df = pd.DataFrame()

            # add column model names
            df["model_name"] = report['model_name']

        except Exception as e:
            raise e

    def classfier_for_imbalanced_data(self, model, direction: str):
        try:
            if self.device == 'cpu':
                # for cross validation
                cv = StratifiedKFold(n_splits=self.n_splits, shuffle=self.shuffle, random_state=self.seed)
                # bagging classifier
                bbc = BalancedBaggingClassifier(
                            estimator=model, # Assuming the last step is the base model
                            sampling_strategy='auto',
                            random_state=self.seed,
                            n_jobs=-1 # Use all available CPU cores
                        )

                # This ensures SFS selects features based on CALIBRATED Precision/F2
                search_estimator = CalibratedClassifierCV(
                    estimator=bbc,
                    method='sigmoid',
                    cv=cv, # Use the same CV for calibration logic
                )
                                # Create the scorers
                recall_pct_scorer = make_scorer(
                    self.recall_at_percent_func,
                    percent=0.10,
                    response_method="predict_proba" # or needs_proba=True in older versions
                )

                # features selection object
                selection_obj = SequentialFeatureSelector(
                    estimator=search_estimator,   # try on this model
                    n_features_to_select='auto',  # select automatically
                    tol = None,                   # score threshould
                    direction=direction,          # direction of feature selection
                    scoring=recall_pct_scorer,    # evaluation metric
                    cv=cv,                        # cross validation method
                    n_jobs=-1,                    # use all cores
                )
            else: # gpu
                pass

            return selection_obj, bbc
        except Exception as e:
            raise e

    def classifier_for_balanced_data(self):
        try:
            if self.device == 'cpu':
                pass
            else:
                pass
        except Exception as e:
            raise e

    def directional_feature_selection(
            self,
            model_configs: Optional[dict] = None,
            print_metric: bool = True,
            direction: str = "forward",
            default_use_bagging: bool = True,
            default_use_calibration: bool = False,
    ) -> dict:
        """
        Objective: this works on subset of features and there influence over evaluation metric, that will get us to max score
        by forwardly or backwardly eliminating the features from superset

        Remainder: this technique works with parametric and non-parametric models, does not rely on feature importance or
        models coefficients to determin the feature selection

        model_configs (Dict[str, Optional[dict, Any]]): it contains model tag, and model parameters (optional)

        print_status (bool): print model training status

        direction (str): feature selection direction , default is "forward"
                            "forward"  : subset -> superset
                            "backward" : superset -> subset

        Returns:

        model_report (dict): models performance on each subset of features
        """
        try:
            model_report = {
                "model_name": [],
                "selected_features": [],
                "all_scores": [
                    {
                        "roc_auc": [],
                        "pr_auc": [],
                        "recall_10": [],
                        "recall_15": [],
                        "recall_20": [],
                        "precision_10": [],
                        "nns_10": [],
                    }
                ],
            }

            # --------- Select Features -------------

            for model_tag, params in model_configs.items():
                cfg = cfg or {}
                params = cfg,get("params", {})
                use_bagging = cfg.get("use_bagging", default_use_bagging)
                use_calibration = cfg.get("use_calibration", default_use_calibration)
                bagging_params = cfg.get("bagging_params")
                calibration_params = cfg.get("calibration_params")

                # ------------- sequenctial feature selection ------------------
                # get the base model
                model_name, full_pipeline, model = self._get_model(model_tag, params)


                selection_obj, bbc = self.classfier_for_imbalanced_data(model, direction)

                # combining pipeline and model
                full_model = ImbPipeline(steps=full_pipeline.steps + [("sfs", selection_obj)])

                # print(f"full model: {full_model}")

                start = time.time()
                # 2. Fit the selector
                full_model.fit(self.X, self.y)
                end = time.time()
                print("Sequential Feature Selection Execution time:", end - start, "seconds")

                # 3. FIX: Index safely using NumPy
                selected_indices = full_model['sfs'].get_support(indices=True)
                # feature_names = full_model.named_steps["outlier_handeling"].get_feature_names_out()
                feature_names = full_model[:-1].get_feature_names_out()
                selected_features = feature_names[selected_indices]

                # --------- validate the features robustness ------------

                seed_values = self._generate_random_seeds(
                                    base_seed=self.seed,
                                    n_seeds=self.n_repeats
                                )

                eval_scores_per_exp = []
                features_list_per_exp = []

                for seed in seed_values:

                    # splitting the data into train test split
                    X_train_sandbox, X_holdout, y_train_sandbox, y_holdout = train_test_split(
                        self.X, self.y, test_size=0.3, random_state=seed,
                        shuffle=self.shuffle, stratify=self.y
                    )

                    # 1. Transform data through the preprocessing parts of the pipeline
                    X_train_processed = full_pipeline.fit_transform(X_train_sandbox)
                    X_val_processed = full_pipeline.transform(X_holdout)
                    self.X_features = X_train_processed.columns.tolist()
                    selected_features = np.array(X_train_processed.columns)[selected_indices].tolist()

                    # ------------- evaluating selected feature ------------------
                    scores = self._evaluate_selected_features(
                                        X_train_processed.iloc[:, selected_indices],
                                        y_train_sandbox,
                                        X_val_processed.iloc[:, selected_indices],
                                        y_holdout,
                                        bbc
                                    )

                    features_list_per_exp.append(selected_features)
                    # eval_scores_per_exp[0][].append(scores["roc_auc"])
                    model_report["all_scores"][0]["roc_auc"].append(scores["roc_auc"])
                    model_report["all_scores"][0]["pr_auc"].append(scores["pr_auc"])
                    model_report["all_scores"][0]["recall_10"].append(scores["recall_10"])
                    model_report["all_scores"][0]["recall_15"].append(scores["recall_15"])
                    model_report["all_scores"][0]["recall_20"].append(scores["recall_20"])
                    model_report["all_scores"][0]["precision_10"].append(scores["precision_10"])
                    model_report["all_scores"][0]["nns_10"].append(scores["nns_10"])

                # collecting models name
                model_report["model_name"].append(model_name)

                # feature lists
                model_report["selected_features"].append(features_list_per_exp)

                # collecting scores of each fold per experiments
                # model_report["all_scores"].append(eval_scores_per_exp)

                # print scores with only metric from passed emtrics
                if print_metric:
                    self._print_scores(model_report["all_scores"][0], model_name, selected_features)

            return model_report
        except Exception as e:
            raise RuntimeError(f"Error in directional_feature_selection : {e}")

    def backward_feature_elimination(self, model_configs: Optional[Dict[str, Optional[dict]]] = None, print_metric: bool = True) -> dict:
        """
        Objective: this works on subset of features and there influence over evaluation metric, that will get us to max score
        by forwardly or backwardly eliminating the features from superset

        Remainder: this technique works with parametric and non-parametric models, does not rely on feature importance or
        models coefficients to determin the feature selection

        Parameters:

        model_tags (List[str]): abbrivateions of model its optional

        print_status (bool): print model training status

        direction (str): feature selection direction , default is "forward"
                            "forward"  : subset -> superset
                            "backward" : superset -> subset

        Returns:

        model_report (dict): models performance on each subset of features
        """
        try:
            model_report = {
                "model_name": [],
                "selected_features": [],
                "all_scores": [
                    {
                        "roc_auc": [],
                        "pr_auc": [],
                        "recall_10": [],
                        "recall_15": [],
                        "recall_20": [],
                        "precision_10": [],
                        "nns_10": [],
                    }
                ],
            }

            # --------- Select Features -------------

            for model_tag, params in model_configs.items():

                # ------------- sequenctial feature selection ------------------
                # get the base model
                model_name, full_pipeline, model = self._get_model(model_tag, params)

                if self.model_type == 'classification':
                    selection_obj, bbc = self.classfier_for_imbalanced_data(model,)
                    selection_obj = RFE(
                        estimator=model,                # try on this model
                        step=1,                         # num of features at a time
                        cv=cv,                          # evaluation metric
                        scoring=self.primary_scoring,   # evaluation metric
                        min_features_to_select=1,       # minimun feature select
                        n_jobs=-1,                      # use all cores
                    )
                # combining pipeline and model
                full_model = ImbPipeline(steps=full_pipeline.steps + [("sfs", selection_obj)])

                print(f"full model: {full_model}")

                start = time.time()
                # 2. Fit the selector
                full_model.fit(self.X, self.y)
                end = time.time()
                print("Sequential Feature Selection Execution time:", end - start, "seconds")

                # 3. FIX: Index safely using NumPy
                selected_indices = full_model['sfs'].get_support(indices=True)
                # feature_names = full_model.named_steps["outlier_handeling"].get_feature_names_out()
                feature_names = full_model[:-1].get_feature_names_out()
                selected_features = feature_names[selected_indices]

                # --------- validate the features robustness ------------

                seed_values = self._generate_random_seeds(
                                    base_seed=self.seed,
                                    n_seeds=self.n_repeats
                                )

                eval_scores_per_exp = []
                features_list_per_exp = []

                for seed in seed_values:

                    # splitting the data into train test split
                    X_train_sandbox, X_holdout, y_train_sandbox, y_holdout = train_test_split(
                        self.X, self.y, test_size=0.3, random_state=seed,
                        shuffle=self.shuffle, stratify=self.y
                    )

                    # 1. Transform data through the preprocessing parts of the pipeline
                    X_train_processed = full_pipeline.fit_transform(X_train_sandbox)
                    X_val_processed = full_pipeline.transform(X_holdout)
                    self.X_features = X_train_processed.columns.tolist()
                    selected_features = np.array(X_train_processed.columns)[selected_indices].tolist()

                    # ------------- evaluating selected feature ------------------
                    scores = self._evaluate_selected_features(
                                        X_train_processed.iloc[:, selected_indices],
                                        y_train_sandbox,
                                        X_val_processed.iloc[:, selected_indices],
                                        y_holdout,
                                        bbc
                                    )

                    features_list_per_exp.append(selected_features)
                    # eval_scores_per_exp[0][].append(scores["roc_auc"])
                    model_report["all_scores"][0]["roc_auc"].append(scores["roc_auc"])
                    model_report["all_scores"][0]["pr_auc"].append(scores["pr_auc"])
                    model_report["all_scores"][0]["recall_10"].append(scores["recall_10"])
                    model_report["all_scores"][0]["recall_15"].append(scores["recall_15"])
                    model_report["all_scores"][0]["recall_20"].append(scores["recall_20"])
                    model_report["all_scores"][0]["precision_10"].append(scores["precision_10"])
                    model_report["all_scores"][0]["nns_10"].append(scores["nns_10"])

                # collecting models name
                model_report["model_name"].append(model_name)

                # feature lists
                model_report["selected_features"].append(features_list_per_exp)

                # collecting scores of each fold per experiments
                # model_report["all_scores"].append(eval_scores_per_exp)

                # print scores with only metric from passed emtrics
                if print_metric:
                    self._print_scores(model_report["all_scores"][0], model_name, selected_features)

            return model_report
        except Exception as e:
            raise e

    # ------------------------------------------------------------------
    # 1. Single builder method: composes the estimator based on switches
    # ------------------------------------------------------------------
    def _build_estomator(
            self,
            base_model: BaseEstimator,
            use_bagging: bool = True,
            use_calibration: bool = False,
            bagging_params: Optional[dict] = None,
            calibration_params: Optional[dict] = None,
            cv = None,
    ) -> BaseEstimator:
        """
        Compose an estimator with optional BalancedBaggignClassifier and/or
        optionl ClibratedClassifierCV wrapping.

        Order: bagging wraps the base model first (if enabled),
        then calibration wraps whatever comes out of that (if enabled).
        This order matters - calibrating raw scores from bagging is
        usually more meaningful than bagging already-calibrated scores.
        """
        estimator = base_model

        if use_bagging:
            bg = bagging_params or {}
            estimator = BalancedBaggingClassifier(
                estimator=estimator,
                sampling_strategy=bp.get("sampling_strategy", "auto"),
                random_state=self.seed,
                n_jobs=-1,
                **{k: v for k, v in bp.items() if k != "sampling_strategy"},
            )

        if use_calibration:
            cp = calibration_params or {}
            estimator = CalibratedClassifierCV(
                estimator=estimator,
                method=cp.get("method", "sigmoid"),
                cv=cv,
            )

        return estimator

    # ---------------------------------------------------------------
    # 2. classifier_for_imbalanced_data now just takes the switches
    #    and passes them through - no branching logic duplicated here
    # ---------------------------------------------------------------
    def classifier_for_imbalanced_data(
            self,
            model,
            direction: str,
            use_bagging: bool = True,
            use_calibration: bool = False,
            bagging_params: Optional[dict] = None,
            calibration_params: Optional[dict] = None,
    ) -> Tuple[SequentialFeatureSelector, BaseEstimator]:
        try:
            if self.device == "cpu":
                cv = StratifiedKFold(
                    n_split=self.n_splits,
                    shuffle=self.shuffle,
                    random_state=self.seed,
                )

                search_estimator = self._build_estomator(
                    base_model=model,
                    use_bagging=use_bagging,
                    use_calibration=use_calibration,
                    bagging_params=bagging_params,
                    calibration_params=calibration_params,
                    cv=cv,
                )

                recall_pct_score = make_scorer(
                    self.recall_at_percent_func,
                    percent=0.10,
                    response_method="predict_proba",
                )

                selection_obj = SequentialFeatureSelector(
                    estimator=search_estimator,
                    n_features_to_select="auto",
                    tol=None,
                    direction=direction,
                    scoring=recall_pct_score,
                    cv=cv,
                    n_jobs=-1,
                )
            elif self.device == "gpu":
                raise NotImplementedError(
                    "GPU path not implemented yet. Use device='cpu'."
                )
            else:
                raise ValueError(f"Unknown device: {self.device}")

            # return BOTH - you need search_estimator later for
            # _evaluate_selected_features instead of the undefined 'bbc'
            return selection_obj, search_estimator
        except Exception as e:
            raise e
