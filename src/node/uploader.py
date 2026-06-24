import requests


def upload_detection(api_url: str, api_token: str, payload: dict) -> None:
    response = requests.post(
        f"{api_url.rstrip('/')}/detections/",
        json=payload,
        headers={"Authorization": f"Bearer {api_token}"},
        timeout=10,
    )
    response.raise_for_status()
