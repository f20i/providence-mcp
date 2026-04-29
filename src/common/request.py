import httpx
from os import getenv
from typing import Any, Literal

PROVIDENCE_SERVICE_ENDPOINT = getenv("PROVIDENCE_SERVICE_ENDPOINT", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT_SECONDS = float(getenv("PROVIDENCE_SERVICE_TIMEOUT_SECONDS", "10"))

print(PROVIDENCE_SERVICE_ENDPOINT)

def request(
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
    path: str,
    *,
    params: dict[str, Any] = None,
    data: dict[str, Any] = None,
    headers: dict[str, Any] = None,
):
    try:
        response = httpx.request(
            method=method,
            url=f"{PROVIDENCE_SERVICE_ENDPOINT}{path}",
            timeout=REQUEST_TIMEOUT_SECONDS,
            params=params,
            data=data,
            headers={
                **(headers or {}),
                "content-type": "application/json",
            },
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code if exc.response is not None else None
        detail = exc.response.text if exc.response is not None else str(exc)
        return {
            "ok": False,
            "status_code": status_code,
            "path": path,
            "error": "api_error",
            "detail": detail,
        }
    except httpx.HTTPError as exc:
        print(str(exc), path)
        return {
            "ok": False,
            "path": path,
            "error": "network_error",
            "detail": str(exc),
        }

    return {"ok": True, "status_code": response.status_code, "path": path, "data": response.json()}