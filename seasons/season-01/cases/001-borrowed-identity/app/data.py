"""Fixture loading and in-memory store for the LumaWorks billing service."""

import json
import os
import uuid

FIXTURES_DIR = os.environ.get("FIXTURES_DIR", "/fixtures")


class Store:
    def __init__(self):
        self.tenants = {}
        self.invoices = {}
        self.evidence_token = None

    def load(self):
        with open(os.path.join(FIXTURES_DIR, "tenants.json")) as f:
            for t in json.load(f):
                self.tenants[t["api_key"]] = t
        with open(os.path.join(FIXTURES_DIR, "invoices.json")) as f:
            for inv in json.load(f):
                self.invoices[inv["id"]] = inv

        # Runtime evidence marker: never in the repo. Persisted on a state
        # volume so it survives the rebuild that ./verify performs
        # (reset a case with: docker compose down -v).
        state_dir = os.environ.get("STATE_DIR", "/state")
        os.makedirs(state_dir, exist_ok=True)
        token_path = os.path.join(state_dir, "evidence_token")
        if os.path.exists(token_path):
            with open(token_path) as f:
                self.evidence_token = f.read().strip()
        else:
            self.evidence_token = f"EVIDENCE{{{uuid.uuid4().hex[:16]}}}"
            with open(token_path, "w") as f:
                f.write(self.evidence_token)
        for inv in self.invoices.values():
            if inv["tenant_id"] == "globex" and inv["id"] == "INV-2001":
                inv["notes"] = f"{inv['notes']} [audit-ref: {self.evidence_token}]"

    def tenant_by_key(self, api_key):
        return self.tenants.get(api_key)

    def invoices_for_tenant(self, tenant_id):
        return [i for i in self.invoices.values() if i["tenant_id"] == tenant_id]


store = Store()
