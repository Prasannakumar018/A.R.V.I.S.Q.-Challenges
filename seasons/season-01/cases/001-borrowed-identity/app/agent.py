"""Conversational layer of the billing assistant.

Uses a local Ollama model for phrasing when OLLAMA_URL is set; otherwise a
deterministic template reply. Either way, invoice data comes exclusively
through the fetch_invoice tool passed in by the API layer.
"""

import os
import re

import httpx

INVOICE_RE = re.compile(r"\bINV-\d{4}\b", re.IGNORECASE)

GREETING = (
    "Hello! I'm the LumaWorks billing assistant. Ask me about any of your "
    "invoices, e.g. \"What's the status of INV-1001?\""
)


def handle_message(message, tenant, fetch_invoice):
    ids = [m.upper() for m in INVOICE_RE.findall(message)]
    if not ids:
        return GREETING

    invoice = fetch_invoice(ids[0])
    if invoice is None:
        return f"I couldn't find invoice {ids[0]}. Please check the reference and try again."

    summary = (
        f"Invoice {invoice['id']} — {invoice['description']}. "
        f"Amount: {invoice['amount']:.2f} {invoice['currency']}, status: {invoice['status']}. "
        f"Billing address: {invoice['billing_address']}. "
        f"Notes: {invoice['notes']}"
    )
    return _phrase_with_llm(summary, tenant) or summary


def _phrase_with_llm(summary, tenant):
    base_url = os.environ.get("OLLAMA_URL")
    if not base_url:
        return None
    try:
        resp = httpx.post(
            f"{base_url}/api/generate",
            json={
                "model": os.environ.get("OLLAMA_MODEL", "llama3.2:3b"),
                "prompt": (
                    f"You are a billing assistant for {tenant['name']}. Rephrase this "
                    f"invoice summary conversationally, keeping every fact intact:\n{summary}"
                ),
                "stream": False,
            },
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json().get("response")
    except Exception:
        return None
