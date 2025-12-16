# Intern-Data-Engineer

This repository contains the solutions for various data engineering tasks completed during my internship. Each task demonstrates skills in data processing, database management, Python programming, web development, and data visualization.

## Repository Structure

Data Engineer Intern/
├── task1 # Data ingestion and transformation
├── task2 # File processing and checksum calculation
├── task3 # Web method for lowest common multiple
├── task4 # Data cleaning, aggregation, and visualization
├── task5 # Google Spreadsheet realistic data generator
├── task6 # Web application for generating fake user data


---

## Task Overview

### **Task 1** – Data Ingestion and Transformation
- Processed non-standard JSON (`task1_d.json`) and ingested it into a relational database.
- Generated a summary table with:
  - `publication_year`
  - `book_count` published that year
  - `average_price` (in USD, rounded to cents, conversion rate €1 = $1.2)
- Transformations were performed inside the database using SQL.

### **Task 2** – File Hashing and Sorting
- Calculated **SHA3-256** for all files in the provided archive.
- Sorted hashes by the product of hex digits (increased by one).
- Concatenated sorted hashes, appended email, and calculated final SHA3-256.
- Result submitted to Discord as per instructions.

### **Task 3** – Web Method for LCM
- Implemented an HTTP GET web method to compute **Lowest Common Multiple (LCM)** of two natural numbers `x` and `y`.
- Returns `NaN` for invalid inputs.
- Deployed the method with URL structured using email: http://yourserver.com/app/your_email_formatted?x={}&y={}


### **Task 4** – Data Cleaning, Aggregation, and Visualization
- Loaded data from `DATA1`, `DATA2`, and `DATA3`.
- Cleaned data: parsed dates, handled duplicates, missing and malformed values.
- Added `paid_price` column (`quantity * unit_price`, converted to USD).
- Extracted year, month, day from timestamps.
- Calculated:
  1. Top 5 days by daily revenue.
  2. Number of unique real users (reconciled aliases, addresses, phones, etc.).
  3. Number of unique author sets.
  4. Most popular author or author set.
  5. Top customer by total spending (considering multiple aliases).
- Plotted daily revenue chart using matplotlib.
- Dashboard with three tabs/views for each dataset.

### **Task 5** – Google Spreadsheet Data Generator
- Created a spreadsheet generating realistic daily mine resource data.
- Features:
  - Customizable mine names and date range.
  - Uniform and normal distributions with adjustable parameters.
  - Smoothing, day-of-week effects, trends, and event spikes/drops.
  - Dynamic charts reflecting parameter changes.
- [Link to Task 5 Spreadsheet](https://intern-data-engineer-git-main-manish-rais-projects-570d7f51.vercel.app?_vercel_share=EbJZclEtv8PIxghl1QRbeszNzbiKw1vu)

### **Task 6** – Web Application for Fake User Data
- Web app allows batch generation of fake users using SQL stored procedures.
- Users can select locale (English/USA, German/Germany) and seed.
- Generated data per user:
  - Full name, address, geolocation, physical attributes, phone, email.
- Deterministic random generation based on locale, seed, batch index, and position.
- Database designed for extensibility with large lookup tables.
- [Link to Task 6 Web Application](https://fake-user-generator-fvqv.onrender.com/?locale=de_DE&seed=cake&batch_size=20)

---

## Tools & Technologies
- **Python**: pandas, matplotlib, Flask
- **Databases**: PostgreSQL / MySQL
- **Big Data / ETL**: SQL, stored procedures
- **Web**: HTTP GET methods, simple dashboard
- **Other**: Google Spreadsheets (formulas), SHA3-256 hashing

---

## How to Run
1. Clone the repository:
```bash
git clone https://github.com/yourusername/Data-Engineer-Intern.git
