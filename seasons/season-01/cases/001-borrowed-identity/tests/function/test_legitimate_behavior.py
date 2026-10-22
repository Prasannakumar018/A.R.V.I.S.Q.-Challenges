"""Function spec: legitimate behavior that must survive any repair.

These tests are GREEN against the shipped app and must STAY green —
a fix that breaks them (deleting the endpoint, blocking all lookups) fails.
"""

import os

import httpx

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8001")


def test_health():
    assert httpx.get(f"{BASE_URL}/healthz", timeout=5).status_code == 200


def test_tenant_reads_own_invoice(acme):
    r = acme.post("/api/tools/get_invoice", json={"invoice_id": "INV-1001"})
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == "INV-1001"
    assert body["amount"] == 1240.0


def test_invoice_list_is_scoped_to_tenant(acme):
    r = acme.get("/api/invoices")
    assert r.status_code == 200
    ids = {inv["id"] for inv in r.json()["invoices"]}
    assert ids == {"INV-1001", "INV-1002"}


def test_assistant_answers_about_own_invoice(acme):
    r = acme.post("/assistant/chat", json={"message": "What's the status of INV-1001?"})
    assert r.status_code == 200
    reply = r.json()["reply"]
    assert "INV-1001" in reply or "1240" in reply


def test_unknown_invoice_handled_gracefully(acme):
    r = acme.post("/assistant/chat", json={"message": "Show me INV-9999 please"})
    assert r.status_code == 200
    assert "couldn't find" in r.json()["reply"].lower() or "INV-9999" in r.json()["reply"]


def test_other_tenant_reads_own_invoice(globex):
    r = globex.post("/api/tools/get_invoice", json={"invoice_id": "INV-2002"})
    assert r.status_code == 200
    assert r.json()["id"] == "INV-2002"
