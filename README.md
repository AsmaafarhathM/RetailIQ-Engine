# RetailIQ Engine – End-to-End Retail Data Engineering & Analytics Pipeline

## Project Overview

RetailIQ Engine is an end-to-end Data Engineering and Analytics project designed to process retail transaction data and generate business insights through automated ETL pipelines and interactive Power BI dashboards.

The project follows a modern **Bronze → Silver → Gold** data architecture, performs data quality checks, data standardization, PII masking, revenue calculations, and stores curated data in MySQL for analytics and reporting.

---

## Architecture

```text
Excel Source Data
        │
        ▼
Python ETL Pipeline
        │
        ▼
Bronze Layer
(Raw Combined Data)
        │
        ▼
Silver Layer
(Data Cleaning &
Standardization)
        │
        ▼
Gold Layer
(Business Metrics &
Analytics Dataset)
        │
        ▼
MySQL Database
        │
        ▼
Power BI Dashboards
```

---

## Features

### Data Ingestion

* Reads data from multiple Excel sheets
* Product Details
* Retail Data 1
* Retail Data 2

### Bronze Layer

* Combines retail datasets
* Stores raw integrated data
* Generates bronze_data.csv

### Silver Layer

Data cleaning and transformation:

* Duplicate removal
* Missing price recovery using Product Master
* Category standardization
* Product name standardization
* City standardization
* Date conversion
* Email masking
* Phone number masking

### Gold Layer

Business-ready analytics dataset:

* Revenue calculation
* Year extraction
* Month extraction
* Quarter extraction
* KPI generation
* Revenue analysis

### Data Quality Checks

* Missing value validation
* Duplicate record validation
* Gold layer validation
* Data quality reporting

### Database Integration

* Automatic MySQL table creation
* Gold layer loading into MySQL
* Validation after load

### Automation

* Cron Job based ETL execution
* Automatic refresh every 5 minutes

---

## Tech Stack

| Component       | Technology   |
| --------------- | ------------ |
| Language        | Python       |
| Data Processing | Pandas       |
| Excel Reading   | OpenPyXL     |
| Database        | MySQL        |
| Scheduling      | Cron Jobs    |
| Visualization   | Power BI     |
| Version Control | Git & GitHub |

---

## Project Structure

```text
RetailIQ-Engine
│
├── Code
│   └── retail_pipeline.py
│
├── Data
│   └── USECASE - Data Engineering.xlsx
│
├── Output
│   ├── bronze_data.csv
│   ├── silver_data.csv
│   ├── gold_data.csv
│   ├── data_quality_report.csv
│   └── retailiq.db
│
├── PowerBI
│   └── Dashboard Files
│
├── Documentation
│   └── Project Documents
│
├── requirements.txt
├── .gitignore
└── README.md
```

> **Note:** Files under `Output/` are produced by `python Code/retail_pipeline.py` (run from the project root). Commit updated outputs after re-running the pipeline when source data or transforms change.

---

## ETL Workflow

### Step 1: Extract

Data is extracted from:

```text
PRODUCT DETAILS
RETAIL DATA 1
RETAIL DATA 2
```

Excel sheets using Pandas.

---

### Step 2: Transform

#### Data Cleaning

* Remove duplicate records
* Handle missing values
* Standardize categories

#### Data Enrichment

Missing product prices are recovered from Product Master.

#### Privacy Protection

Email Example:

```text
Before:
johnsmith@gmail.com

After:
jo****@gmail.com
```

Phone Example:

```text
Before:
9876543210

After:
98******10
```

---

### Step 3: Load

Data is loaded into:

```text
MySQL Database
Database Name: retailiq
Table Name: gold_sales
```

---

## Business KPIs

The project calculates:

### Revenue

```text
Revenue =
Price × Quantity × (1 - Discount)
```

### Metrics

* Total Revenue
* Total Orders
* Total Customers
* Revenue by Category
* Revenue by City
* Top Products
* Payment Analytics
* Customer Analytics

---

## Power BI Dashboards

### Page 1 – Executive Dashboard

Provides a high-level business overview.

#### KPIs

* Total Revenue
* Total Orders
* Total Customers
* Total Quantity Sold

#### Visuals

* Revenue by Category
* Revenue by City
* Monthly Revenue Trend
* Top Products by Revenue
* Orders by Payment Method
* Orders by Payment Status

---

### Page 2 – Product Performance Dashboard

Provides product-level analytics.

#### KPIs

* Total Product Revenue
* Total Products Sold

#### Visuals

* Revenue by Product
* Quantity Sold by Product
* Revenue Share by Category
* Product Revenue Contribution

---

### Page 3 – Customer & Payment Insights

Provides customer and transaction insights.

#### KPIs

* Total Customers
* Total Orders
* Failed Transactions

#### Visuals

* Customers by City
* Orders by Payment Status
* Revenue by Payment Method
* Orders by Payment Method

---

## Data Privacy & Governance

Sensitive customer information is protected through masking.

### Email Masking

```text
jo****@gmail.com
```

### Phone Masking

```text
98******10
```

This ensures compliance with basic data privacy practices.

---

## Data Quality Report

Generated automatically after ETL execution.

Includes:

* Total Records
* Duplicates Removed
* Missing Prices Fixed
* Emails Masked
* Phones Masked

Output:

```text
data_quality_report.csv
```

---

## Setup & Run

```bash
cd RetailIQ-Engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your MySQL credentials
python Code/retail_pipeline.py
```

Required environment variables (see `.env.example`):

* `MYSQL_USER`
* `MYSQL_PASSWORD`
* `MYSQL_HOST`
* `MYSQL_DATABASE`

---

##  Automation

Cron Job executes the ETL pipeline every 5 minutes.

Example:

```bash
*/5 * * * * cd "/path/to/RetailIQ-Engine" && python3 Code/retail_pipeline.py >> "/path/to/RetailIQ-Engine/cron.log" 2>&1
```

This automatically:

* Reads latest Excel data
* Rebuilds Bronze Layer
* Rebuilds Silver Layer
* Rebuilds Gold Layer
* Updates MySQL

---

## Key Achievements

✅ Built an end-to-end ETL pipeline

✅ Implemented Bronze-Silver-Gold architecture

✅ Automated data quality checks

✅ Implemented PII masking

✅ Integrated MySQL as analytical storage

✅ Created interactive Power BI dashboards

✅ Automated pipeline execution using Cron Jobs

✅ Generated business KPIs and insights

---

##  Author

**Asmaa Farhath M**

