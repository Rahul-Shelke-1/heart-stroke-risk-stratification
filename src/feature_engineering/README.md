# Feature Engineering

This block of code is here to

```bash
src/feature_engineering/
├── experiment/
│   ├── numerical.py        # experiment on features with different techniques and visualize
│   └── categorical.py      # experiment on features with different techniques and visualize
└── use_custom_functions
```

## Structure of functions

**CustomFunction**

- fit
- fit_tranform
- get_feature_names_out
- get_metadata_routing
- get_params
- inverse_transform
- set_output
- set_params
- transform


## Execution

### 1. Numerical Features

- CustomImputer
    - here we pass `sklearn.impute` function to make internal changes.
- CustomConstantImputer
    - replace a fix value with another constant, (`Age`: 0 replace with `np.nan`).

### 2. Categorical Features

- CustomeLabelEncoder
    - custom label encoder, primary used to encode **target features** (1-D)
    - input: dict[str, str] = {'label1': 3, 'label2' : 2, 'label3' : 1}
    - output: pd.DataFrame

- CustomeOrdinalEncoder
    - this encodes the ordinal values, primary use is to encoder multiple features (2D)
    - input: dict[str, str] = {'label1': 3, 'label2' : 2, 'label3' : 1}
    - output: pd.DataFrame

- CustomeOnehotEncoder
    - custom one hot encoder


### 3. Feature Extractor

- CustomFeatureExtractor
    - performs custom function

### 4. Tranforma Distribution


### 5. Scale Distribution
