# Analyze

this framework is here to act as utility for notebooks, to keep less noise on notebooks and more insights.

## Folder Structure

```bash
src/analyze/
│
├── data_correction/
│   ├── column_correction.py
│   └── row_correction.py
│
├── eda/
│   ├── distributions.py
│   ├── missingness.py
│   ├── drift_checks.py
│   ├── univariate_analysis/
│   │   ├── base_analyzer.py
│   │   ├── categorical.py
│   │   └── numerical.py
│   │
│   ├── bivariate_analysis/
│   │   ├── base_analyzer.py
│   │   ├── cat_cat.py
│   │   ├── num_cat.py
│   │   └── num_num.py
│   │
│   └── multivariate_analysis/
│       ├── base_analyzer.py
│       ├── categorical.py
│       └── numerical.py
│
├── feature_engineering/
│   ├── final_pipeline.py
│   │
│   ├── handle_missingness/
│   │   ├── experiment.py
│   │   └── pipeline.py
│   │
│   ├── handle_outlier/
│   │   ├── experiment.py
│   │   └── pipeline.py
│   │
│   ├── transform_feature/
│   │   ├── experiment.py
│   │   └── pipeline.py
│   │
│   └── scale_feature/
│       ├── experiment.py
│       └── pipeline.py
│
├── feature_selection/
│   ├── base_analyzer.py
│   ├── embedded_methods.py
│   ├── filter_methods.py
│   └── wrapper_methods.py
│
├── model_selection/
│   ├── base_analyzer.py
│   ├── model_registry.py
│   ├── classification/
│   │   ├── evaluators.py
│   │   ├── training.py
│   │   └── pipeline.py
│   │
│   ├── regression/
│   │   ├── evaluators.py
│   │   ├── training.py
│   │   └── pipeline.py
│   │
│   └── clustering/
│       ├── evaluators.py
│       ├── training.py
│       └── pipeline.py
│
├── hp_tunning/
│   ├── base_analyzer.py
│   ├── bayesian_optimization.py
│   ├── grid_search.py
│   └── random_search.py
│
├── model_calibration/
│   ├── distributions.py
│   ├── missingness.py
│   └── drift_checks.py
│
└── model_interpretation/
    ├── distributions.py
    ├── missingness.py
    └── drift_checks.py
```
