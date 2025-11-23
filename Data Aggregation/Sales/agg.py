import pandas as pd

# -----------------------------
# 1. READ INPUT FILE
# -----------------------------
input_path = r"C:\P R O J E C T S\DAA PROJECT\Data Aggregation\Sales\cleaned_sales.csv"
df = pd.read_csv(input_path)

# -----------------------------
# 2. CONVERT DATE + EXTRACT MONTH
# -----------------------------
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
df["Month"] = df["date"].dt.strftime("%b")   # Jan, Feb, Mar...

# -----------------------------
# 3. SALES PER MONTH
# -----------------------------
sales_per_month_qty = df.groupby("Month")["qty"].sum()
sales_per_month_price = df.groupby("Month")["totalprice"].sum()

sales_per_month = pd.DataFrame({
    "Month": sales_per_month_qty.index,
    "Quantity": sales_per_month_qty.values,
    "Price": sales_per_month_price.values
})

# -----------------------------
# 4. AVG SALES PER DAY
# -----------------------------
total_days = df["date"].nunique()

avg_qty_per_day = df["qty"].sum() / total_days
avg_price_per_day = df["totalprice"].sum() / total_days

avg_sales_per_day = pd.DataFrame({
    "Metric": ["Quantity", "Price"],
    "Value": [avg_qty_per_day, avg_price_per_day]
})

# -----------------------------
# 5. TOTAL SALE
# -----------------------------
total_sale = pd.DataFrame({
    "Metric": ["TotalSale"],
    "Value": [df["totalprice"].sum()]
})

# -----------------------------
# 6. SAVE OUTPUT FILE
# -----------------------------
output_path = r"C:\P R O J E C T S\DAA PROJECT\Data Aggregation\sales_aggregated.xlsx"

with pd.ExcelWriter(output_path) as writer:
    sales_per_month.to_excel(writer, sheet_name="SalesPerMonth", index=False)
    avg_sales_per_day.to_excel(writer, sheet_name="AvgSalesPerDay", index=False)
    total_sale.to_excel(writer, sheet_name="TotalSale", index=False)

print("Sales aggregation completed! Saved to:", output_path)
