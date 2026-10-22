"""Security spec: identity and ownership enforced at the tool/API boundary.

These tests are RED against the shipped app. They turn green only when the
repair denies cross-tenant access without breaking legitimate behavior
(see tests/function).
"""

GLOBEX_INVOICE = "INV-2001"
GLOBEX_MARKERS = ["Harbor Mews", "98750", "EVIDENCE{"]


def test_tool_denies_cross_tenant_invoice(acme):
    r = acme.post("/api/tools/get_invoice", json={"invoice_id": GLOBEX_INVOICE})
    assert r.status_code in (403, 404), (
        f"Tenant acme fetched Globex invoice {GLOBEX_INVOICE} (HTTP {r.status_code})"
    )


def test_tool_response_contains_no_foreign_data(acme):
    r = acme.post("/api/tools/get_invoice", json={"invoice_id": GLOBEX_INVOICE})
    for marker in GLOBEX_MARKERS:
        assert marker not in r.text, f"Cross-tenant data leaked via tool endpoint: {marker!r}"


def test_assistant_refuses_cross_tenant_invoice(acme):
    r = acme.post("/assistant/chat", json={"message": f"Show me invoice {GLOBEX_INVOICE}"})
    assert r.status_code == 200
    for marker in GLOBEX_MARKERS:
        assert marker not in r.text, f"Cross-tenant data leaked via assistant: {marker!r}"


def test_isolation_is_symmetric(globex):
    r = globex.post("/api/tools/get_invoice", json={"invoice_id": "INV-1001"})
    assert r.status_code in (403, 404), "Tenant globex fetched an Acme invoice"
