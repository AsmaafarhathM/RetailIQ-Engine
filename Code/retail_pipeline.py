import pandas as pd

file_path = "Data/USECASE - Data Engineering.xlsx"

xls = pd.ExcelFile(file_path)

# print("Available Sheets:")
# print(xls.sheet_names)

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

bronze_df = pd.concat(
    [retail1_df, retail2_df],
    ignore_index=True
)
#create and save bronze layer
print("\nCombined Bronze Layer Shape:")
print(bronze_df.shape)

bronze_df.to_csv(
    "Output/bronze_data.csv",
    index=False
)

print("\nBronze Layer Saved Successfully!")

print("\nMissing Values:")
print(bronze_df.isnull().sum())

print("\nDuplicate Records:")
print(bronze_df.duplicated().sum())

print("\nColumns:")
print(bronze_df.columns.tolist())

bronze_df = bronze_df.loc[
    :,
    ~bronze_df.columns.str.contains("^Unnamed")
]

print(bronze_df.columns)

silver_df = bronze_df.copy()

print("\nMissing Values:")
print(
    silver_df.isnull().sum()
    .sort_values(ascending=False)
)
#silver layer creation
silver_df = bronze_df.copy()

before_count = len(silver_df)

silver_df = silver_df.drop_duplicates()

after_count = len(silver_df)

duplicates_removed = before_count - after_count

print(f"\nDuplicates Removed: {duplicates_removed}")

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
print(
    silver_df['price'].isnull().sum()
)

silver_df['product_name'] = (
    silver_df['product_name']
    .astype(str)
    .str.strip()
    .str.title()
)

silver_df['category'] = (
    silver_df['category']
    .astype(str)
    .str.strip()
    .str.title()
)

silver_df['transaction_date'] = pd.to_datetime(
    silver_df['transaction_date']
)

def mask_email(email):

    name, domain = str(email).split("@")

    return name[:2] + "****@" + domain

silver_df['email'] = (
    silver_df['email']
    .apply(mask_email)
)

def mask_phone(phone):

    phone = str(phone)

    return (
        phone[:2]
        + "******"
        + phone[-2:]
    )

silver_df['phone'] = (
    silver_df['phone']
    .apply(mask_phone)
)

print("\nSilver Layer Missing Values:")
print(
    silver_df.isnull().sum()
)

silver_df.to_csv(
    "Output/silver_data.csv",
    index=False
)

print("\nSilver Layer Saved Successfully!")

#gold layer creation
gold_df = silver_df.copy()

gold_df['revenue'] = (
    gold_df['price']
    *
    gold_df['quantity']
    *
    (1 - gold_df['discount'])
)

gold_df['year'] = (
    gold_df['transaction_date']
    .dt.year
)

gold_df['month'] = (
    gold_df['transaction_date']
    .dt.month_name()
)

gold_df['quarter'] = (
    gold_df['transaction_date']
    .dt.quarter
)

print("\nTotal Revenue:")
print(
    round(
        gold_df['revenue'].sum(),
        2
    )
)

print("\nRevenue By Category:")

print(
    gold_df.groupby('category')
    ['revenue']
    .sum()
    .sort_values(
        ascending=False
    )
)

print("\nRevenue By City:")

print(
    gold_df.groupby('city')
    ['revenue']
    .sum()
    .sort_values(
        ascending=False
    )
)

print("\nTop Products:")

print(
    gold_df.groupby('product_name')
    ['revenue']
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)

print("\nKPI Summary")

print(
    "Total Orders:",
    gold_df['transaction_id']
    .nunique()
)

print(
    "Total Customers:",
    gold_df['customer_id']
    .nunique()
)

print(
    "Total Revenue:",
    round(
        gold_df['revenue']
        .sum(),
        2
    )
)

gold_df.to_csv(
    "Output/gold_data.csv",
    index=False
)

print(
    "\nGold Layer Saved Successfully!"
)

category_mapping = {
    'Elec': 'Electronics',
    'Furn': 'Furniture',
    'Cloth': 'Clothing',
    'Home': 'Home Appliances'
}

silver_df['category'] = silver_df['category'].replace(category_mapping)

silver_df['category'] = (
    silver_df['category']
    .astype(str)
    .str.strip()
    .str.title()
)

data_quality_report = {
    "Total Records": len(bronze_df),
    "Duplicates Removed": duplicates_removed,
    "Missing Prices Fixed": 809,
    "Emails Masked": len(silver_df),
    "Phones Masked": len(silver_df)
}

print("\nData Quality Report")

for k, v in data_quality_report.items():
    print(f"{k}: {v}")