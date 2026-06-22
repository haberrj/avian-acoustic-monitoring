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
    selected_station: str


load_dotenv()

st.set_page_config(
    page_title="Avian Acoustic Monitoring",
    layout="wide",
)

st_autorefresh(interval=60_000, key="dashboard_refresh")


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

    df["station"] = (
        df["latitude"].round(3).astype(str)
        + ", "
        + df["longitude"].round(3).astype(str)
    )

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
    station_options = ["All"]

    if not df.empty:
        species_options += sorted(df["display_name"].dropna().unique())
        station_options += sorted(df["station"].dropna().unique())

    selected_species = st.sidebar.selectbox("Species", species_options)
    selected_station = st.sidebar.selectbox("Station", station_options)

    return DashboardFilters(
        confidence_threshold=confidence_threshold,
        selected_species=selected_species,
        selected_station=selected_station,
    )


def apply_filters(df: pd.DataFrame, filters: DashboardFilters) -> pd.DataFrame:
    if df.empty:
        return df

    filtered = df[df["confidence"] >= filters.confidence_threshold].copy()

    if filters.selected_species != "All":
        filtered = filtered[filtered["display_name"] == filters.selected_species]

    if filters.selected_station != "All":
        filtered = filtered[filtered["station"] == filters.selected_station]

    return filtered


def render_kpis(df: pd.DataFrame) -> None:
    detections = len(df)
    species = df["display_name"].nunique() if not df.empty else 0
    stations = df["station"].nunique() if not df.empty else 0
    latest = df["event_time"].max() if not df.empty else None

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Detections", detections)
    col2.metric("Species", species)
    col3.metric("Stations", stations)

    if latest is not None and pd.notna(latest):
        col4.metric("Latest detection", latest.strftime("%Y-%m-%d %H:%M"))
    else:
        col4.metric("Latest detection", "None")


def calculate_zoom(df: pd.DataFrame) -> int:
    if len(df) <= 1:
        return 10

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


def build_station_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.dropna(subset=["latitude", "longitude"])
        .groupby("station")
        .agg(
            latitude=("latitude", "mean"),
            longitude=("longitude", "mean"),
            detections=("id", "count"),
            species=("display_name", "nunique"),
            latest_detection=("event_time", "max"),
        )
        .reset_index()
    )


def render_map(df: pd.DataFrame) -> None:
    map_df = df.dropna(subset=["latitude", "longitude"]).copy()

    if map_df.empty:
        st.info("No GPS coordinates available for the current selection.")
        return

    map_df["latitude"] = map_df["latitude"].astype(float)
    map_df["longitude"] = map_df["longitude"].astype(float)
    map_df["confidence"] = map_df["confidence"].astype(float)
    map_df["event_time"] = map_df["event_time"].astype(str)

    station_df = build_station_summary(map_df)

    center_lat = map_df["latitude"].mean()
    center_lon = map_df["longitude"].mean()

    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=station_df,
        get_position="[longitude, latitude]",
        get_weight="detections",
        radiusPixels=80,
    )

    station_layer = pdk.Layer(
        "ScatterplotLayer",
        data=station_df,
        get_position="[longitude, latitude]",
        radius_units="pixels",
        get_radius=12,
        get_fill_color=[255, 255, 255, 0],
        get_line_color=[255, 255, 255, 0],
        pickable=True,
    )

    deck = pdk.Deck(
        layers=[heatmap_layer, station_layer],
        initial_view_state=pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=calculate_zoom(map_df),
            pitch=0,
        ),
        tooltip={
            "html": (
                "<b>Station {station}</b><br/>"
                "Detections: {detections}<br/>"
                "Species: {species}<br/>"
                "Latest: {latest_detection}"
            )
        }, # type: ignore[arg-type]
    )

    st.pydeck_chart(deck, use_container_width=True)


def render_overview_tab(df: pd.DataFrame) -> None:
    render_kpis(df)

    st.subheader("Detection Map")
    render_map(df)

    st.subheader("Recent Detections")

    if df.empty:
        st.info("No detections match the current filters.")
        return

    st.dataframe(
        df[
            [
                "event_time",
                "display_name",
                "species",
                "confidence",
                "call_duration",
                "station",
            ]
        ].sort_values("event_time", ascending=False).head(25),
        use_container_width=True,
        hide_index=True,
    )


def render_species_tab(df: pd.DataFrame) -> None:
    st.subheader("Species Summary")

    if df.empty:
        st.info("No species data available.")
        return

    species_summary = (
        df.groupby("display_name")
        .agg(
            detections=("id", "count"),
            avg_confidence=("confidence", "mean"),
            first_detection=("event_time", "min"),
            last_detection=("event_time", "max"),
        )
        .sort_values("detections", ascending=False)
        .reset_index()
    )

    st.dataframe(species_summary, use_container_width=True, hide_index=True)

    st.subheader("Top species")
    st.bar_chart(df["display_name"].value_counts().head(15))

    st.subheader("Activity by hour")
    hourly = df.assign(hour=df["event_time"].dt.hour).groupby("hour").size()
    st.bar_chart(hourly)


def render_stations_tab(df: pd.DataFrame) -> None:
    st.subheader("Station Summary")

    if df.empty:
        st.info("No station data available.")
        return

    station_summary = build_station_summary(df)

    if station_summary.empty:
        st.info("No station coordinates available.")
        return

    station_summary = station_summary.sort_values(
        "latest_detection",
        ascending=False,
    )

    station_summary = station_summary.rename(
        columns={
            "station": "Station",
            "detections": "Detections",
            "species": "Species",
            "latest_detection": "Latest Detection",
            "latitude": "Latitude",
            "longitude": "Longitude",
        }
    )

    st.dataframe(
        station_summary,
        use_container_width=True,
        hide_index=True,
    )


def render_system_tab(df: pd.DataFrame) -> None:
    st.subheader("System status")

    if df.empty:
        st.warning("No detections found.")
        return

    latest_detection = df["event_time"].max()
    age = pd.Timestamp.now(tz=latest_detection.tz) - latest_detection

    if age > pd.Timedelta(hours=6):
        st.warning(f"No detections in {age}. Check recorder, microphone, or schedule.")
    else:
        st.success("Recent detections available.")

    st.write("Latest detection:", latest_detection)
    st.write("Total database rows loaded:", len(df))

    with st.expander("Raw data"):
        st.dataframe(df, use_container_width=True)


def main() -> None:
    st.title("Avian Acoustic Monitoring")

    df = prepare_data(load_detections())
    filters = render_sidebar(df)
    filtered_df = apply_filters(df, filters)

    overview_tab, species_tab, stations_tab, system_tab = st.tabs(
        ["Overview", "Species", "Stations", "System"]
    )

    with overview_tab:
        render_overview_tab(filtered_df)

    with species_tab:
        render_species_tab(filtered_df)

    with stations_tab:
        render_stations_tab(filtered_df)

    with system_tab:
        render_system_tab(df)


if __name__ == "__main__":
    main()
