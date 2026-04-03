# ---------------- BLOCK 1 — IMPORTS ----------------
from utils.cleaning import run_cleaning_pipeline

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np

matplotlib.use("Agg")

# ---------------- BLOCK 2 — PAGE CONFIG ----------------
st.set_page_config(
    page_title="DOX v2 🍇",
    page_icon="🍇",
    layout="wide"
)

# ---------------- BLOCK 3 — TITLE ----------------
col_title, col_badge = st.columns([5, 1])

with col_title:
    st.title("🍇 DOX — Data Exploration System")
    st.markdown("*Unlock the power of your dataset — like a Devil Fruit*")

with col_badge:
    st.markdown("""
    <div style='background:#7c3aed; color:white; padding:0.4rem 0.8rem;
    border-radius:8px; text-align:center; margin-top:1rem; font-weight:700;'>
        v2.1
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- BLOCK 4 — SIDEBAR ----------------
st.sidebar.header("📂 Upload Your Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Choose a file",
    type=["csv", "xlsx", "xls", "json"]
)

if uploaded_file is None:
    st.info("👈 Upload a dataset from the sidebar to get started.")
    st.stop()

# ---------------- BLOCK 5 — FILE LOADING ----------------
file_type = uploaded_file.name.split('.')[-1].lower()

try:
    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
        format_label = "CSV"

    elif file_type in ["xlsx", "xls"]:
        df = pd.read_excel(uploaded_file)
        format_label = "Excel"

    elif file_type == "json":
        df = pd.read_json(uploaded_file)
        format_label = "JSON"

    else:
        st.error("❌ Unsupported file type.")
        st.stop()

except Exception as e:
    st.error(f"❌ Error loading file: {e}")
    st.stop()

st.success(f"✅ {format_label} file loaded: **{uploaded_file.name}**")
st.divider()

numeric_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols     = df.select_dtypes(include="object").columns.tolist()

# ---------------- BLOCK 6 — DATASET OVERVIEW ----------------
st.header("📊 Dataset Overview")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Rows", df.shape[0])
c2.metric("Total Columns", df.shape[1])
c3.metric("Numeric Columns", len(numeric_cols))
c4.metric("Categorical Columns", len(cat_cols))
c5.metric("Total Missing", int(df.isnull().sum().sum()))

st.divider()

# ---------------- BLOCK 7 — DATA PREVIEW ----------------
st.header("🔍 Data Preview")
st.dataframe(df.head(10), use_container_width=True)
st.divider()

# ---------------- BLOCK 7.5 — ADVANCED DATA CLEANING (FIXED & EXPORT READY) ----------------
st.header("⚙️ Block 1 — Advanced Data Cleaning")

st.markdown(
    "This module intelligently detects outliers using statistical methods and allows "
    "safe removal without damaging your dataset."
)

# 🔥 Initialize session state to remember if the pipeline was run
if "pipeline_run" not in st.session_state:
    st.session_state.pipeline_run = False

# ---------------- RUN PIPELINE ----------------
if st.button("🚀 Run Cleaning Pipeline"):
    st.session_state.pipeline_run = True

# Only display results and the removal button IF the pipeline was triggered
if st.session_state.pipeline_run:

    # Run backend function
    results = run_cleaning_pipeline(
        df,
        outlier_tolerance=2,   # Matches updated utils/cleaning.py
        apply_removal=False    # Detect only first
    )

    cleaned_df = results["cleaned_df"]
    outlier_summary = results["outlier_summary"]
    row_counts = results["row_outlier_counts"]
    skewness_report = results["skewness_report"]

    # ---------------- METRICS (Gemini UI) ----------------
    total_rows = len(df)
    affected_rows = (row_counts > 0).sum()
    affected_pct = (affected_rows / total_rows) * 100 if total_rows > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", total_rows)
    col2.metric("Rows with Outliers", affected_rows)
    col3.metric("Data Affected", f"{affected_pct:.1f}%")

    # ---------------- WARNINGS ----------------
    if affected_rows == 0:
        st.success("🎉 No outliers detected! Your data is clean.")
    elif affected_pct > 15:
        st.warning(
            f"⚠️ {affected_pct:.1f}% of rows contain outliers. "
            "Be careful when removing data — it may affect results."
        )
    else:
        st.info("💡 Review the breakdown before removing outliers.")

    # ---------------- DETAILS (Gemini Style) ----------------
    with st.expander("📊 View Detailed Analysis"):

        tab1, tab2, tab3 = st.tabs(["By Column", "By Row", "Affected Data"])

        # ---- Column-wise ----
        with tab1:
            col_df = outlier_summary.reset_index()
            st.dataframe(col_df, use_container_width=True)

        # ---- Row-wise ----
        with tab2:
            row_df = row_counts[row_counts > 0].reset_index()
            row_df.columns = ["Row Index", "Outlier Count"]
            st.dataframe(row_df, use_container_width=True)

        # ---- Affected rows ----
        with tab3:
            affected_data = df[row_counts > 0]
            st.dataframe(affected_data, use_container_width=True)

    # ---------------- ACTION (SAFE REMOVAL) ----------------
    st.markdown("### 🧹 Action")

    # 🔥 Because of session_state, this button is no longer nested!
    if st.button("🗑️ Remove Outlier Rows Safely"):

        # Apply SAFE removal using tolerance
        final_results = run_cleaning_pipeline(
            df,
            outlier_tolerance=2,
            apply_removal=True
        )

        final_df = final_results["cleaned_df"]

        removed = len(df) - len(final_df)

        st.success(f"✅ Removed {removed} rows safely (tolerance-based)")

        # Safety warning
        if removed > 0.5 * len(df):
            st.warning("⚠️ More than 50% data removed — consider adjusting tolerance.")

        # Shows a safe preview of the top 10 rows
        st.subheader("📊 Cleaned Data Preview")
        st.dataframe(final_df.head(10), use_container_width=True)

        # ---------------- NEW DOWNLOAD BUTTON ----------------
        st.markdown("### 📥 Export")
        
        # Converts the FULL dataframe to CSV format
        csv_data = final_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="⬇️ Download Full Cleaned Dataset",
            data=csv_data,
            file_name="cleaned_dox_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )
       
st.divider()

# ---------------- BLOCK 8 — COLUMN INFORMATION ----------------
st.header("🗂️ Column Information")

missing_counts = df.isnull().sum()

col_info = pd.DataFrame({
    "Column Name": df.columns,
    "Data Type": df.dtypes.values,
    "Missing Values": missing_counts.values,
    "Missing %": (missing_counts.values / len(df) * 100).round(2),
    "Unique Values": df.nunique().values
})

st.dataframe(col_info, use_container_width=True)
st.divider()

# ---------------- BLOCK 10 — STATISTICAL SUMMARY ----------------
st.header("📈 Statistical Summary")

if len(numeric_cols) > 0:
    st.dataframe(df[numeric_cols].describe().round(2), use_container_width=True)

st.divider()

# ---------------- BLOCK 11 — OUTLIER DETECTION ----------------
st.header("🔍 Outlier Detection — IQR Method")

if len(numeric_cols) > 0:
    outlier_col = st.selectbox("Select column:", numeric_cols)

    col_data = df[outlier_col].dropna()

    Q1 = col_data.quantile(0.25)
    Q3 = col_data.quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = col_data[(col_data < lower) | (col_data > upper)]

    st.metric("Outliers Found", len(outliers))

    fig, ax = plt.subplots()
    ax.boxplot(col_data, vert=False)
    st.pyplot(fig)
    plt.close()

st.divider()

# ---------------- BLOCK 12 — CORRELATION HEATMAP ----------------
st.header("🔥 Correlation Heatmap")

if len(numeric_cols) >= 2:
    corr = df[numeric_cols].corr().round(2)

    threshold = st.slider("Correlation strength filter:", 0.0, 1.0, 0.5)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # 🔥 STRONG CORRELATION TABLE
    st.subheader("🔝 Strong Correlations")

    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

    strong_corr = (
        corr.where(mask)
        .stack()
        .reset_index()
    )

    strong_corr.columns = ["Column A", "Column B", "Correlation"]

    strong_corr = strong_corr[
        strong_corr["Correlation"].abs() >= threshold
    ].sort_values(by="Correlation", key=abs, ascending=False)

    if strong_corr.empty:
        st.warning("⚠️ No strong correlations found. Try lowering threshold.")
    else:
        st.dataframe(strong_corr, use_container_width=True)

st.divider()

# ---------------- BLOCK 13 — HISTOGRAM ----------------
st.header("📊 Histogram")

if len(numeric_cols) > 0:
    col = st.selectbox("Select column:", numeric_cols, key="hist")
    fig, ax = plt.subplots()
    ax.hist(df[col].dropna(), bins=30)
    st.pyplot(fig)
    plt.close()

st.divider()

# ---------------- BLOCK 14 — BAR CHART (FINAL FIX) ----------------
st.header("🏷️ Bar Chart")

bar_col = st.selectbox("Select column for bar chart:", df.columns)

data = df[bar_col].dropna()

if pd.api.types.is_numeric_dtype(data):
    bins = st.slider("Number of bins:", 5, 20, 10)
    binned = pd.cut(data, bins=bins)
    value_counts = binned.value_counts().sort_index()

    labels = [str(i) for i in value_counts.index]

    fig, ax = plt.subplots(figsize=(10, 5 + len(labels) * 0.3))
    ax.bar(range(len(value_counts)), value_counts.values)

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")

else:
    value_counts = data.value_counts().head(15)

    fig, ax = plt.subplots(figsize=(10, 5 + len(value_counts) * 0.3))
    ax.bar(value_counts.index.astype(str), value_counts.values)

    plt.xticks(rotation=45, ha="right")

ax.set_title(f"Bar Chart of '{bar_col}'")

plt.tight_layout()
st.pyplot(fig)
plt.close()

st.divider()

# ---------------- BLOCK 15 — FOOTER ----------------
st.markdown(
    "<div style='text-align:center; color:gray;'>"
    "🍇 DOX v2.1 | Built by <b>Risi Nigarish</b> 👑"
    "</div>",
    unsafe_allow_html=True
)
st.divider()