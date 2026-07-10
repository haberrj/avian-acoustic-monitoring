from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
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
            d.id,
            d.timestamp,
            d.event_time,
            d.latitude,
            d.longitude,
            d.species,
            d.common_name,
            d.call_duration,
            d.confidence,
            s.name AS station_name,
            s.country AS station_country,
            s.region AS station_region,
            s.timezone AS station_timezone
        FROM detections d
        LEFT JOIN stations s ON d.station_id = s.id
        ORDER BY d.event_time DESC
    """
    return pd.read_sql(query, get_engine())

@st.cache_data(ttl=60)
def load_latest_heartbeats() -> pd.DataFrame:
    query = """
        SELECT DISTINCT ON (s.id)
            s.id AS station_db_id,
            s.station_id,
            s.name AS station_name,
            s.country,
            s.region,
            s.timezone,
            s.is_active,
            h.timestamp AS heartbeat_time,
            h.created_at AS received_at,
            h.uptime_seconds,
            h.cpu_temp_c,
            h.memory_available_mb,
            h.disk_free_gb,
            h.wifi_signal_dbm,
            h.node_version
        FROM stations s
        LEFT JOIN node_heartbeats h
            ON h.station_id = s.id
        ORDER BY s.id, h.timestamp DESC NULLS LAST
    """
    return pd.read_sql(query, get_engine())


def convert_utc_to_local(
    timestamp: Any,
    timezone_name: Any,
) -> pd.Timestamp | None:
    if timestamp is None or pd.isna(timestamp):
        return None

    try:
        utc_timestamp = pd.Timestamp(timestamp)
    except (TypeError, ValueError):
        return None

    if pd.isna(utc_timestamp):
        return None

    if utc_timestamp.tzinfo is None:
        utc_timestamp = utc_timestamp.tz_localize("UTC")
    else:
        utc_timestamp = utc_timestamp.tz_convert("UTC")

    if not isinstance(timezone_name, str) or not timezone_name:
        return utc_timestamp

    try:
        station_timezone = ZoneInfo(timezone_name)
        return utc_timestamp.tz_convert(station_timezone)
    except (ZoneInfoNotFoundError, TypeError, ValueError):
        return utc_timestamp


def format_local_timestamp(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""

    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M:%S %Z")

    return str(value)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()

    df["timestamp_utc"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce",
        utc=True,
    )
    df["event_time_utc"] = pd.to_datetime(
        df["event_time"],
        errors="coerce",
        utc=True,
    )

    df["timestamp_local"] = [
        convert_utc_to_local(timestamp, timezone_name)
        for timestamp, timezone_name in zip(
            df["timestamp_utc"],
            df["station_timezone"],
            strict=False,
        )
    ]

    df["event_time_local"] = [
        convert_utc_to_local(timestamp, timezone_name)
        for timestamp, timezone_name in zip(
            df["event_time_utc"],
            df["station_timezone"],
            strict=False,
        )
    ]

    df["local_year_month"] = [
        value.strftime("%Y-%m")
        if isinstance(value, pd.Timestamp)
        else None
        for value in df["event_time_local"]
    ]
    
    df["local_month_label"] = [
        value.strftime("%b %Y")
        if isinstance(value, pd.Timestamp)
        else None
        for value in df["event_time_local"]
    ]

    df["display_name"] = (
        df["common_name"]
        .fillna(df["species"])
        .fillna("Unknown")
    )

    fallback_station = (
        df["latitude"].round(3).astype(str)
        + ", "
        + df["longitude"].round(3).astype(str)
    )

    df["station"] = df["station_name"].fillna(fallback_station)

    return df


def prepare_heartbeats(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()

    df["heartbeat_time"] = pd.to_datetime(
        df["heartbeat_time"],
        errors="coerce",
        utc=True,
    )
    df["received_at"] = pd.to_datetime(
        df["received_at"],
        errors="coerce",
        utc=True,
    )

    now = pd.Timestamp.now(tz="UTC")
    df["heartbeat_age"] = df["heartbeat_time"].rsub(now)
    df["heartbeat_age_minutes"] = (
        df["heartbeat_age"].dt.total_seconds() / 60
    )

    def determine_status(row: pd.Series) -> str:
        if not row["is_active"]:
            return "Disabled"

        if pd.isna(row["heartbeat_time"]):
            return "Never connected"

        age_minutes = row["heartbeat_age_minutes"]

        if age_minutes <= 10:
            return "Online"
        if age_minutes <= 30:
            return "Stale"
        return "Offline"

    df["status"] = df.apply(determine_status, axis=1)

    df["uptime_hours"] = df["uptime_seconds"] / 3600
    df["memory_available_gb"] = df["memory_available_mb"] / 1024
    df["heartbeat_time_local"] = [
        convert_utc_to_local(timestamp, timezone_name)
        for timestamp, timezone_name in zip(
            df["heartbeat_time"],
            df["timezone"],
            strict=False,
        )
    ]
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
    latest = df["event_time_local"].max() if not df.empty else None

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
            country=("station_country", "first"),
            region=("station_region", "first"),
            latitude=("latitude", "mean"),
            longitude=("longitude", "mean"),
            detections=("id", "count"),
            species=("display_name", "nunique"),
            latest_detection=("event_time_local", "max"),
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

    recent = (
        df[
            [
                "event_time_local",
                "display_name",
                "species",
                "confidence",
                "station",
            ]
        ]
        .sort_values("event_time_local", ascending=False)
        .head(25)
        .copy()
    )

    recent["event_time_local"] = recent["event_time_local"].apply(
        format_local_timestamp
    )

    recent = recent.rename(
        columns={
            "event_time_local": "Local Time",
            "display_name": "Common Name",
            "species": "Scientific Name",
            "confidence": "Confidence",
            "station": "Station",
        }
    )

    st.dataframe(
        recent,
        use_container_width=True,
        hide_index=True,
    )


def render_monthly_detections(df: pd.DataFrame) -> None:
    st.subheader("Detections by Month")

    monthly_df = df.dropna(
        subset=["local_year_month", "local_month_label"]
    ).copy()

    if monthly_df.empty:
        st.info("No monthly detection data available.")
        return

    monthly_counts = (
        monthly_df.groupby(
            ["local_year_month", "local_month_label"],
            as_index=False,
        )
        .agg(detections=("id", "count"))
        .sort_values("local_year_month")
    )

    chart_data = monthly_counts.rename(
        columns={
            "local_month_label": "Month",
            "detections": "Detections",
        }
    ).set_index("Month")[["Detections"]]

    st.bar_chart(
        chart_data,
        x_label="Month",
        y_label="Detections",
    )

    st.caption(
        "Monthly totals reflect the available monitoring period and may "
        "represent partial months."
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
            first_detection=("event_time_local", "min"),
            last_detection=("event_time_local", "max"),
        )
        .sort_values("detections", ascending=False)
        .reset_index()
    )
    species_summary["first_detection"] = species_summary[
        "first_detection"
    ].apply(format_local_timestamp)
    species_summary["last_detection"] = species_summary[
        "last_detection"
    ].apply(format_local_timestamp)
    species_summary = species_summary.rename(
        columns={
            "display_name": "Species",
            "detections": "Detections",
            "avg_confidence": "Average Confidence",
            "first_detection": "First Detection",
            "last_detection": "Last Detection",
        }
    )

    st.dataframe(species_summary, use_container_width=True, hide_index=True)

    st.subheader("Top Species")
    st.bar_chart(df["display_name"].value_counts().head(15))

    st.subheader("Activity by Hour")
    hourly = (
        df.assign(hour=df["event_time_local"].apply(
            lambda value: value.hour if pd.notna(value) else None
        ))
        .dropna(subset=["hour"])
        .groupby("hour")
        .size()
    )
    st.bar_chart(hourly)

    st.dataframe(
        species_summary,
        use_container_width=True,
        hide_index=True,
    )

    render_monthly_detections(df)


def render_stations_tab(
    detections_df: pd.DataFrame,
    heartbeat_df: pd.DataFrame,
) -> None:
    st.subheader("Station Health")

    if heartbeat_df.empty:
        st.info("No stations are configured.")
        return

    online_count = (heartbeat_df["status"] == "Online").sum()
    stale_count = (heartbeat_df["status"] == "Stale").sum()
    offline_count = heartbeat_df["status"].isin(
        ["Offline", "Never connected"]
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Stations", len(heartbeat_df))
    col2.metric("Online", int(online_count))
    col3.metric("Stale", int(stale_count))
    col4.metric("Offline", int(offline_count))

    display_df = heartbeat_df.copy()

    display_df["Last Heartbeat"] = display_df[
        "heartbeat_time_local"
    ].apply(
        lambda value: (
            "Never"
            if pd.isna(value)
            else value.strftime("%Y-%m-%d %H:%M:%S %Z")
        )
    )

    display_df["Heartbeat Age"] = display_df[
        "heartbeat_age_minutes"
    ].apply(
        lambda value: (
            "Never"
            if pd.isna(value)
            else f"{value:.1f} min"
        )
    )

    display_df["Uptime"] = display_df["uptime_hours"].apply(
        lambda value: (
            "Unknown"
            if pd.isna(value)
            else f"{value:.1f} h"
        )
    )

    display_df["Memory Available"] = display_df[
        "memory_available_gb"
    ].apply(
        lambda value: (
            "Unknown"
            if pd.isna(value)
            else f"{value:.2f} GB"
        )
    )

    display_df["Disk Free"] = display_df["disk_free_gb"].apply(
        lambda value: (
            "Unknown"
            if pd.isna(value)
            else f"{value:.2f} GB"
        )
    )

    display_df["CPU Temp"] = display_df["cpu_temp_c"].apply(
        lambda value: (
            "Unknown"
            if pd.isna(value)
            else f"{value:.1f} °C"
        )
    )

    display_df["Wi-Fi Signal"] = display_df["wifi_signal_dbm"].apply(
        lambda value: (
            "Unknown"
            if pd.isna(value)
            else f"{value:.0f} dBm"
        )
    )

    status_icons = {
        "Online": "🟢 Online",
        "Stale": "🟡 Stale",
        "Offline": "🔴 Offline",
        "Never connected": "⚪ Never connected",
        "Disabled": "⚫ Disabled",
    }

    display_df["status"] = display_df["status"].map(
        status_icons
    ).fillna(display_df["status"])

    display_df = display_df.rename(
        columns={
            "status": "Status",
            "station_name": "Station",
            "station_id": "Station ID",
            "country": "Country",
            "region": "Region",
            "node_version": "Version",
        }
    )

    st.dataframe(
        display_df[
            [
                "Status",
                "Station",
                "Station ID",
                "Country",
                "Region",
                "Last Heartbeat",
                "Heartbeat Age",
                "Uptime",
                "Memory Available",
                "Disk Free",
                "CPU Temp",
                "Wi-Fi Signal",
                "Version",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Detection Summary")

    if detections_df.empty:
        st.info("No detections available for the selected filters.")
        return

    station_summary = build_station_summary(detections_df)

    if station_summary.empty:
        st.info("No station coordinates available.")
        return

    station_summary["latest_detection"] = station_summary[
        "latest_detection"
    ].apply(format_local_timestamp)

    station_summary = station_summary.rename(
        columns={
            "station": "Station",
            "country": "Country",
            "region": "Region",
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


def render_system_tab(
    detections_df: pd.DataFrame,
    heartbeat_df: pd.DataFrame,
) -> None:
    st.subheader("System Status")

    if heartbeat_df.empty:
        st.warning("No station heartbeat data available.")
    else:
        for _, station in heartbeat_df.iterrows():
            name = station["station_name"]
            status = station["status"]

            if status == "Online":
                st.success(
                    f"{name}: Online — last heartbeat "
                    f"{station['heartbeat_age_minutes']:.1f} minutes ago"
                )
            elif status == "Stale":
                st.warning(
                    f"{name}: Heartbeat stale — last received "
                    f"{station['heartbeat_age_minutes']:.1f} minutes ago"
                )
            elif status == "Disabled":
                st.info(f"{name}: Disabled")
            elif status == "Never connected":
                st.error(f"{name}: No heartbeat has ever been received")
            else:
                st.error(
                    f"{name}: Offline — last heartbeat "
                    f"{station['heartbeat_age_minutes']:.1f} minutes ago"
                )

    st.subheader("Detection Pipeline")

    if detections_df.empty:
        st.warning("No detections found.")
        return

    latest_detection = detections_df["event_time"].max()
    age = pd.Timestamp.now(tz=latest_detection.tz) - latest_detection

    st.write("Latest detection:", latest_detection)
    st.write("Total database rows loaded:", len(detections_df))

    if age > pd.Timedelta(hours=24):
        st.info(
            "No recent detections. This does not necessarily indicate a node "
            "failure if heartbeats are still arriving."
        )

    with st.expander("Raw detection data"):
        st.dataframe(detections_df, use_container_width=True)


def main() -> None:
    st.title("Avian Acoustic Monitoring")

    df = prepare_data(load_detections())
    heartbeat_df = prepare_heartbeats(load_latest_heartbeats())
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
        render_stations_tab(filtered_df, heartbeat_df)

    with system_tab:
        render_system_tab(df, heartbeat_df)


if __name__ == "__main__":
    main()
