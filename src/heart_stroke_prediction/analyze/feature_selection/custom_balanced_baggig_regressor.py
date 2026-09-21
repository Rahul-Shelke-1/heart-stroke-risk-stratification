import cudf
import numpy as np
from scipy import stats
from sklearn.base import BaseEstimator, RegressorMixin, clone
from sklearn.tree import DecisionTreeRegressor
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y


class BalancedBaggingRegressorCustom(BaseEstimator, RegressorMixin):
    def __init__(self, base_estimator=None, n_estimators=100):
        self.base_estimator = base_estimator
        self.n_estimators = n_estimators
        self.estimators_ = []

    def fit(self, X, y):
        # SFS passes a small subset of features here as a NumPy arrays
        # 1. Convert to GPU ONLY when we are ready to do the heavy math
        X = cudf.DataFrame(X)
        y = cudf.Series(y)

        # 1. Standard sklearn validation
        X, y = check_X_y(X, y)
        self.classes_ = np.unique(y)

        self.estimators_ = []
        unique_classes, counts = np.unique(y, return_counts=True)
        n_minority = np.min(counts)

        base_clf = self.base_estimator if self.base_estimator else DecisionTreeRegressor()

        for _ in range(self.n_estimators):
            indices_to_keep = []
            for cls in unique_classes:
                cls_indices = np.where(y == cls)[0]
                # Changed to replace=False for robust undersampling as discussed
                chosen_indices = np.random.choice(cls_indices, n_minority, replace=False)
                indices_to_keep.extend(chosen_indices)

            X_resampled, y_resampled = X[indices_to_keep], y[indices_to_keep]

            clf = clone(base_clf)
            clf.fit(X_resampled, y_resampled)
            self.estimators_.append(clf)
        return self

    def predict(self, X):
        check_is_fitted(self)
        X = check_array(X)

        all_preds = np.array([clf.predict(X) for clf in self.estimators_])
        final_preds, _ = stats.mode(all_preds, axis=0, keepdims=False)
        return final_preds
