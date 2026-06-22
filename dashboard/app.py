from __future__ import annotations

import os
from dataclasses import dataclass

import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from streamlit_autorefresh import st_autorefresh


@dataclass(frozen=True)
class DashboardFilters:
    confidence_threshold: float
    selected_species: str
    date_range: tuple[pd.Timestamp, pd.Timestamp] | None


load_dotenv()

st.set_page_config(
    page_title="Avian Acoustic Monitoring",
    page_icon=None,
    layout="wide",
)

st_autorefresh(interval=60_000, key="datarefresh")


@st.cache_resource
def get_engine() -> Engine:
    database_url = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
        f"{os.getenv('POSTGRES_PORT', '5432')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )
    return create_engine(database_url)


@st.cache_data(ttl=60)
def load_detections() -> pd.DataFrame:
    query = """
        SELECT
            id,
            timestamp,
            event_time,
            latitude,
            longitude,
            species,
            common_name,
            call_duration,
            confidence
        FROM detections
        ORDER BY event_time DESC
    """
    return pd.read_sql(query, get_engine())


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")
    df["display_name"] = df["common_name"].fillna(df["species"]).fillna("Unknown")
    return df


def render_sidebar(df: pd.DataFrame) -> DashboardFilters:
    st.sidebar.header("Filters")

    confidence_threshold = st.sidebar.slider(
        "Minimum confidence",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.05,
    )

    species_options = ["All"]
    if not df.empty:
        species_options += sorted(df["display_name"].dropna().unique().tolist())

    selected_species = st.sidebar.selectbox("Species", species_options)

    date_range = None
    if not df.empty and df["event_time"].notna().any():
        min_date = df["event_time"].min().date()
        max_date = df["event_time"].max().date()

        selected_range = st.sidebar.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        if isinstance(selected_range, tuple) and len(selected_range) == 2:
            date_range = (
                pd.Timestamp(selected_range[0]),
                pd.Timestamp(selected_range[1]) + pd.Timedelta(days=1),
            )

    return DashboardFilters(
        confidence_threshold=confidence_threshold,
        selected_species=selected_species,
        date_range=date_range,
    )


def apply_filters(df: pd.DataFrame, filters: DashboardFilters) -> pd.DataFrame:
    if df.empty:
        return df

    filtered = df[df["confidence"] >= filters.confidence_threshold].copy()

    if filters.selected_species != "All":
        filtered = filtered[filtered["display_name"] == filters.selected_species]

    if filters.date_range is not None:
        start_date, end_date = filters.date_range
        filtered = filtered[
            (filtered["event_time"] >= start_date)
            & (filtered["event_time"] < end_date)
        ]

    return filtered


def render_header(df: pd.DataFrame) -> None:
    st.title("Avian Acoustic Monitoring")

    if df.empty or df["event_time"].isna().all():
        st.caption("No detections available.")
        return

    latest_detection = df["event_time"].max()
    st.caption(f"Last detection: {latest_detection:%Y-%m-%d %H:%M:%S}")


def render_kpis(df: pd.DataFrame) -> None:
    total_detections = len(df)
    unique_species = df["display_name"].nunique() if not df.empty else 0
    locations = (
        df[["latitude", "longitude"]]
        .dropna()
        .drop_duplicates()
        .shape[0]
        if not df.empty
        else 0
    )
    avg_confidence = df["confidence"].mean() if not df.empty else 0.0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Detections", total_detections)
    col2.metric("Species", unique_species)
    col3.metric("Locations", locations)
    col4.metric("Avg confidence", f"{avg_confidence:.2f}")


def calculate_zoom(df: pd.DataFrame) -> int:
    lat_range = df["latitude"].max() - df["latitude"].min()
    lon_range = df["longitude"].max() - df["longitude"].min()
    max_range = max(lat_range, lon_range)

    if max_range > 80:
        return 1
    if max_range > 40:
        return 2
    if max_range > 15:
        return 3
    if max_range > 5:
        return 5
    if max_range > 1:
        return 7
    return 10


def render_map(df: pd.DataFrame) -> None:
    st.subheader("Detection Map")

    map_df = df.dropna(subset=["latitude", "longitude"])

    if map_df.empty:
        st.info("No GPS coordinates available for the current selection.")
        return

    center_lat = map_df["latitude"].mean()
    center_lon = map_df["longitude"].mean()
    zoom = calculate_zoom(map_df)

    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=map_df,
        get_position="[longitude, latitude]",
        get_weight="confidence",
        radiusPixels=35,
    )

    point_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position="[longitude, latitude]",
        get_radius=200,
        get_fill_color="[30, 120, 180, 120]",
        pickable=True,
    )

    tooltip = {
        "html": (
            "<b>{display_name}</b><br/>"
            "Confidence: {confidence}<br/>"
            "Time: {event_time}"
        )
    }

    deck = pdk.Deck(
        layers=[heatmap_layer, point_layer],
        initial_view_state=pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=zoom,
        ),
        tooltip=tooltip,
    )

    st.pydeck_chart(deck, use_container_width=True)


def render_charts(df: pd.DataFrame) -> None:
    left, right = st.columns(2)

    with left:
        st.subheader("Detections Over Time")
        if df.empty or df["event_time"].isna().all():
            st.info("No time-series data available.")
        else:
            time_series = (
                df.set_index("event_time")
                .sort_index()
                .resample("1h")
                .size()
            )
            st.line_chart(time_series)

    with right:
        st.subheader("Top Species")
        species_counts = df["display_name"].value_counts().head(10)
        if species_counts.empty:
            st.info("No species data available.")
        else:
            st.bar_chart(species_counts)

    left, right = st.columns(2)

    with left:
        st.subheader("Activity by Hour")
        if df.empty or df["event_time"].isna().all():
            st.info("No hourly data available.")
        else:
            hourly_counts = df.assign(hour=df["event_time"].dt.hour).groupby("hour").size()
            st.bar_chart(hourly_counts)

    with right:
        st.subheader("Confidence Distribution")
        if df.empty:
            st.info("No confidence data available.")
        else:
            fig, ax = plt.subplots()
            ax.hist(df["confidence"].dropna(), bins=10)
            ax.set_xlabel("Confidence")
            ax.set_ylabel("Detections")
            st.pyplot(fig)


def render_detection_table(df: pd.DataFrame) -> None:
    st.subheader("Recent Detections")

    if df.empty:
        st.info("No detections match the selected filters.")
        return

    columns = [
        "event_time",
        "display_name",
        "species",
        "confidence",
        "call_duration",
        "latitude",
        "longitude",
    ]

    st.dataframe(
        df[columns].sort_values("event_time", ascending=False),
        use_container_width=True,
        hide_index=True,
    )


def main() -> None:
    df = prepare_data(load_detections())

    render_header(df)

    with st.expander("Raw data"):
        st.dataframe(df, use_container_width=True)

    filters = render_sidebar(df)
    filtered_df = apply_filters(df, filters)

    if filtered_df.empty:
        st.warning("No detections match the selected filters.")

    render_kpis(filtered_df)
    render_map(filtered_df)
    render_charts(filtered_df)
    render_detection_table(filtered_df)


if __name__ == "__main__":
    main()