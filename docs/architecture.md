# Architecture

## Overview

The Avian Acoustic Monitoring project is a passive acoustic monitoring system designed to identify bird vocalizations using BirdNET and store detections in a PostgreSQL database for later analysis and visualization.

The system consists of four primary components:

1. Audio capture
2. Acoustic classification
3. Data storage
4. Visualization

## Processing Flow

```text
Audio Recorder
    ↓
WAV Recording
    ↓
BirdNET Analysis
    ↓
Detection Filtering
    ↓
PostgreSQL Storage
    ↓
Streamlit Dashboard
```

A recording is captured using the local microphone attached to the Raspberry Pi. The recording is analyzed using BirdNET and detections above the configured confidence threshold are retained.

Detection metadata is enriched with:

* Species information
* Confidence score
* Detection timestamp
* Geographic coordinates
* Call duration

Detections are persisted to PostgreSQL and made available through the Streamlit dashboard.

Depending on deployment configuration, audio recordings may be deleted immediately after processing or retained for debugging purposes.

## Components

### Recorder

Responsible for capturing audio from the configured recording device and writing recordings to disk.

### BirdNET

Responsible for species classification and post-processing of detections.

### Storage

Provides database connectivity, schema management, and persistence of detections.

### Dashboard

Provides a web-based interface for viewing detections and monitoring system activity.

## Deployment Model

The system is designed to run on a Raspberry Pi using Docker Compose.

Long-running services:

* PostgreSQL
* Streamlit Dashboard
* Cloudflare Tunnel

Scheduled services:

* Audio Recording Pipeline
* System Update Tasks
