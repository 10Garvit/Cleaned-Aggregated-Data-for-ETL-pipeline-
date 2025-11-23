import pandas as pd

# READ CLEANED CSV
input_path = r"C:\P R O J E C T S\DAA PROJECT\Data Aggregation\Field\cleaned_field.csv"
df = pd.read_csv(input_path)

# ------------------------
# EXTRACT MONTH FROM failuredate
# ------------------------
df["failuredate"] = pd.to_datetime(df["failuredate"], format="%d/%m/%Y", errors="coerce")

df["Month"] = df["failuredate"].dt.strftime("%b")   # Jan, Feb, Mar...

# ------------------------
# 1. FAILURES PER MONTH
# ------------------------
failures_per_month = df.groupby("Month").size().reset_index(name="Count")

# ------------------------
# 2. FAILURE MODE (%)
# ------------------------
failure_mode = df["failuremode"].value_counts(normalize=True) * 100
failure_mode = failure_mode.reset_index()
failure_mode.columns = ["FailureMode", "Percentage"]

# ------------------------
# 3. SEVERITY (%)
# ------------------------
severity = df["severity"].value_counts(normalize=True) * 100
severity = severity.reset_index()
severity.columns = ["SeverityMode", "Percentage"]

# ------------------------
# 4. REPORTED BY (%)
# ------------------------
reported_by = df["reportedby"].value_counts(normalize=True) * 100
reported_by = reported_by.reset_index()
reported_by.columns = ["ReportedBy", "Percentage"]

# ------------------------
# SAVE OUTPUT
# ------------------------
output_path = r"C:\P R O J E C T S\DAA PROJECT\Data Aggregation\field_aggregated.xlsx"

with pd.ExcelWriter(output_path) as writer:
    failures_per_month.to_excel(writer, sheet_name="FailurePerMonth", index=False)
    failure_mode.to_excel(writer, sheet_name="FailureMode%", index=False)
    severity.to_excel(writer, sheet_name="Severity%", index=False)
    reported_by.to_excel(writer, sheet_name="ReportedBy%", index=False)

print("Aggregation complete! Saved to:", output_path)
