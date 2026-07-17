# ETL Pipeline - Superstore Data Warehouse

## Project Overview

This project implements an ETL (Extract, Transform, Load) pipeline for the Superstore dataset using Python, Docker, and PostgreSQL.

The pipeline performs the following tasks:

- Extracts data from the Superstore CSV file
- Cleans and transforms the data
- Creates dimension tables
- Creates the fact table
- Loads all data into a PostgreSQL data warehouse

---

## Requirements

Before running the project, install:

- Docker Desktop
- Docker Compose

---

## Project Structure

```
ETL-pipeline-super-Store
│
├── app/
│   ├── src/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   ├── load.py
│   │   ├── database.py
│   │   ├── config.py
│   │   └── etl.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── data/
│   └── raw/
│       └── Sample - Superstore.csv
│
├── sql/
│   └── schema.sql
│
└── docker-compose.yml
```

---

# Running the Project

## Step 1

Open a terminal inside the project folder.

Example:

```bash
cd ETL-pipeline-super-Store
```

---

## Step 2

Build the Docker image and start the containers.

```bash
docker compose up --build
```

This command will:

- Build the ETL Docker image
- Create the PostgreSQL container
- Start the ETL container
- Execute the ETL pipeline
- Load all transformed data into PostgreSQL

---

## Step 3

Wait until the following message appears:

```
========== ETL Pipeline Finished ==========
```

This indicates that the ETL process completed successfully.

---

# Access PostgreSQL

Open another terminal and connect to the PostgreSQL container.

```bash
docker exec -it postgres_container psql -U postgres -d super_store_db
```

---

# Useful PostgreSQL Commands

## List all tables

```sql
\dt
```

---

## View the first 5 rows of a table

```sql
SELECT * FROM "DIM PRODUCT" LIMIT 5;

SELECT * FROM "DIM CUSTOMER" LIMIT 5;

SELECT * FROM "DIM LOCATION" LIMIT 5;

SELECT * FROM "DIM TIME" LIMIT 5;

SELECT * FROM "FACT SALES" LIMIT 5;
```

---

## Count rows

```sql
SELECT COUNT(*) FROM "DIM PRODUCT";

SELECT COUNT(*) FROM "DIM CUSTOMER";

SELECT COUNT(*) FROM "DIM LOCATION";

SELECT COUNT(*) FROM "DIM TIME";

SELECT COUNT(*) FROM "FACT SALES";
```

---

## Describe a table

```sql
\d "DIM PRODUCT"

\d "FACT SALES"
```
## OLAP Queries

```sql
    ROLLUP with GROUPING()
    GROUPING SETS
    LAG() and Lead()
    Running Total
    DENSE_RANK()
    Multi-dimensional Filter
    
```

---

## Exit PostgreSQL

```sql
\q
```

---

# ETL Workflow

```
Extract
    ↓
Read Superstore CSV

    ↓
Transform
- Data cleaning
- Remove duplicates
- Create surrogate keys
- Build dimension tables
- Build fact table

    ↓
Load
Insert all tables into PostgreSQL
```

---

# Technologies Used

- Python
- Pandas
- PostgreSQL
- Docker
- Docker Compose
- psycopg2