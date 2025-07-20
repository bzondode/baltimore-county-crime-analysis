import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils.data_loader import load_data

st.set_page_config("Baltimore Crime Dashboard", layout="wide")
st.title("📊 Baltimore County Crime Dashboard")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Public_Crime_Data.csv")
df = load_data(DATA_PATH)

with st.sidebar:
    st.header("Filters")
    city = st.selectbox("City", sorted(df["CITY"].dropna().unique()))
    offense = st.selectbox("Offense", sorted(df["OFFENSE"].dropna().unique()))

mask = (df["CITY"] == city) & (df["OFFENSE"] == offense)
df_filtered = df[mask]

st.subheader(f"Total Records: {len(df_filtered)}")
st.dataframe(df_filtered.head(100))

col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Monthly Crime Distribution")
    fig_month = px.histogram(df_filtered, x="MONTH", title="Crimes by Month")
    st.plotly_chart(fig_month, use_container_width=True)

with col2:
    st.subheader("🕒 Hourly Crime Distribution")
    fig_hour = px.histogram(df_filtered, x="HOUR", nbins=24, title="Crimes by Hour")
    st.plotly_chart(fig_hour, use_container_width=True)

if "OBF_XCOORD" in df.columns and "OBF_YCOORD" in df.columns:
    st.subheader("📍 Crime Location Map")
    fig = px.scatter_mapbox(
        df_filtered,
        lat="OBF_YCOORD",
        lon="OBF_XCOORD",
        hover_name="OFFENSE",
        hover_data=["OCCURREDON", "ZIP", "BASE_PRECINCT"],
        zoom=9,
        height=500
    )
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)
