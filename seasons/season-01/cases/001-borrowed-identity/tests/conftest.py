import os
import time

import httpx
import pytest

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8001")

# Keys match fixtures/tenants.json — tests play the role of each tenant.
ACME_KEY = "lw_live_acme_6f2d"
GLOBEX_KEY = "lw_live_globex_9c41"


@pytest.fixture(scope="session", autouse=True)
def wait_for_app():
    deadline = time.time() + 40
    while time.time() < deadline:
        try:
            if httpx.get(f"{BASE_URL}/healthz", timeout=2).status_code == 200:
                return
        except httpx.HTTPError:
            pass
        time.sleep(1)
    raise RuntimeError(f"App at {BASE_URL} did not become healthy in 40s")


@pytest.fixture
def acme():
    with httpx.Client(base_url=BASE_URL, headers={"X-API-Key": ACME_KEY}, timeout=10) as c:
        yield c


@pytest.fixture
def globex():
    with httpx.Client(base_url=BASE_URL, headers={"X-API-Key": GLOBEX_KEY}, timeout=10) as c:
        yield c
