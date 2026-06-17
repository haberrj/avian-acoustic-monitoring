import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pydeck as pdk
import seaborn as sns

# ============================
# CONFIG
# ============================

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
    f"{os.getenv('POSTGRES_PORT', '5432')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)

# ============================
# LOAD DATA
# ============================

@st.cache_data
def load_data():
    query = "SELECT * FROM detections"
    return pd.read_sql(query, engine)

df = load_data()

# ============================
# UI HEADER
# ============================

st.title("🐦 Acoustic Bird Monitoring Dashboard")

# Debug view
with st.expander("🔍 Show raw data"):
    st.dataframe(df)

if df.empty:
    st.warning("No detections yet.")
    st.stop()

# ============================
# DATA PREP
# ============================

df["event_time"] = pd.to_datetime(df["event_time"])
df = df.sort_values("event_time")

# ============================
# FILTERS
# ============================

st.sidebar.header("Filters")

# Confidence filter
threshold = st.sidebar.slider(
    "Confidence threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.05
)

df = df[df["confidence"] >= threshold]

# Species filter
species_list = sorted(df["species"].dropna().unique())
selected_species = st.sidebar.selectbox(
    "Select species",
    ["All"] + species_list
)

if selected_species != "All":
    df = df[df["species"] == selected_species]

# ============================
# SUMMARY METRICS
# ============================

st.subheader("📊 Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total detections", len(df))
col2.metric("Unique species", df["species"].nunique())
col3.metric("Avg confidence", round(df["confidence"].mean(), 2))

# ============================
# TIME SERIES
# ============================

st.subheader("📈 Detections over time")

time_series = df.set_index("event_time").resample("10min").size()

st.line_chart(time_series)

# ============================
# ACTIVITY BY HOUR
# ============================

st.subheader("⏰ Activity by hour")

df["hour"] = df["event_time"].dt.hour
hour_counts = df.groupby("hour").size()

st.bar_chart(hour_counts)

# ============================
# SPECIES DISTRIBUTION
# ============================

st.subheader("🦜 Top species")

species_counts = df["common_name"].value_counts().head(10)

st.bar_chart(species_counts)

# ============================
# CONFIDENCE HISTOGRAM
# ============================

st.subheader("🎯 Confidence distribution")

fig, ax = plt.subplots()
ax.hist(df["confidence"], bins=10)
ax.set_xlabel("Confidence")
ax.set_ylabel("Frequency")

st.pyplot(fig)

# ============================
# DAILY ACTIVITY
# ============================

st.subheader("📅 Daily detections")

df["date"] = df["event_time"].dt.date
daily_counts = df.groupby("date").size()

st.line_chart(daily_counts)

# ============================
# ACTIVITY TABLE
# ============================

st.subheader("📋 Species activity table")

activity_table = (
    df.groupby("common_name")
    .size()
    .sort_values(ascending=False)
    .rename("detections")
)

st.dataframe(activity_table)

st.subheader("🗺️ Detection intensity")

layer = pdk.Layer(
    "HeatmapLayer",
    data=df,
    get_position='[longitude, latitude]',
    get_weight="confidence",
    radiusPixels=50,
)

view_state = pdk.ViewState(
    latitude=df["latitude"].mean(),
    longitude=df["longitude"].mean(),
    zoom=14,
)

deck = pdk.Deck(layers=[layer], initial_view_state=view_state)

st.pydeck_chart(deck)

# ============================
# TIME HEATMAP
# ============================

st.subheader("🔥 Activity heatmap (time of day vs date)")

# Ensure datetime
df["event_time"] = pd.to_datetime(df["event_time"])

# Create time features
df["date"] = df["event_time"].dt.date
df["hour"] = df["event_time"].dt.hour

# Pivot table
heatmap_data = df.groupby(["date", "hour"]).size().unstack(fill_value=0)
heatmap_data = heatmap_data.sort_index()

# Plot with seaborn
fig, ax = plt.subplots(figsize=(12, 6))

sns.heatmap(
    heatmap_data,
    cmap="viridis",        # color scheme
    linewidths=0.5,        # grid lines
    linecolor="gray",
    cbar_kws={"label": "Number of detections"},  # color bar label
    ax=ax
)

# Labels
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Date")

st.pyplot(fig)
