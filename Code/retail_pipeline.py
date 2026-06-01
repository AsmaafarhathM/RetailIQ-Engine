import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

os.makedirs("Output", exist_ok=True)

file_path = "Data/USECASE - Data Engineering.xlsx"

# READ SOURCE FILES

product_df = pd.read_excel(
    file_path,
    sheet_name="PRODUCT DETAILS",
    header=3
)

retail1_df = pd.read_excel(
    file_path,
    sheet_name="RETAIL DATA 1",
    header=2
)

retail2_df = pd.read_excel(
    file_path,
    sheet_name="RETAIL DATA 2",
    header=4
)

print("\nProduct Columns")
print(product_df.columns.tolist())

print("\nRetail1 Columns")
print(retail1_df.columns.tolist())

print("\nRetail2 Columns")
print(retail2_df.columns.tolist())

print("\nProduct Details Shape:")
print(product_df.shape)

print("\nRetail Data 1 Shape:")
print(retail1_df.shape)

print("\nRetail Data 2 Shape:")
print(retail2_df.shape)

# BRONZE LAYER

bronze_df = pd.concat(
    [retail1_df, retail2_df],
    ignore_index=True
)

print("\nCombined Bronze Layer Shape:")
print(bronze_df.shape)

print("\nMissing Values:")
print(bronze_df.isnull().sum())

print("\nDuplicate Records:")
print(bronze_df.duplicated().sum())

bronze_df = bronze_df.loc[
    :,
    ~bronze_df.columns.str.contains("^Unnamed")
]

bronze_df.to_csv(
    "Output/bronze_data.csv",
    index=False
)

print("\nBronze Layer Saved Successfully!")

# ----------------------------
# SILVER LAYER
# ----------------------------

silver_df = bronze_df.copy()

before_count = len(silver_df)

silver_df = silver_df.drop_duplicates()

after_count = len(silver_df)

duplicates_removed = before_count - after_count

print(f"\nDuplicates Removed: {duplicates_removed}")

# Save missing price count before fixing
missing_prices_before = silver_df['price'].isnull().sum()

# Recover Missing Prices
silver_df = silver_df.merge(
    product_df[['product_id', 'price']],
    on='product_id',
    how='left',
    suffixes=('', '_master')
)

silver_df['price'] = silver_df['price'].fillna(
    silver_df['price_master']
)

silver_df.drop(
    columns=['price_master'],
    inplace=True
)

print("\nMissing Prices After Recovery:")
print(silver_df['price'].isnull().sum())

# Standardize Product Names
silver_df['product_name'] = (
    silver_df['product_name']
    .astype(str)
    .str.strip()
    .str.title()
)

# Standardize Categories
silver_df['category'] = (
    silver_df['category']
    .astype(str)
    .str.strip()
    .str.title()
)

category_mapping = {
    'Elec': 'Electronics',
    'Furn': 'Furniture',
    'Cloth': 'Clothing',
    'Home': 'Home Appliances'
}

silver_df['category'] = (
    silver_df['category']
    .replace(category_mapping)
)

print("\nUnique Categories After Mapping:")
print(silver_df['category'].unique())

# Standardize City
silver_df['city'] = (
    silver_df['city']
    .astype(str)
    .str.strip()
    .str.title()
)

# Convert Date
silver_df['transaction_date'] = pd.to_datetime(
    silver_df['transaction_date']
)

# DATA PRIVACY

def mask_email(email):

    email = str(email)

    if "@" not in email:
        return email

    name, domain = email.split("@")

    return name[:2] + "****@" + domain

silver_df['email'] = (
    silver_df['email']
    .apply(mask_email)
)

def mask_phone(phone):
    phone = str(phone)
    return phone[:2] + "******" + phone[-2:]

silver_df['phone'] = (
    silver_df['phone']
    .apply(mask_phone)
)

print("\nSilver Layer Missing Values:")
print(silver_df.isnull().sum())

silver_df.to_csv(
    "Output/silver_data.csv",
    index=False
)

print("\nSilver Layer Saved Successfully!")

# GOLD LAYER

gold_df = silver_df.copy()

gold_df['revenue'] = (
    gold_df['price']
    * gold_df['quantity']
    * (1 - gold_df['discount'])
)

gold_df['year'] = (
    gold_df['transaction_date']
    .dt.year
)

gold_df['month'] = (
    gold_df['transaction_date']
    .dt.month_name()
)

gold_df['month_num'] = (
    gold_df['transaction_date']
    .dt.month
)

gold_df['quarter'] = (
    gold_df['transaction_date']
    .dt.quarter
)

print("\nTotal Revenue:")
print(round(gold_df['revenue'].sum(), 2))

print("\nRevenue By Category:")
print(
    gold_df.groupby('category')['revenue']
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue By City:")
print(
    gold_df.groupby('city')['revenue']
    .sum()
    .sort_values(ascending=False)
)

print("\nTop Products:")
print(
    gold_df.groupby('product_name')['revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nKPI Summary")

print(
    "Total Orders:",
    gold_df['transaction_id'].nunique()
)

print(
    "Total Customers:",
    gold_df['customer_id'].nunique()
)

print(
    "Total Revenue:",
    round(gold_df['revenue'].sum(), 2)
)

# DATA QUALITY CHECKS

assert silver_df['price'].isnull().sum() == 0, \
    "Price column still contains null values"

assert gold_df['revenue'].isnull().sum() == 0, \
    "Revenue column contains null values"

assert gold_df['transaction_id'].nunique() > 0, \
    "No transactions found"

print("\nData Quality Checks Passed!")

gold_df.to_csv(
    "Output/gold_data.csv",
    index=False
)

print("\nGold Layer Saved Successfully!")

# LOAD GOLD LAYER INTO MYSQL

load_dotenv()

engine = create_engine(
    f"mysql+mysqlconnector://"
    f"{os.getenv('MYSQL_USER')}:"
    f"{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}/"
    f"{os.getenv('MYSQL_DATABASE')}"
)

gold_df.to_sql(
    "gold_sales",
    con=engine,
    if_exists="replace",
    index=False
)

print("\nMySQL Table Created Successfully!")

assert len(gold_df) > 0, \
    "Gold table is empty"

print("Database Validation Passed!")

# DATA QUALITY REPORT

data_quality_report = {
    "Total Records": len(bronze_df),
    "Duplicates Removed": duplicates_removed,
    "Missing Prices Fixed": missing_prices_before,
    "Emails Masked": len(silver_df),
    "Phones Masked": len(silver_df)
}

print("\nData Quality Report")

for k, v in data_quality_report.items():
    print(f"{k}: {v}")

dq_df = pd.DataFrame(
    list(data_quality_report.items()),
    columns=["Metric", "Value"]
)

dq_df.to_csv(
    "Output/data_quality_report.csv",
    index=False
)

print("\nData Quality Report Saved Successfully!")