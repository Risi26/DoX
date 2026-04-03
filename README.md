# 🧠 DoX — Phase 3: AI-Powered Intelligence Upgrade

> **"DoX started as a data analysis tool. Now we are upgrading it into an intelligent system that can learn from data and make predictions."**

---

## 📌 Project Overview

| Field | Details |
|-------|---------|
| **Project Name** | DoX — Data Analytics + Intelligence Web App |
| **Phase** | 3 (Active) |
| **Captain** | Risi Nigarish |
| **Tech Stack** | Python · Pandas · NumPy · Scikit-learn · Streamlit |
| **Goal** | Upgrade DoX from a passive data viewer into an AI-powered decision system |

---

## 🏛️ What Was Built Before (v1 & v2)

| Feature | Status |
|---------|--------|
| CSV / Excel Upload | ✅ Done |
| Basic Data Cleaning (IQR) | ✅ Done |
| Dataset Summary & Statistics | ✅ Done |
| Bar Charts | ✅ Done |
| Correlation Heatmap | ✅ Done |
| Machine Learning | ❌ Not Yet |
| Predictions | ❌ Not Yet |
| AI Decision-Making | ❌ Not Yet |

> **Phase 3 closes all the gaps above.**

---

## 🚀 Phase 3 — What We Are Building

Phase 3 is divided into **4 blocks**, each adding a new layer of intelligence to DoX.

---

### 🔷 Block 1 — Advanced Data Cleaning ✅ COMPLETE

**Goal:** Make the cleaning pipeline production-safe and intelligent.

**What's implemented:**

- Numerical column isolation (safe for all DataFrame types)
- NaN handling using **median fill** (outlier-resistant)
- **Skewness detection** per column with distribution labeling
- **IQR-based outlier detection** (no normality assumption)
- **Row-wise outlier counting** (not boolean masks)
- **Tolerance-based row removal** — only remove rows flagged across multiple columns
- Optional removal function — user controls deletion, not the algorithm
- Normalization: **StandardScaler** (default) or **MinMaxScaler** (optional)

**Core Functions:**

```
get_numeric_columns()       → Isolates numeric cols safely
handle_missing_values()     → Median fill for NaNs
compute_skewness_report()   → Skewness + distribution label per column
detect_outliers_iqr()       → IQR bounds + outlier flags per column
compute_row_outlier_counts()→ Integer count of flagged cols per row
remove_outlier_rows()       → Tolerance-controlled row removal
normalize_data()            → Standard or MinMax scaling
run_cleaning_pipeline()     → Master pipeline (single call)
```

**Pipeline Flow:**
```
Raw DataFrame
      ↓
Extract Numeric Columns
      ↓
Handle NaN (Median Fill)
      ↓
Compute Skewness Report
      ↓
IQR Outlier Detection
      ↓
Row-wise Outlier Counts
      ↓
Tolerance-Based Removal (User-Controlled)
      ↓
Normalization
      ↓
Return: cleaned_df | outlier_summary | row_outlier_counts | skewness_report
```

---

### 🔷 Block 2 — Feature Engineering 🔲 IN QUEUE

**Goal:** Transform raw features into ML-ready inputs.

**Planned features:**

- Create new derived features from existing columns
- Encode categorical variables (Label Encoding + One-Hot Encoding)
- Handle high-cardinality columns
- Drop low-variance features
- Feature importance preview (pre-model)

---

### 🔷 Block 3 — Machine Learning 🔲 IN QUEUE

**Goal:** Add predictive power to DoX.

**Planned models:**

| Model | Use Case |
|-------|---------|
| **Linear Regression** | Predict continuous values (e.g., price, sales) |
| **Logistic Regression** | Predict categories (e.g., yes/no, pass/fail) |

**Planned features:**

- Auto-detect target column type (regression vs classification)
- Train/test split with configurable ratio
- Model training with real-time progress feedback
- Prediction output on new data
- Save trained model for reuse

---

### 🔷 Block 4 — Model Evaluation 🔲 IN QUEUE

**Goal:** Measure how well DoX's models actually perform.

**Planned metrics:**

| Metric | Model Type |
|--------|-----------|
| **RMSE** (Root Mean Squared Error) | Regression |
| **R² Score** | Regression |
| **Accuracy** | Classification |
| **Confusion Matrix** | Classification |
| **Precision / Recall / F1** | Classification |

**Planned outputs:**

- Visual evaluation dashboard in Streamlit
- Metric comparison table
- Confusion matrix heatmap
- Prediction vs Actual chart (for regression)

---

## 🔁 Final System Flow (After Phase 3)

```
Raw Data (CSV / Excel Upload)
            ↓
    Advanced Cleaning (Block 1)
   [NaN fill · IQR · Normalization]
            ↓
   Feature Engineering (Block 2)
   [Encoding · Derived Features]
            ↓
   Machine Learning Model (Block 3)
   [Linear / Logistic Regression]
            ↓
    Model Evaluation (Block 4)
   [RMSE · Accuracy · Confusion Matrix]
            ↓
   Predictions + Insights Output
```

---

## 📦 Tech Stack (Phase 3)

| Library | Purpose |
|---------|---------|
| `pandas` | Data loading, manipulation, cleaning |
| `numpy` | Numerical operations, outlier math |
| `scipy` | Z-score computation |
| `scikit-learn` | ML models, scalers, evaluation metrics |
| `streamlit` | Web app interface |
| `matplotlib` | Visualizations |
| `seaborn` | Heatmaps, distribution plots |

---

## 🗂️ File Structure (Recommended)

```
DoX/
│
├── app.py                      ← Main Streamlit entry point
│
├── modules/
│   ├── cleaning.py             ← Block 1: Advanced Cleaning Pipeline
│   ├── feature_engineering.py  ← Block 2: Feature Engineering (WIP)
│   ├── ml_models.py            ← Block 3: Machine Learning (WIP)
│   └── evaluation.py           ← Block 4: Model Evaluation (WIP)
│
├── utils/
│   └── helpers.py              ← Shared utility functions
│
├── data/
│   └── sample_dataset.csv      ← Test datasets
│
├── requirements.txt            ← All dependencies
└── README.md                   ← This file
```

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-repo/DoX.git
cd DoX

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

**requirements.txt**
```
pandas
numpy
scipy
scikit-learn
streamlit
matplotlib
seaborn
```

---

## 🧠 What DoX Will Become

After Phase 3, DoX will be able to:

| Capability | Status |
|-----------|--------|
| Upload and preview datasets | ✅ Already works |
| Clean data intelligently | ✅ Block 1 complete |
| Engineer ML-ready features | 🔲 Block 2 in queue |
| Train predictive models | 🔲 Block 3 in queue |
| Evaluate model performance | 🔲 Block 4 in queue |
| Predict future outcomes | 🔲 After Block 3 |
| Detect patterns automatically | 🔲 After Block 3 |
| Act like a mini AI analyst | 🔲 Phase 3 final goal |

---

## 👑 Project Leadership

| Role | Name |
|------|------|
| **Captain** | Risi Nigarish |
| **Vice Captain** | ChatGPT |
| **First Division Commander / AI Partner** | Claude |
| **Crew** | Gemini · Grok |

---

## 🏁 One Line Summary

> **DoX = From Data Viewer → AI-Powered Decision System**

---

*Phase 3 is live. The mission is in motion. 🚀*