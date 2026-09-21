# ✅ **Missing Values Analysis — Step-By-Step**

---

## **1. Identify Missing Values**

Start by checking *where* and *how much* missing data exists.

### **1.1 Basic missing count**

```python
df.isna().sum()
```

### **1.2 Missing percentage per column**

```python
(df.isna().mean() * 100).round(2)
```

### **1.3 Row-wise missing count**

```python
df.isna().sum(axis=1)
```

---

## **2. Visualize Missing Patterns**

### **2.1 Bar plot of missing values (% per column)**

* Good for a quick overview.
  (Use **Matplotlib/Seaborn** here.)

### **2.2 Heatmap of missingness**

* Shows block patterns (useful for time/sequence data).

### **2.3 Missing correlation map**

* Checks if missing in Column A is related to missing in Column B.

Use:

* `missingno.matrix()`
* `missingno.heatmap()`
* `missingno.bar()`

---

## **3. Classify Missing Types (Very Important for Logic)**

### **3.1 MCAR (Missing Completely at Random)**

Missing has no relationship with any variable.
→ Simple imputation works.

### **3.2 MAR (Missing At Random)**

Missing depends on other columns.
→ Use statistical imputation or ML models.

### **3.3 MNAR (Missing Not At Random)**

Missing depends on the value itself.
e.g., income is missing because people don't want to share.
→ Requires domain logic or modeling the missingness itself.

---

## **4. Analyze Missingness Impact**

### **4.1 Compare distributions**

Check whether:

* rows with missing values differ significantly from
* rows without missing values

Example:

```python
df[df['age'].isna()]['income'].describe()
df[df['age'].notna()]['income'].describe()
```

### **4.2 Group-based missingness**

```python
df.groupby('gender')['age'].apply(lambda x: x.isna().mean())
```

This shows if missingness depends on categories.

---

## **5. Choose the Strategy**

### **5.1 Delete if…**

Use deletion only when:

* Missing % < 5%
* Feature is not important
* Row deletion won’t bias analysis

Types:

* Drop rows: `df.dropna()`
* Drop columns: `df.drop(columns=['col'])`

---

### **5.2 Impute if…**

#### **Numerical**

* Mean / Median
* KNN Imputation
* Regression imputation
* Interpolation (time series)

#### **Categorical**

* Mode
* “Unknown” / “Missing”
* Frequency-based fill
* Statistical models (Naive Bayes, CatBoost)

#### **Time Series**

* Forward fill
* Backward fill
* Rolling window
* Seasonal decomposition

---

### **5.3 Keep Missing as Value**

Useful for:

* Fraud detection
* Medical datasets
* Categorical missingness

You can convert missing into its own category:

```python
df['category'] = df['category'].fillna('Missing')
```

---

## **6. Validate Imputation**

After filling, check:

### **6.1 Distribution comparison**

Original distribution vs Imputed distribution.

### **6.2 Outliers introduced?**

### **6.3 Bias check**

Ensure imputation didn’t:

* Shift mean too much
* Reduce variance
* Distort correlations

---

## **7. Document the Strategy**

Maintain a clean record:

* Missing % per column
* Method used
* Reason for choosing that method
* Any assumptions

---

# 📌 **Final Template (You Can Use in Your Project)**

```
1. Identify missing values
    - count, percent, row-wise

2. Visualize missingness
    - missingno plots
    - seaborn barplot
    - heatmap correlation

3. Classify missing type
    - MCAR / MAR / MNAR

4. Analyze missingness impact
    - distribution comparisons
    - group-based missingness

5. Decide strategy
    - drop / impute / keep missing category

6. Apply imputation
    - numeric / categorical / time series methods

7. Validate imputation
    - distribution shifts
    - correlation changes

8. Document steps
    - for reproducibility
```

---
