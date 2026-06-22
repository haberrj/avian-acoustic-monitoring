# Privacy Considerations

## Overview

This project was developed for passive acoustic monitoring of bird species using automated classification techniques. While the primary objective is the detection of bird vocalizations, environmental audio recordings may unintentionally capture human speech or other personally identifiable information.

As a result, privacy considerations were incorporated into the system design from the beginning.

## Data Minimization

The system follows a data minimization approach wherever practical.

Only the information required for bird detection and ecological analysis is retained. This includes:

* Species name
* Scientific name
* Detection confidence
* Detection timestamp
* Geographic coordinates
* Call duration

Raw audio recordings are not required for long-term operation of the system.

## Recording Retention

The default processing workflow is:

1. Record audio
2. Analyze audio using BirdNET
3. Store detection metadata
4. Delete the original recording

This approach reduces the amount of potentially sensitive audio retained by the system.

For development and troubleshooting purposes, recordings may optionally be retained in a dedicated debug mode. This mode should only be enabled when necessary.

## Human Speech

The system is not intended to record, transcribe, classify, or analyze human conversations.

Any incidental capture of human speech is considered a by-product of environmental audio recording rather than a project objective.

Where possible, deployments should avoid locations where regular human conversations are expected.

## Public Access

The public dashboard only exposes processed detection data.

Audio recordings are not published through the dashboard.

Database access is restricted to authorized system components.

## Disclaimer

Users are responsible for ensuring compliance with local laws, regulations, and privacy requirements applicable to their deployment location.

This document describes technical design considerations and should not be interpreted as legal advice.
