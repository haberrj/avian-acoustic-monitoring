# Hardware

## Current Development Hardware

### Compute

* Raspberry Pi 4
* 32 GB microSD card
* Raspberry Pi OS Lite (64-bit)

The software is designed to run entirely on-device without requiring cloud-based inference.

## Audio Capture

The system uses an external microphone connected to the Raspberry Pi.

Microphone quality has a significant impact on detection accuracy and is currently one of the most important factors affecting overall performance.

Future testing will compare:

* USB microphones
* Lavalier microphones
* Purpose-built environmental microphones
* Directional microphone configurations

## Networking

The Raspberry Pi is connected via Wi-Fi.

Remote dashboard access is provided through Cloudflare Tunnel, eliminating the need for port forwarding or public exposure of the local network.

## Storage

The system stores:

* Detection metadata
* Database records
* Application logs

Audio recordings are temporary and are removed after processing unless debug mode is enabled.

## Power

Current development deployments assume a permanent power source.

Future work may investigate:

* Battery-backed operation
* Solar-powered deployments
* Low-power operating modes

## Environmental Considerations

Outdoor acoustic monitoring introduces several challenges:

* Rain
* Wind
* Condensation
* Temperature fluctuations
* Insects
* Wildlife interference

Any long-term deployment should consider weatherproofing, microphone protection, and adequate ventilation.

## Future Hardware Improvements

Potential future upgrades include:

* Dedicated environmental microphone enclosure
* Solar charging system
* Larger storage capacity
* GPS integration
* Multiple synchronized recording devices
* LoRa or cellular connectivity for remote deployments
