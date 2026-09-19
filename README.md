# Supermarket Sales Analysis

A complete data analytics project for analyzing 500 supermarket sales transactions
across 4 branches in 4 Indian cities. Built as part of an internship data analytics
assignment.

---

## Project Overview

This project analyzes supermarket sales data to uncover insights about products,
branches, categories, customers, payments, and ratings. The analysis answers six
specific business questions stated in the project manual, and provides an
interactive Streamlit dashboard for exploring the data.

---

## Objective

- Analyze 500 supermarket sales transactions
- Calculate Sales = Quantity x Unit Price
- Identify best-performing branch, product, and category
- Understand customer type and payment behavior
- Analyze ratings and make business recommendations
- Verify calculated results against the manual's expected values

---

## Dataset

| Attribute | Detail |
|-----------|--------|
| Source | `SUPER MARKET DATA.pdf` |
| Rows | 500 transactions |
| Columns | Invoice ID, Date, Branch, City, Customer Type, Gender, Product, Category, Quantity, Unit Price, Payment, Rating, Sales |
| Date Range | January 2026 -- July 2026 |
| Branches | A (Jaipur), B (Delhi), C (Mumbai), D (Bengaluru) |
| Categories | Beverages, Personal Care, Dairy, Grocery, Snacks, Fruits, Bakery, Vegetables |
| Products | 20+ distinct products |
| Payment Methods | UPI, Card, Cash, Net Banking |

---

## Project Structure

```
project/
|-- SUPER MARKET DATA.pdf          # Original dataset PDF (do not modify)
|-- Supermarket Sales Analysis DA project.pdf  # Project manual (do not modify)
|-- app.py                         # Streamlit dashboard
|-- requirements.txt               # Python dependencies
|-- README.md                      # This file
|-- data/
|   |-- processed/
|       |-- supermarket_sales.csv  # Extracted & cleaned dataset
|-- src/
    |-- extract_data.py            # PDF extraction pipeline
    |-- analysis.py                # Analysis functions & manual verification
```

---

## Installation & Setup

### Prerequisites

- Python 3.9 or higher
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `pdfplumber` -- PDF table extraction
- `pandas` -- data processing
- `plotly` -- interactive charts
- `streamlit` -- web dashboard

---

## How to Run

### Step 1: Extract Data from PDF

Run the extraction script to produce the clean CSV from the dataset PDF:

```bash
python src/extract_data.py
```

This creates `data/processed/supermarket_sales.csv`.

The extraction validates:
- Row count (expected 500)
- Column count (expected 13)
- Numeric types
- Sales = Quantity x Unit Price
- Valid categorical values (Branch, City, Category, Payment, etc.)

### Step 2: Launch the Dashboard

```bash
streamlit run app.py
```

