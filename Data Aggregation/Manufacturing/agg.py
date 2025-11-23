import pandas as pd

# -------------------------------------------------------
# 1. READ INPUT FILE
# -------------------------------------------------------
input_path = r"C:\P R O J E C T S\DAA PROJECT\Data Aggregation\Manufacturing\cleaned_manufacturing.csv"
df = pd.read_csv(input_path)

# -------------------------------------------------------
# 2. CONVERT DATE + EXTRACT MONTH
# -------------------------------------------------------
df["productiondate"] = pd.to_datetime(df["productiondate"], format="%d/%m/%Y", errors="coerce")
df["Month"] = df["productiondate"].dt.strftime("%b")  # Jan, Feb, Mar...

# -------------------------------------------------------
# 3. PRODUCTION PER MONTH
# -------------------------------------------------------
monthly_qty = df.groupby("Month")["producedqty"].sum().reset_index()

# Sort months correctly
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

monthly_qty["Month"] = pd.Categorical(monthly_qty["Month"], categories=month_order, ordered=True)
monthly_qty = monthly_qty.sort_values("Month")

# Final display table for sheet
production_per_month = pd.DataFrame({
    "ProductionPerMonth": monthly_qty["Month"],
    "Quantity": monthly_qty["producedqty"]
})

# -------------------------------------------------------
# 4. AVG PRODUCTION PER DAY
# -------------------------------------------------------
total_days = df["productiondate"].nunique()
avg_production_per_day = df["producedqty"].sum() / total_days

avg_day_table = pd.DataFrame({
    "Metric": ["Quantity"],
    "Value": [avg_production_per_day]
})

# -------------------------------------------------------
# 5. AVG PRODUCTION PER SHIFT
# -------------------------------------------------------
shift_avg = df.groupby("shift")["producedqty"].mean().reset_index()
shift_avg.columns = ["Shift", "Value"]

# Ensure order Morning → Afternoon → Night
shift_order = ["MORNING", "AFTERNOON", "NIGHT"]
shift_avg["Shift"] = pd.Categorical(shift_avg["Shift"], categories=shift_order, ordered=True)
shift_avg = shift_avg.sort_values("Shift")

# -------------------------------------------------------
# 6. TOTAL PRODUCTION
# -------------------------------------------------------
total_production = df["producedqty"].sum()

total_prod_table = pd.DataFrame({
    "Metric": ["TotalProduction"],
    "Value": [total_production]
})

# -------------------------------------------------------
# 7. SAVE OUTPUT TO EXCEL (matching your layout)
# -------------------------------------------------------
output_path = r"C:\P R O J E C T S\DAA PROJECT\Data Aggregation\production_aggregated.xlsx"

with pd.ExcelWriter(output_path) as writer:
    production_per_month.to_excel(writer, sheet_name="ProductionPerMonth", index=False)
    avg_day_table.to_excel(writer, sheet_name="AvgProductionPerDay", index=False)
    shift_avg.to_excel(writer, sheet_name="AvgProductionPerShift", index=False)
    total_prod_table.to_excel(writer, sheet_name="TotalProduction", index=False)

print("Manufacturing Aggregation Completed!")
print("Saved to:", output_path)
