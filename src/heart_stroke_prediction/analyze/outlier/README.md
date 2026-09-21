Here is a clean and practical **Outlier Handling Guide** you can directly use in your EDA workflow.

---

# **Outlier Handling — Steps, Methods & Best Practices**

Outliers are values that lie far outside the typical range of the data. They may represent:

* Data entry errors
* Measurement issues
* Rare valid cases (true extreme events)

Your handling strategy must depend on *why* the outlier exists and *how* it affects the model.

---

# **1. Detecting Outliers**

### **A. Statistical Methods**

1. **Z-Score Rule**

   * Compute z-score = (x – mean)/std
   * Mark as outlier if |z| > 3

2. **IQR Rule**

   * Q1 = 25th percentile
   * Q3 = 75th percentile
   * IQR = Q3 – Q1
   * Outliers = values < Q1 – 1.5×IQR or > Q3 + 1.5×IQR
   * Good for skewed data.

### **B. Visualization**

* Boxplot
* Histogram
* Scatterplot
* Violin plot

### **C. Model-Based**

* Isolation Forest
* DBSCAN
* LOF (Local Outlier Factor)

---

# **2. Decide How to Handle Outliers**

### **A. Remove Outliers**

Use when:

* It’s definitely an error (e.g., age = 999)
* Very small dataset impact
* Does not represent the real world

→ `df = df[(df[col] > lower) & (df[col] < upper)]`

### **B. Cap / Winsorize**

Replace extreme values with boundary limits:

* Values < lower bound → set to lower bound
* Values > upper bound → set to upper bound

Useful for:

* Heavy-tailed distributions
* Financial data (to avoid loss of information)

### **C. Impute Outliers**

Replace them with:

* Median (best for skewed columns)
* Mean (for normal distribution)
* Mode (categorical)

### **D. Transform Data**

If distribution is extremely skewed:

* Log transform
* Square root
* Box-Cox
* Yeo-Johnson

Transforms shrink extreme values naturally.

### **E. Treat Separately**

If rare cases matter (fraud detection, anomalies):

* Keep them
* Create a binary feature (flag_outlier=1)

---

# **3. Outlier Strategy Framework (Use in EDA)**

For each numeric column:

1. **Check distribution**

   * If normally distributed → use z-score
   * If skewed → use IQR

2. **Identify reason for outlier**

   * Data entry?
   * Real extreme?
   * Domain-specific?

3. **Choose strategy**

   * If error → remove
   * If extreme but valid → cap
   * If important → keep + flag
   * If skewed → transform

4. **Document the choice**

   * Store before/after metrics
   * Mention in EDA report

---

# **4. Quick Code Snippet (Reusable)**

### **IQR Method + Capping**

```python
def cap_outliers_iqr(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df[col] = df[col].clip(lower, upper)

    return df
```

---

# **5. Outlier Handling Checklist (Use in Notebook)**

✅ Check distribution
✅ Detect using IQR or Z-score
✅ Confirm with visualization
✅ Decide strategy (remove, cap, transform, keep)
✅ Apply
✅ Compare before/after stats

* mean, median, std
* boxplot difference
* % outliers removed
* model performance impact

---
