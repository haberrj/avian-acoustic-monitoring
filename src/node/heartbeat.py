import os
import shutil
import subprocess
import time
from datetime import datetime, timezone

import psutil
import requests


def get_cpu_temp_c() -> float | None:
    try:
        out = subprocess.check_output(["vcgencmd", "measure_temp"], text=True)
        return float(out.split("=")[1].split("'")[0])
    except Exception:
        return None


def get_wifi_signal_dbm() -> float | None:
    try:
        out = subprocess.check_output(["iw", "dev", "wlan0", "link"], text=True)
        for line in out.splitlines():
            if "signal:" in line:
                return float(line.split("signal:")[1].split()[0])
    except Exception:
        return None


def main() -> None:
    api_base_url = os.environ["API_BASE_URL"].rstrip("/")
    token = os.environ.get("NODE_API_TOKEN")

    payload = {
        "station_id": os.environ["STATION_ID"],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": time.monotonic(),
        "cpu_temp_c": get_cpu_temp_c(),
        "memory_available_mb": psutil.virtual_memory().available / 1024 / 1024,
        "disk_free_gb": shutil.disk_usage("/").free / 1024 / 1024 / 1024,
        "wifi_signal_dbm": get_wifi_signal_dbm(),
        "node_version": os.environ.get("NODE_VERSION", "unknown"),
    }

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.post(
        f"{api_base_url}/heartbeat/",
        json=payload,
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    print(f"Heartbeat sent: {response.status_code}")


if __name__ == "__main__":
    main()
