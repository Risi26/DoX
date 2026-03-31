# ---------------- BLOCK 1 — IMPORTS ----------------
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
        v2.0
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- BLOCK 4 — SIDEBAR ----------------
st.sidebar.header("📂 Upload Your Dataset")
st.sidebar.markdown("Supported formats: **CSV, Excel, JSON**")

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

# ---------------- BLOCK 9 — MISSING VALUES ----------------
st.header("🚨 Missing Values Analysis")

total_missing = missing_counts.sum()

if total_missing == 0:
    st.success("✅ No missing values found!")
else:
    st.warning(f"⚠️ Total missing values: {total_missing}")

    missing_df = pd.DataFrame({
        "Column": missing_counts[missing_counts > 0].index,
        "Missing Count": missing_counts[missing_counts > 0].values,
        "Missing %": (missing_counts[missing_counts > 0].values / len(df) * 100).round(2)
    })

    st.dataframe(missing_df, use_container_width=True)

st.divider()

# ---------------- BLOCK 10 — STATISTICAL SUMMARY ----------------
st.header("📈 Statistical Summary")

if len(numeric_cols) == 0:
    st.info("No numeric columns found.")
else:
    st.dataframe(df[numeric_cols].describe().round(2), use_container_width=True)

st.divider()

# ---------------- BLOCK 11 — OUTLIER DETECTION ----------------
st.header("🔍 Outlier Detection — IQR Method")

if len(numeric_cols) == 0:
    st.info("No numeric columns available.")
else:
    outlier_col = st.selectbox("Select column:", numeric_cols)

    col_data = df[outlier_col].dropna()

    Q1 = col_data.quantile(0.25)
    Q3 = col_data.quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = col_data[(col_data < lower) | (col_data > upper)]

    st.metric("Outliers Found", len(outliers))
    st.write(f"Lower: {round(lower,2)} | Upper: {round(upper,2)}")

    fig, ax = plt.subplots()
    ax.boxplot(col_data, vert=False)
    st.pyplot(fig)
    plt.close()

st.divider()

# ---------------- BLOCK 12 — CORRELATION HEATMAP (FINAL FIXED) ----------------
st.header("🔥 Correlation Heatmap")

if len(numeric_cols) < 2:
    st.info("Need at least 2 numeric columns.")
else:
    corr = df[numeric_cols].corr().round(2)

    # Controls
    show_annot = st.checkbox("Show correlation values", value=True)
    threshold = st.slider("Correlation strength filter:", 0.0, 1.0, 0.5)

    # Dynamic sizing based on number of columns
    size = len(corr.columns)
    fig_size = max(6, size * 0.6)

    fig, ax = plt.subplots(figsize=(fig_size, fig_size))

    # Adjust font size dynamically
    font_size = max(6, 12 - size * 0.3)

    sns.heatmap(
        corr,
        annot=show_annot,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        cbar=True,
        annot_kws={"size": font_size},
        ax=ax
    )

    ax.set_title("Correlation Matrix", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    st.pyplot(fig)
    plt.close()
    

    # ---------------- TOP CORRELATIONS ----------------
    st.subheader("🔝 Strong Correlations")

    corr_pairs = (
        corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        .stack()
        .reset_index()
    )

    corr_pairs.columns = ["Column A", "Column B", "Correlation"]

    strong_corr = corr_pairs[abs(corr_pairs["Correlation"]) >= threshold]

    if strong_corr.empty:
        st.info("No strong correlations found.")
    else:
        strong_corr = strong_corr.sort_values(by="Correlation", key=abs, ascending=False)
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

# ---------------- BLOCK 14 — BAR CHART (FIXED) ----------------
st.header("🏷️ Bar Chart")

all_cols = df.columns.tolist()
bar_col = st.selectbox("Select column for bar chart:", all_cols)

data = df[bar_col].dropna()

if pd.api.types.is_numeric_dtype(data):
    bins = st.slider("Select number of bins:", 5, 50, 10)
    data = pd.cut(data, bins=bins)
    value_counts = data.value_counts().sort_index()
else:
    value_counts = data.value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor("#0f0f1a")
ax.set_facecolor("#0f0f1a")

ax.bar(value_counts.index.astype(str), value_counts.values,
       color="#7c3aed", edgecolor="#1e1b4b")

ax.set_title(f"Bar Chart of '{bar_col}'", color="white")
ax.tick_params(colors="#94a3b8")

plt.xticks(rotation=45, ha="right")

st.pyplot(fig)
plt.close()

st.divider()

# ---------------- BLOCK 15 — FOOTER ----------------
st.markdown(
    "<div style='text-align:center; color:gray;'>"
    "🍇 DOX v2.0 | Built by <b>Risi Nigarish</b> 👑"
    "</div>",
    unsafe_allow_html=True
)