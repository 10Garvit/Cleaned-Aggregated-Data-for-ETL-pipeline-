import pandas as pd

# ------------------------------------------------------------
# 1. READ INPUT FILE
# ------------------------------------------------------------
input_path = r"C:\P R O J E C T S\DAA PROJECT\Data Aggregation\Testing\cleaned_testing.csv"
df = pd.read_csv(input_path)

# ------------------------------------------------------------
# 2. EXTRACT MONTH FROM testdate
# ------------------------------------------------------------
df["testdate"] = pd.to_datetime(df["testdate"], format="%d/%m/%Y", errors="coerce")
df["Month"] = df["testdate"].dt.strftime("%b")

# ------------------------------------------------------------
# 3. NUMBER OF TESTS PER MONTH
# ------------------------------------------------------------
monthly_tests = df.groupby("Month").size().reset_index(name="Quantity")

# Ensure correct month order
month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly_tests["Month"] = pd.Categorical(monthly_tests["Month"], categories=month_order, ordered=True)
monthly_tests = monthly_tests.sort_values("Month")

# ------------------------------------------------------------
# 4. AVG TESTS PER DAY
# ------------------------------------------------------------
total_days = df["testdate"].nunique()
avg_tests_per_day = len(df) / total_days

avg_tests_table = pd.DataFrame({
    "Metric": ["Quantity"],
    "Value": [avg_tests_per_day]
})

# ------------------------------------------------------------
# 5. TOTAL NO. OF TESTS + FAIL%
# ------------------------------------------------------------
total_tests = len(df)
fail_percentage = (df["status"].value_counts().get("FAIL", 0) / total_tests) * 100

totals_table = pd.DataFrame({
    "Metric": ["TotalTests", "Fail%"],
    "Value": [total_tests, fail_percentage]
})

# ------------------------------------------------------------
# 6. TEST-WISE FAIL% + AVG MEASUREMENT VALUE + UNIT
# ------------------------------------------------------------
test_group = df.groupby("testname")

test_table = pd.DataFrame({
    "Test Name": test_group.size().index,
    "Fail%": (test_group.apply(lambda x: (x["status"]=="FAIL").sum()) /
              test_group.size()) * 100,
    "Average Measurement Value": test_group["measurementvalue"].mean(),
    "Unit": test_group["unit"].first()
})

# ------------------------------------------------------------
# 7. SAVE OUTPUT
# ------------------------------------------------------------
output_path = r"C:\P R O J E C T S\DAA PROJECT\Data Aggregation\testing_aggregated.xlsx"

with pd.ExcelWriter(output_path) as writer:
    monthly_tests.to_excel(writer, sheet_name="TestsPerMonth", index=False)
    avg_tests_table.to_excel(writer, sheet_name="AvgTestsPerDay", index=False)
    totals_table.to_excel(writer, sheet_name="TotalTests_Fail%", index=False)
    test_table.to_excel(writer, sheet_name="TestDetails", index=False)

print("Testing Aggregation Completed!")
print("Saved to:", output_path)
