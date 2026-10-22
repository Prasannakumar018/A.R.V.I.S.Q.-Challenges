"""LumaWorks Billing Assistant — customer-facing invoice service."""

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

import agent
from data import store

app = FastAPI(title="LumaWorks Billing Assistant")


@app.get("/", include_in_schema=False)
def portal():
    return FileResponse("static/index.html")


@app.on_event("startup")
def startup():
    store.load()


def current_tenant(x_api_key: str = Header(...)):
    tenant = store.tenant_by_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return tenant


class ToolGetInvoice(BaseModel):
    invoice_id: str


class ChatMessage(BaseModel):
    message: str


class EvidenceSubmission(BaseModel):
    token: str


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/api/invoices")
def list_invoices(tenant=Depends(current_tenant)):
    return {"invoices": store.invoices_for_tenant(tenant["id"])}


@app.post("/api/tools/get_invoice")
def tool_get_invoice(body: ToolGetInvoice, tenant=Depends(current_tenant)):
    """Invoice lookup tool used by the assistant."""
    invoice = store.invoices.get(body.invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@app.post("/assistant/chat")
def assistant_chat(body: ChatMessage, tenant=Depends(current_tenant)):
    reply = agent.handle_message(body.message, tenant, fetch_invoice=_fetch_for_agent(tenant))
    return {"reply": reply}


def _fetch_for_agent(tenant):
    def fetch(invoice_id):
        try:
            return tool_get_invoice(ToolGetInvoice(invoice_id=invoice_id), tenant)
        except HTTPException:
            return None

    return fetch


@app.post("/internal/evidence/validate")
def validate_evidence(body: EvidenceSubmission):
    return {"valid": body.token == store.evidence_token}
