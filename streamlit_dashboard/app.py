import os
import boto3
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# Load AWS credentials and config
load_dotenv()

ATHENA_DATABASE = os.getenv("ATHENA_DATABASE")
ATHENA_TABLE = os.getenv("ATHENA_TABLE")
S3_OUTPUT = os.getenv("S3_OUTPUT")

client = boto3.client("athena", region_name=os.getenv("AWS_REGION"))

st.set_page_config(page_title="E-Commerce Trends", layout="wide")
st.title("📊 E-Commerce Trends Dashboard")

@st.cache_data
def run_athena_query(query):
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": ATHENA_DATABASE},
        ResultConfiguration={"OutputLocation": S3_OUTPUT}
    )
    query_id = response["QueryExecutionId"]
    while True:
        status = client.get_query_execution(QueryExecutionId=query_id)
        state = status["QueryExecution"]["Status"]["State"]
        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
    if state != "SUCCEEDED":
        st.error(f"Query failed: {state}")
        return pd.DataFrame()

    result = client.get_query_results(QueryExecutionId=query_id)
    columns = [col["VarCharValue"] for col in result["ResultSet"]["Rows"][0]["Data"]]
    rows = [
        [col.get("VarCharValue", "") for col in row["Data"]]
        for row in result["ResultSet"]["Rows"][1:]
    ]
    return pd.DataFrame(rows, columns=columns)

# Query the Athena table
df = run_athena_query(f"SELECT * FROM {ATHENA_TABLE} LIMIT 1000")

if not df.empty:
    df["purchase_amount"] = pd.to_numeric(df["purchase_amount"], errors="coerce")
    df["purchase_date"] = pd.to_datetime(df["purchase_date"], errors="coerce")

    # --- Top Customers by Spend ---
    st.subheader("💰 Top 10 Customers by Total Spend (with Location)")

    top_df = (
        df.groupby(["id", "location"])["purchase_amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_df["label"] = top_df["id"].astype(str) + " (" + top_df["location"].astype(str) + ")"

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=top_df,
        y="label",
        x="purchase_amount",
        palette="magma",
        ax=ax
    )
    ax.set_title("Top 10 Customers by Spend", fontsize=14)
    ax.set_xlabel("Total Spend ($)")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    for i, value in enumerate(top_df["purchase_amount"]):
        ax.text(value + 100, i, f"${value:,.0f}", va="center", fontsize=10)

    st.pyplot(fig)

    # --- Daily Purchase Trend ---
    st.subheader("📈 Daily Purchase Trend")
    daily = df.groupby(df["purchase_date"].dt.date)["purchase_amount"].sum()
    st.line_chart(daily)

    # --- Export Option ---
    st.download_button(
        label="📥 Download Data as CSV",
        data=df.to_csv(index=False),
        file_name="customer_data.csv",
        mime="text/csv"
    )
else:
    st.warning("No data returned from Athena.")
