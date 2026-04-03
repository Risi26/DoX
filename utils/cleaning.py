import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler


# ─────────────────────────────────────────
# BLOCK 1 — ADVANCED DATA CLEANING (FINAL)
# ─────────────────────────────────────────


def get_numerical_columns(df: pd.DataFrame) -> list:
    """Select only numerical columns."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def compute_skewness(df: pd.DataFrame, columns: list) -> dict:
    """Compute skewness for each column."""
    return {col: df[col].skew() for col in columns}


def flag_outliers(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Flag outliers using dynamic method:
    - Z-score if distribution ~ normal
    - IQR if skewed
    Returns column-wise boolean mask
    """
    outlier_mask = pd.DataFrame(False, index=df.index, columns=columns)
    skewness = compute_skewness(df, columns)

    for col in columns:
        col_data = df[col].fillna(df[col].median())  # FIX: handle NaN safely
        skew_val = skewness[col]

        if -0.5 <= skew_val <= 0.5:
            # Z-score method
            std = col_data.std()
            if std == 0:
                continue  # skip constant columns
            z_scores = np.abs((col_data - col_data.mean()) / std)
            outlier_mask[col] = z_scores > 3

        else:
            # IQR method
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1

            if IQR == 0:
                continue  # skip constant columns

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outlier_mask[col] = (col_data < lower) | (col_data > upper)

    return outlier_mask


def remove_outliers(
    df: pd.DataFrame,
    outlier_mask: pd.DataFrame,
    threshold: int = 1
) -> pd.DataFrame:
    """
    Remove rows where number of outlier columns exceeds threshold.
    Default threshold=1 → removes rows with >1 outlier columns
    """
    outlier_counts = outlier_mask.sum(axis=1)
    rows_to_remove = outlier_counts > threshold
    return df.loc[~rows_to_remove].reset_index(drop=True)


def normalize_data(
    df: pd.DataFrame,
    columns: list,
    method: str = "standard",
    exclude: list = None
) -> pd.DataFrame:
    """
    Normalize numerical columns.
    - method: 'standard' or 'minmax'
    - exclude: columns to skip (e.g., target column)
    """
    df_normalized = df.copy()

    if exclude:
        columns = [col for col in columns if col not in exclude]

    if not columns:
        return df_normalized

    scaler = MinMaxScaler() if method == "minmax" else StandardScaler()
    df_normalized[columns] = scaler.fit_transform(df_normalized[columns])

    return df_normalized


def run_cleaning_pipeline(
    df: pd.DataFrame,
    outlier_tolerance: int = 1,    # 🔥 MATCHES APP.PY
    apply_removal: bool = False,   # 🔥 MATCHES APP.PY
    normalize_method: str = "standard",
    exclude_cols: list = None
) -> dict:
    """
    Master pipeline for Block 1
    """

    # 🔥 FIX 1: Global missing value handling
    df = df.copy()
    df = df.fillna(df.median(numeric_only=True))

    # Step 1: Numerical columns
    num_cols = get_numerical_columns(df)

    # Step 2: Skewness
    skewness_report = compute_skewness(df, num_cols)

    # Step 3: Outlier detection
    outlier_mask = flag_outliers(df, num_cols)
    
    # 🔥 FIX 2: Calculate row outlier counts for the Streamlit UI
    row_outlier_counts = outlier_mask.sum(axis=1)

    # Step 4: Optional removal (threshold-based using outlier_tolerance)
    if apply_removal:
        cleaned_df = remove_outliers(df, outlier_mask, threshold=outlier_tolerance)
    else:
        cleaned_df = df.copy()

    # 🔥 FIX 3: Recompute columns after cleaning
    clean_num_cols = get_numerical_columns(cleaned_df)

    # Step 5: Normalization (with exclusion support)
    normalized_df = normalize_data(
        cleaned_df,
        clean_num_cols,
        method=normalize_method,
        exclude=exclude_cols
    )

    # Step 6: Summary (Kept as a Pandas Series so app.py can use .reset_index())
    outlier_summary = outlier_mask.sum()

    # 🔥 FIX 4: Return all the keys that app.py is expecting!
    return {
        "cleaned_df": cleaned_df,
        "outlier_mask": outlier_mask,
        "normalized_df": normalized_df,
        "skewness_report": skewness_report,
        "outlier_summary": outlier_summary,
        "row_outlier_counts": row_outlier_counts # App.py needs this!
    }