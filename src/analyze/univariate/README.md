# Univariate Analysis

This functionality strictly helps to perform univariate analysis on numerical and categorical variables, features are expected to be already clean

According to type of variable we have to perform following things:

## **Descriptive Analysis**

Descriptive analysis summarizes the main characteristics of the data using numbers and visualizations. This is the most common use of univariate analysis.

### Numerical Data

Functionality |	Code Implementation
--- | ---
Central Tendency |	Mean, Median, Mode.
Dispersion | Standard Deviation, Variance, Range (Max-Min), IQR.
Distribution | Shape	Skewness, Kurtosis.
Visualization |	Histograms, Box plots, Density plots.
Summary Table |	A function that returns a table of all these metrics (.describe() equivalent).

### Categorcial Data

Functionality | Code Implementation
---|---
Frequency Counts | Value counts (absolute numbers).
Proportions | Value counts (percentages).
Visualization | Bar charts (count plots), Pie charts.

## **Inferenctial Analysis**

Inferential analysis uses statistical tests to draw conclusions about the entire population based on your sample data.

### Numerical Data

Functionality | Code Implementation
---|---
Hypothesis Testing | One-sample T-test (e.g., "Is the average age different from 40?").
Confidence Intervals | Calculating the margin of error for the population mean/median.

### Categorical Data

Functionality | Code Implementation
---|---
Hypothesis Testing | Chi-squared Goodness-of-Fit test (e.g., "Are all department counts equal?").
Confidence Intervals | Calculating the CI for a population proportion (e.g., "What is the confidence interval for the proportion of 'Male' employees?").

## **Predictive Anslysis**

Predictive analysis involves building models that forecast future outcomes or probabilities based solely on that single variable. In univariate analysis, this is limited but possible, often focusing on forecasting time series data.

### Numerical Data

Functionality| Code Implementation (Example)
---|---
Time Series Forecasting | Simple moving averages or ARIMA models (if your numerical data is a time series).

### Categorical Data

Functionality|Code Implementation (Example)
Baseline Prediction| A function that simply predicts the most frequent category as a naive baseline model.

## **Prescriptive Anslysis**

Prescriptive analysis aims to provide recommendations for optimal actions based on the analysis of a single variable. This is the most complex level and often requires business logic layered on top of insights.

### Numerical/Categorical Data

Functionality| Code Implementation
---|---
Outlier Detection Logic| A function that returns a list of suggested data points that might need manual review (e.g., "These salaries are > 3 SD from the mean, review them").
Data Imputation Strategy| A function that suggests a specific imputation strategy (e.g., "Data has skew > 1.0, recommend imputing missing values with the median rather than the mean").
