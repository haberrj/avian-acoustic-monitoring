# Design Challenges and Lessons Learned

## Project Motivation

The project began as an exploration of passive acoustic monitoring using low-cost hardware and open-source software.

A primary goal was to determine whether a Raspberry Pi could reliably perform automated bird detection without requiring cloud-based processing.

## Privacy and Data Retention

One of the earliest challenges was balancing ecological monitoring with privacy concerns.

Environmental audio recording can unintentionally capture human speech, particularly in urban and suburban environments.

To reduce privacy risks, the system was designed to retain only detection metadata while deleting raw audio recordings after successful processing.

A separate debug mode was introduced to support troubleshooting and validation without making permanent audio retention part of the default workflow.

## Hardware Constraints

The Raspberry Pi provides a low-cost and energy-efficient platform, but introduces several limitations:

* Limited CPU resources
* Limited memory
* Dependence on SD card storage
* Limited power availability for remote deployments

These constraints influenced architectural decisions throughout the project.

## Long-Term Reliability

The intended deployment model assumes unattended operation over extended periods.

This created several challenges:

* Recovery from application crashes
* Automatic updates
* Container management
* Service scheduling
* Monitoring and troubleshooting

The project uses Docker and systemd timers to reduce operational complexity and improve reliability.

## Audio Quality

Bird detection accuracy is heavily influenced by microphone quality and placement.

Environmental factors such as:

* Wind
* Rain
* Road traffic
* Aircraft
* Human activity

can significantly impact classification performance.

The software pipeline can only partially compensate for poor recording conditions.

## False Positives

BirdNET is highly effective but not infallible.

Common sources of false detections include:

* Insects
* Mechanical noise
* Human-made sounds
* Overlapping bird calls

Detection thresholds and post-processing logic are used to reduce false positives while preserving sensitivity.

## Deployment

A key objective was creating a deployment process that could be reproduced on a new Raspberry Pi with minimal manual intervention.

The project therefore includes:

* Docker-based services
* Automated database migrations
* Systemd timers
* Automated update mechanisms
* Infrastructure documentation

This allows the system to be rebuilt or redeployed without requiring extensive manual configuration.

## Future Work

Areas currently under investigation include:

* Solar-powered deployments
* Improved microphone configurations
* Additional quality-control filters
* Geospatial visualization
* Long-term trend analysis
* Multi-device deployments
