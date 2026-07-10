---
name: Performance Report
about: Report performance, resource usage, or scalability issues
title: "[Performance]: "
labels: performance
assignees: ""
---

# Summary

Provide a brief description of the performance issue.

---

# Component

Select the affected component.

- [ ] Server
- [ ] Recording Node
- [ ] Dashboard
- [ ] Database
- [ ] API
- [ ] BirdNET Inference
- [ ] Docker
- [ ] Other

---

# What Is Slow?

Describe the operation experiencing poor performance.

Examples:

- Detection upload
- Heartbeat upload
- Dashboard loading
- BirdNET inference
- Database queries
- Docker startup
- Recording pipeline

---

# Expected Performance

Describe what you expected to happen.

Example:

- Dashboard should load in under 2 seconds.
- BirdNET inference should complete before the next scheduled recording.
- Heartbeat uploads should complete within a few hundred milliseconds.

---

# Actual Performance

Describe what actually happened.

Include measurements if available.

Example:

- Dashboard takes 15 seconds to load.
- BirdNET inference takes 90 seconds.
- API requests frequently time out.

---

# Steps to Reproduce

1.
2.
3.
4.

---

# Hardware

## Device

- [ ] Raspberry Pi 4
- [ ] Raspberry Pi 5
- [ ] VPS
- [ ] Desktop
- [ ] Laptop
- [ ] Other

CPU:

RAM:

Storage:

---

# Software

Operating System:

Docker Version:

Project Version:

Branch:

Commit:

---

# Resource Usage

If known, include any relevant metrics.

| Metric | Value |
|--------|-------|
| CPU Usage | |
| Memory Usage | |
| Disk Usage | |
| Disk Free | |
| Network | |

---

# Logs

Include any relevant logs.

```text

```

---

# Screenshots

If applicable, attach screenshots or graphs.

---

# Additional Context

Include any additional information that may help diagnose the issue.

Examples:

- Number of detections
- Number of stations
- Database size
- Internet connection quality
- Time of day
- Whether the issue is reproducible