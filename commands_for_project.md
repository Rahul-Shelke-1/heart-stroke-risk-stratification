# build environment using conda

```bash
conda create -p heart-env python=3.12 -y

conda activate ./heart-env

or

conda activate /Users/rahulshelke/Documents/Data-Science/Data-Science-Projects/heart-stroke-prediction/heart-env
```

### Use the activated env

```bash
poetry env use $(which python)
```

### Verify the environment

```bash
poetry env info
```

### Install poetry

```bash
poetry install
```

- It will install packages into your Conda environment.

- The `poetry.lock` file will still be created, ensuring reproducible installs.

### List all conda environments

```bash
conda env list
```

### Remove all installs from poetry

```bash

```

## check active environments

```bash
poetry env list
```

### run poetry command

```bash
poetry add ${cat requirements.txt}
```

### Sync changes with virtual environment

```bash
poetry install --sync
```

### run pre-commit on all files

```bash
poetry run pre-commit run --all-files
```

### run pre-commit on one specific file

```bash
poetry run pre-commit run --files /path/to/file.py
```

### run test on pytest

```bash
poetry run pytest tests/unit --cov=src --cov-report=term-missing
```

### run test with `print` outputs

```bash
poetry run pytest tests/unit --capture=no
```

### generate test coverage report

```bash
poetry run pytest --cov=src tests/unit
```

### generate HTML coverage report

```bash
poetry run pytest --cov=src --cov-report=html tests/unit
```

###################################
#
# feature branch push
#
# 1. Final Checks in your feature branch:
#
#   => poetry run pre-commit run --all-files
#
# 2. Run All Tests:
#
#   => poetry run pytest -v
#
# 3. Sync with `main` branch:
#
#   => git checkout main
#   => git pull origin main
#   => git checkout feature/clients-mongo-connector
#   => git merge main
#   - resolve merge conflicts if prompted
#
#   then re-run your tests:
#   => poetry run pytest
#
# 4. Stage and Commit Any Final Fixes:
#
#   => git add .
#   => git commit -m "Final clean-up for MongoDB client connector"
#
# 5. Push Your Branch to GitHub:
#
#   => git push origin features/clients-mongo-connector
###################################


run ci locally

```bash
act -W .github/workflows/<your-file-name>.yml
```

##################################

i am building custome code for feature seleciton, so i am curating things into a package , i have src/analyze/feature_selection/ in this i have filter_methods.py, embedded_methods.py and wrapper_methods.py, i am working in wrapper_methods.py, in thils i will need models for classifier and regressor, in this package i also have src/analyze and in this i have univariate/, bivariate/, outlier/, missing_values/ , feature_selection, then will create model_selection/, hyper_parameter_optimization, model_interpretation/, model_calibration, so that i can use this in my all the projects

Title
→ Demo (first impression)
→ Problem + Impact
→ Results (metrics table)
→ Architecture Diagram
→ Pipeline Breakdown
→ Design Decisions
→ Tech Stack (shortened)
→ Visualizations
→ Monitoring + Retraining
→ Future Improvements
→ Contact
