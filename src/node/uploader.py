import os
from typing import Any

import requests


def upload_detection_payload(payload: dict[str, Any]) -> None:
    """Upload a node detection payload to the server API."""
    api_url = os.getenv("API_URL")
    api_token = os.getenv("API_TOKEN")

    if not api_url:
        raise RuntimeError("API_URL is not set")

    if not api_token:
        raise RuntimeError("API_TOKEN is not set")

    response = requests.post(
        f"{api_url.rstrip('/')}/detections/",
        json=payload,
        headers={"Authorization": f"Bearer {api_token}"},
        timeout=30,
    )
    response.raise_for_status()