import streamlit as st
import pandas as pd

# GOOGLE SHEETS - PUBLISH TO WEB (CSV) URLS
# Replace these with your actual "Publish to Web" CSV links
SHEET_URLS = {
    "stations": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQZERwEGErkv8Mx92cYRIb8GR-nbD4Ccc7RPnnleUgdTSyRYd-46_Pfdi1j06dVUaLodEEXHNQoJPvR/pub?output=csv",
    "fares": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7XlUF_KfI8jbNdsZJZCO0bWYIqjCcLC5FVZvGCCjROSBWQOKggP6hsa07BAcHKCNh4b3kXx4MUmMm/pub?output=csv",
    "interchanges": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQpkY8xYuhu-sqtp1JtZgchmK002nC9CEbeTePPpdg8Dp-bKxOocez1wFwdbtiF-a6wwCNghHztleT5/pub?output=csv"
}

# BACKUP LOCAL FILES
BACKUP_FILES = {
    "stations": "data/stations.csv",
    "fares": "data/fare_matrix.csv",
    "interchanges": "data/interchange_stations.csv"
}

@st.cache_data(ttl=300)
def load_stations():
    """Load metro stations with 5-minute cache and local fallback."""
    try:
        # Attempt to fetch from Google Sheets
        df = pd.read_csv(SHEET_URLS["stations"])
        return df
    except Exception:
        # Fallback to local backup if Sheets fails
        return pd.read_csv(BACKUP_FILES["stations"])

@st.cache_data(ttl=300)
def load_fares():
    """Load fare matrix with 5-minute cache and local fallback."""
    try:
        df = pd.read_csv(SHEET_URLS["fares"])
        return df
    except Exception:
        return pd.read_csv(BACKUP_FILES["fares"])

@st.cache_data(ttl=300)
def load_interchanges():
    """Load interchange stations with 5-minute cache and local fallback."""
    try:
        df = pd.read_csv(SHEET_URLS["interchanges"])
        return df
    except Exception:
        return pd.read_csv(BACKUP_FILES["interchanges"])
