from __future__ import annotations

from fastapi.testclient import TestClient
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app


def main() -> None:
    client = TestClient(app)
    routes = [
        "/",
        "/evidence-board",
        "/conflicts",
        "/owners",
        "/docs",
        "/api/dashboard/summary",
        "/api/evidence",
        "/api/conflicts",
        "/api/owners",
        "/api/sample",
    ]
    for route in routes:
        response = client.get(route)
        assert response.status_code == 200, f"{route} returned {response.status_code}"
    print("smoke-ok")


if __name__ == "__main__":
    main()
