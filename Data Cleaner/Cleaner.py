import os
import glob
import pandas as pd
import numpy as np
from dateutil.parser import parse

# -----------------------
# Helper functions
# -----------------------

def looks_like_date(value):
    try:
        parse(str(value), dayfirst=True)
        return True
    except:
        return False

def standardize_colnames(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    return df

def convert_dates(df):
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
            df[col] = df[col].dt.strftime("%d/%m/%Y")
    return df

def convert_numeric_by_name(df):
    money_keys = ["salary", "revenue", "cost", "amount", "sales", "price", "total"]
    for col in df.columns:
        if any(k in col.lower() for k in money_keys):
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "")
                .str.replace(r"[^\d.\-]", "", regex=True)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
            if df[col].notna().any():
                df[col].fillna(df[col].median(), inplace=True)
    return df

def convert_percent_columns(df):
    for col in df.columns:
        if "%" in col or "percent" in col.lower() or "pct" in col.lower():
            df[col] = df[col].astype(str).str.replace("%", "").str.strip()
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def fill_text_modes(df):
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()
            df[col].replace({"": np.nan, "nan": np.nan, "None": np.nan}, inplace=True)
            if df[col].isna().sum() > 0:
                mode = df[col].mode()
                if not mode.empty:
                    df[col].fillna(mode.iloc[0], inplace=True)
    return df

def auto_detect_and_convert(df):
    for col in df.columns:
        series = df[col].astype(str).str.strip()
        non_null = series[series.notna() & (series != "nan")]

        if len(non_null) == 0:
            continue

        numeric_like = non_null.str.replace(".", "", 1).str.replace("-", "", 1).str.isnumeric().sum()

        if numeric_like > 0.6 * len(series):
            df[col] = pd.to_numeric(series, errors="coerce")
            if df[col].notna().any():
                df[col].fillna(df[col].median(), inplace=True)
        else:
            sample = non_null.head(5)
            if len(sample) > 0 and all(looks_like_date(v) for v in sample):
                df[col] = pd.to_datetime(series, dayfirst=True, errors="coerce")
                df[col] = df[col].dt.strftime("%d/%m/%Y")
            else:
                df[col] = series.replace("nan", np.nan)

    return df

def clean_dataframe(df):
    df = standardize_colnames(df)
    df.replace(["", " ", "NA", "N/A", "--", "null", "None"], np.nan, inplace=True)
    df.drop_duplicates(inplace=True)

    df = auto_detect_and_convert(df)
    df = convert_dates(df)
    df = convert_numeric_by_name(df)
    df = convert_percent_columns(df)
    df = fill_text_modes(df)

    df.drop_duplicates(inplace=True)
    return df

# -----------------------
# Main Cleaning Function
# -----------------------

def process_csvs():
    # Folder where this script lives
    script_folder = os.path.dirname(os.path.abspath(__file__))

    # Parent = DAAproject
    parent_folder = os.path.dirname(script_folder)

    # Output folder = cleaned data
    output_folder = os.path.join(parent_folder, "cleaned data")

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Find CSV files in datacleaner folder
    csv_files = glob.glob(os.path.join(script_folder, "*.csv"))

    print(f"Found {len(csv_files)} CSV files in datacleaner folder.\n")

    for file in csv_files:
        name = os.path.basename(file)
        print(f"Cleaning: {name}")

        try:
            df = pd.read_csv(file, dtype=str)
        except Exception as e:
            print(f"ERROR reading {name}: {e}")
            continue

        cleaned = clean_dataframe(df)

        output_path = os.path.join(output_folder, "cleaned_" + name)
        cleaned.to_csv(output_path, index=False)

        print(f"Saved cleaned file -> {output_path}\n")

    print("All files cleaned successfully!")

# -----------------------
# Run
# -----------------------

if __name__ == "__main__":
    process_csvs()
