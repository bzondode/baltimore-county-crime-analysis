import pandas as pd
import streamlit as st

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["OCCURREDON"], low_memory=False)
    df.columns = df.columns.str.strip().str.upper()
    df = df.dropna(subset=["OBF_YCOORD", "OBF_XCOORD"])
    df["HOUR"] = df["OCCURREDON"].dt.hour
    df["MONTH"] = df["OCCURREDON"].dt.month_name()
    return df
