# 🚖 Uber-like Data Pipeline Project

## 📌 Overview

This project simulates an **end-to-end data pipeline** for an Uber-like ride-hailing system.
The pipeline focuses on **ingestion, geospatial processing, and Hive-based analytics**, turning raw ride data into structured, queryable insights.

---

## ⚙️ Architecture

1. **Data Ingestion**

   * Raw rides and bookings data ingested from RDBMS/CSV (Uber NYC dataset).
   * Loaded into **HDFS** using Sqoop or direct ingestion.

2. **Data Processing**

   * **PySpark** used for transformations:

     * Convert latitude/longitude into **Geo-hash keys** (via H3 library).
     * Calculate **trip duration**.
 
3. **Data Storage & Analytics**

   * Data stored in **Hive tables** for structured queries.
   * Example: `Staging_Rides_Geo`, `Dim_Driver`.

---

## 📊 Core Data Sources

| Table         | Source    | Key Columns    | Example Attributes                                                     |
| ------------- | --------- | -------------- | ---------------------------------------------------------------------- |
| **Raw_Rides** | CSV/RDBMS | `trip_id (PK)` | start_lat, start_lon, end_lat, end_lon, start_time, end_time, distance |

---

## 📂 Detailed Output Tables

### **Staging_Rides_Geo**

| Column           | Description                               | Role                     |
| ---------------- | ----------------------------------------- | ------------------------ |
| `trip_id`        | Business Key                              | Join Key                 |
| `start_time`     | Core Fact Metric (Time Dimension FK)      | Fact Metric              |
| `start_geo_hash` | Derived from start_lat/lon via PySpark H3 | Geospatial Dimension Key |
| `end_geo_hash`   | Derived from end_lat/lon via PySpark H3   | Geospatial Dimension Key |
| `trip_duration`  | end_time − start_time                     | Performance Metric       |

---

## 📦 Deliverables

1. **Sqoop Script**

   * Import drivers/rides data into HDFS.

2. **PySpark Script**

   * Geohash transformation + KPI calculations.

3. **Hive DDL**

   * Table creation (`Staging_Rides_Geo`, `Dim_Driver`, etc.).

4. **Spark SQL Queries**

   * Calculate Driver Utilization %, Acceptance Rate, Ratings over rolling windows.

---

## 🛠️ Tech Stack

* **HDFS** – Storage layer.
* **Sqoop** – Data ingestion from Postgres.
* **PySpark** – ETL & rolling KPIs.
* **Hive** – Data warehouse for analytics.
* **H3 / Geospatial Library** – Geo-hash generation.



## 📈 Results & Insights

* Raw ride data successfully transformed into **geo-hash indexed Hive tables**.
* Enabled **efficient spatial queries** for driver/ride allocation and demand forecasting.
* Demonstrated **end-to-end ETL** using Hadoop ecosystem tools.



