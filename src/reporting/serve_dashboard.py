import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from src.utils.config import settings

st.set_page_config(page_title="PulsePipe KPI Dashboard", layout="wide")

engine = create_engine(settings.database.uri, echo=False)

st.title("📊 PulsePipe — Real-time KPI & ML Monitoring")

col1, col2, col3, col4 = st.columns(4)
with engine.begin() as conn:
    df = pd.read_sql("SELECT * FROM daily_funnel", conn)

views = int(df["views"].sum())
adds = int(df["adds"].sum())
purchases = int(df["purchases"].sum())
conv_rate = purchases / max(views, 1)
lat_avg = float(df["avg_latency_ms"].mean())

col1.metric("Views", f"{views:,}")
col2.metric("Adds to Cart", f"{adds:,}")
col3.metric("Purchases", f"{purchases:,}")
col4.metric("Conversion Rate", f"{conv_rate:.2%}")

st.subheader("Daily Funnel")
st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)

st.subheader("Latency Over Time (avg)")
st.line_chart(df.sort_values("date")[["avg_latency_ms"]].set_index(df["date"]))
