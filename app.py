# ============================================================
#   ⚡ DOX — Main App
#   Built by Risi Nigarish | King of Technology 👑
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ────────────────────────────────────────────────────────────
# STEP 1 — PAGE CONFIGURATION
# ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dox ⚡",
    page_icon="⚡",
    layout="wide"
)

# ────────────────────────────────────────────────────────────
# STEP 2 — TITLE & DESCRIPTION
# ────────────────────────────────────────────────────────────
st.title("⚡ Dox")
st.markdown("**Unlock the power of your dataset**")
st.divider()

# ────────────────────────────────────────────────────────────
# STEP 3 — FILE UPLOAD (Input Module)
# ────────────────────────────────────────────────────────────
st.sidebar.header("📂 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

# If no file is uploaded, show a message and stop
if uploaded_file is None:
    st.info("👈 Upload a CSV file from the sidebar to get started.")
    st.stop()

# ────────────────────────────────────────────────────────────
# STEP 4 — LOAD DATA (Data Processing Module)
# ────────────────────────────────────────────────────────────
df = pd.read_csv(uploaded_file)

st.success(f"✅ File uploaded successfully: **{uploaded_file.name}**")
st.divider()

# ────────────────────────────────────────────────────────────
# STEP 5 — DATASET OVERVIEW (Structure Analysis)
# ────────────────────────────────────────────────────────────
st.header("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rows", df.shape[0])
col2.metric("Total Columns", df.shape[1])
col3.metric("Numeric Columns", len(df.select_dtypes(include="number").columns))
col4.metric("Categorical Columns", len(df.select_dtypes(include="object").columns))

st.divider()

# ────────────────────────────────────────────────────────────
# STEP 6 — DATA PREVIEW
# ────────────────────────────────────────────────────────────
st.header("🔍 Data Preview")
st.markdown("First 5 rows of your dataset:")
st.dataframe(df.head())

st.divider()

# ────────────────────────────────────────────────────────────
# STEP 7 — COLUMN INFO (Data Types)
# ────────────────────────────────────────────────────────────
st.header("🗂️ Column Information")

col_info = pd.DataFrame({
    "Column Name"    : df.columns,
    "Data Type"      : df.dtypes.values,
    "Missing Values" : df.isnull().sum().values,
    "Unique Values"  : df.nunique().values
})

st.dataframe(col_info, use_container_width=True)

st.divider()

# ────────────────────────────────────────────────────────────
# STEP 8 — MISSING VALUES ANALYSIS
# ────────────────────────────────────────────────────────────
st.header("🚨 Missing Values")

total_missing = df.isnull().sum().sum()

if total_missing == 0:
    st.success("✅ No missing values found! Your dataset is clean.")
else:
    st.warning(f"⚠️ Total missing values found: {total_missing}")

    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0]

    missing_df = pd.DataFrame({
        "Column"         : missing_data.index,
        "Missing Count"  : missing_data.values,
        "Missing %"      : round(missing_data.values / len(df) * 100, 2)
    })

    st.dataframe(missing_df, use_container_width=True)

st.divider()

# ────────────────────────────────────────────────────────────
# STEP 9 — STATISTICAL SUMMARY
# ────────────────────────────────────────────────────────────
st.header("📈 Statistical Summary")
st.markdown("Mean, Median, Std, Min, Max — all numeric columns:")

numeric_cols = df.select_dtypes(include="number").columns.tolist()

if len(numeric_cols) == 0:
    st.info("No numeric columns found in this dataset.")
else:
    st.dataframe(df[numeric_cols].describe().round(2), use_container_width=True)

st.divider()

# ────────────────────────────────────────────────────────────
# STEP 10 — VISUALIZATION — HISTOGRAM (Distribution)
# ────────────────────────────────────────────────────────────
st.header("📊 Distribution — Histogram")

if len(numeric_cols) == 0:
    st.info("No numeric columns available for histogram.")
else:
    selected_col = st.selectbox("Select a column to visualize:", numeric_cols)

    fig, ax = plt.subplots(figsize=(10, 4))

    data = df[selected_col].dropna()

    ax.hist(data, bins=30, color="purple", edgecolor="black", alpha=0.7)

    # Mean line
    ax.axvline(data.mean(),   color="red",    linestyle="--", linewidth=2, label=f"Mean   : {data.mean():.2f}")

    # Median line
    ax.axvline(data.median(), color="orange", linestyle="--", linewidth=2, label=f"Median : {data.median():.2f}")

    ax.set_title(f"Distribution of '{selected_col}'")
    ax.set_xlabel(selected_col)
    ax.set_ylabel("Frequency")
    ax.legend()

    st.pyplot(fig)
    plt.close()

st.divider()

# ────────────────────────────────────────────────────────────
# STEP 11 — VISUALIZATION — BAR CHART (Categorical)
# ────────────────────────────────────────────────────────────
st.header("🏷️ Categorical Column — Bar Chart")

cat_cols = df.select_dtypes(include="object").columns.tolist()

if len(cat_cols) == 0:
    st.info("No categorical columns found in this dataset.")
else:
    selected_cat = st.selectbox("Select a categorical column:", cat_cols)

    value_counts = df[selected_cat].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.bar(
        value_counts.index.astype(str),
        value_counts.values,
        color="mediumslateblue",
        edgecolor="black"
    )

    ax.set_title(f"Top values in '{selected_cat}'")
    ax.set_xlabel(selected_cat)
    ax.set_ylabel("Count")
    plt.xticks(rotation=45, ha="right")

    st.pyplot(fig)
    plt.close()

st.divider()

# ────────────────────────────────────────────────────────────
# STEP 12 — FOOTER
# ────────────────────────────────────────────────────────────
st.markdown(
    "<div style='text-align:center; color:gray;'>"
    "⚡ Dox &nbsp;|&nbsp; Built by <strong>Risi Nigarish</strong>"
    "</div>",
    unsafe_allow_html=True
)