Open the URL shown (usually http://localhost:8501) in your browser.

The dashboard auto-extracts data if the CSV does not already exist.

---

## Data Extraction Methodology

The PDF `SUPER MARKET DATA.pdf` contains a structured table of 500 sales records.

**Primary extraction method:** `pdfplumber` table extraction
- pdfplumber identifies table regions on each PDF page and extracts structured rows/columns.
- Column headers are detected automatically.
- Rows are validated to start with a proper Invoice ID (`INV` + digits).

**Fallback method:** Regex text parsing
- If table extraction yields fewer than 10 valid rows, the script falls back to
  reading raw PDF text and applying regex patterns to reconstruct records.
- This handles PDFs where text is concatenated without structural table markers.

---

## Data Cleaning Methodology

After extraction, the pipeline:
1. Strips leading/trailing whitespace from all string columns.
2. Converts Quantity, Unit Price, Rating, and Sales to numeric (float/int).
3. Parses Date as datetime.
4. Drops completely empty rows.
5. Removes duplicate Invoice IDs (keeping first occurrence).
6. Reports missing values.
7. Validates Sales = Quantity x Unit Price (tolerance: 0.05).
8. Validates categorical columns against known valid values.

No source values are silently modified. Discrepancies are reported and preserved.

---

## Analysis Methodology

All results are computed directly from the extracted dataset. No analytical
values are hardcoded.

Key analyses:
- Total Sales, Transactions, Average Transaction Value, Average Rating
- Sales by Branch, Category, Product, Payment, Customer Type, Gender
- Monthly sales trend
- Ratings by Branch, Category, Payment Method
- Customer type spend comparison
- Heatmaps: Category x Branch, Product x Branch

---

## Sales Calculation

Sales = Quantity x Unit Price

This formula is applied during extraction validation and confirmed for all 500 rows.
The extracted Sales column in the PDF matches this formula for all records.

---

## Manual Result Verification

The project manual states 6 specific analytical results. All 6 are calculated
from the actual extracted dataset and compared against the manual's expectations.

| # | Question | Manual Expected | Actual (Dataset) | Match |
|---|----------|----------------|-----------------|-------|
| 1 | Highest-sales product | Cheese, Rs.27,906.30 | Cheese, Rs.27,906.30 | YES |
| 2 | Best-performing branch | Branch C (Mumbai), Rs.72,469.45 | Branch C (Mumbai), Rs.72,469.45 | YES |
| 3 | Highest-sales category | Beverages, Rs.56,108.24 | Beverages, Rs.56,108.24 | YES |
| 4 | Most popular payment | UPI, 127 transactions | UPI, 127 transactions | YES |
| 5 | Member vs Normal avg spend | Member Rs.483.14, Normal Rs.497.07 | Member Rs.483.14, Normal Rs.497.07 | YES |
| 6 | Average customer rating | 3.99 / 5 | 3.99 / 5 | YES |

**All 6 manual results match perfectly.**

Note: If any discrepancy were found, the dashboard would display both the
calculated value and the manual expectation, and the data would NOT be
manipulated to force a match.

---

## Dashboard Features

### Overview Tab
- KPI cards: Total Sales, Transactions, Avg/Transaction, Avg Rating, Best Branch, Top Category
- Monthly sales trend (line chart)
- Sales by category (bar chart)
- Auto-generated key insights

### Branches Tab
- Total sales by branch (bar + pie)
- Transactions by branch
- Average transaction value by branch
- Category sales heatmap by branch
- Branch summary table

### Products & Categories Tab
- Top 15 products by sales (horizontal bar)
- Category sales share (pie)
- Product x Branch sales heatmap
- Average quantity by category
- Full product summary table

### Customers Tab
- Member vs Normal: total sales and average transaction
- Gender sales share and avg transaction
- Category preference by customer type
- Customer type summary table

### Payments Tab
- Transaction share by payment method (pie)
- Total sales by payment method (bar)
- Payment usage by branch
- Payment preference by customer type
- Payment summary table

### Ratings Tab
- Average rating by category
- Average rating by branch
- Rating distribution (histogram)
- Average rating by payment method

### Manual Verification Tab
- All 6 manual results verified against actual data
- Clear pass/fail status for each check
- Full dataset preview table

### Sidebar Filters
- Branch, City, Category, Customer Type, Gender, Payment Method, Date Range
- All charts update dynamically based on active filters

---

## Key Findings

1. **Branch C (Mumbai) leads** with Rs.72,469.45 in total sales -- the best performer.
2. **Beverages is the top category** at Rs.56,108.24 -- nearly 23% of total revenue.
3. **Cheese generates the highest product revenue** at Rs.27,906.30.
4. **UPI is the most-used payment method** (127 transactions, ~25.4% of all transactions).
5. **Normal customers spend slightly more** per transaction (Rs.497.07) than Members (Rs.483.14) --
   suggesting the membership program may not be sufficiently incentivizing higher spend.
6. **Average rating is 3.99/5** -- moderate satisfaction; there is room to improve to 4.2+.

---

## Business Recommendations

1. **Stock management:** Prioritize inventory for Beverages and Cheese, which drive the most revenue.
2. **Branch improvement:** Investigate what makes Branch C (Mumbai) successful and replicate practices
   in Branch D (Bengaluru), which has the lowest sales.
3. **Membership program review:** Members spend slightly less on average than Normal customers --
   review and enhance membership benefits or discounts to increase member basket size.
4. **UPI promotion:** Since UPI is most popular, ensure UPI payment is always available and
   consider UPI-specific offers or cashback campaigns.
5. **Rating improvement:** At 3.99/5, customer satisfaction is below 4.0. Focus on service quality,
   product freshness (especially Dairy and Vegetables), and checkout speed.
6. **Seasonal campaigns:** Monthly sales show variation across Jan--Jul 2026. Identify peak months
   and plan promotions for slower months to smooth revenue.

---

## Assumptions

- The dataset PDF contains exactly the records to be analyzed (no additional pages excluded).
- Where pdfplumber extracted 500 rows matching expected structure, no manual correction was needed.
- "Sales" in the dataset is defined as Quantity x Unit Price with no tax or discount applied
  (confirmed: all 500 records satisfy this formula).
- Branch-to-City mapping is fixed: A=Jaipur, B=Delhi, C=Mumbai, D=Bengaluru.

---

## Discrepancies

None found. All 6 manual-stated results match the actual dataset exactly.

---

## PDF Extraction Notes

- pdfplumber successfully extracted all 500 records as a structured table on first attempt.
- No manual correction of extracted data was required.
- The regex fallback parser is available for PDFs where table structure is not preserved.
- Original PDFs are never modified by this project.

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pdfplumber | >=0.10.0 | PDF table extraction |
| pandas | >=2.0.0 | Data processing and analysis |
| plotly | >=5.18.0 | Interactive visualizations |
| streamlit | >=1.32.0 | Web dashboard |

---

## Reproducibility

The full analysis is reproducible from the two source PDFs:

```bash
# 1. Extract data
python src/extract_data.py

# 2. Verify analysis
python src/analysis.py

# 3. Run dashboard
streamlit run app.py
```

The CSV in `data/processed/` is a derived artifact and can be regenerated at any time.
