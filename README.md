# 🛍️ E-Commerce Sales Analytics with AWS Glue + Athena + Machine Learning

Analyze customer purchasing behavior and trends using AWS Glue, Athena, and Python-based machine learning.

---

## ✅ Phase 1: Data Engineering

You're building a **serverless data pipeline**:

- 📁 Raw `.csv` data stored in **Amazon S3**
- 🛠️ Crawled and cataloged with **AWS Glue**
- 🔍 Queried using **Amazon Athena**

This demonstrates:

- Serverless ETL using AWS Glue
- Schema detection and metadata cataloging
- SQL-based analytics using Athena

**Skills Demonstrated**: Glue, S3, Athena, IAM, SQL

---

## ✅ Phase 2: Data Science – Analysis + Machine Learning

Once the data is accessible via Athena, you can load it into a Pandas DataFrame for ML analysis:

### 🔹 1. Behavioral Trend Analysis

Use `pandas`, `matplotlib`, `seaborn`, `statsmodels`:

- Daily/weekly purchase trends
- Top-spending cities or customers
- RFM segmentation (Recency, Frequency, Monetary)

```python
# Top 10 cities by spending
df.groupby('city')['purchase_amount'].sum().sort_values(ascending=False).head(10)
```
# ecommerce-trends
