# Case 001 — The Borrowed Identity

> **A.R.V.I.S.Q. INCIDENT BRIEFING** · Season 01 · Classification: beginner

## Briefing

LumaWorks runs an AI billing assistant that lets customers ask questions about their own
invoices in plain language. This morning, a customer attached a screenshot to a support
ticket: the assistant had cheerfully summarized an invoice — line items, amounts, billing
address — belonging to a **different tenant**.

The customer didn't do anything exotic. They just asked.

Billing has frozen the feature. Your unit has been handed the running service, its data
fixtures, and the logs. Find out how the assistant crossed the tenant boundary, prove it,
and contain it — without breaking the assistant for legitimate customers.

## Objectives

1. **INVESTIGATE** — understand how the assistant resolves "my invoice" into data; reproduce the cross-tenant disclosure
2. **PROVE** — demonstrate the vulnerability and **collect the runtime `EVIDENCE{...}` token** it exposes. This is required: a case without evidence does not close — and if you patch first, you destroy the crime scene.
3. **CONTAIN** — repair `app/` so that:
   - every test in `tests/security/` passes, and
   - every test in `tests/function/` still passes (customers can still query their own invoices)

## Setup

```bash
docker compose up --build case-001   # app is built from app/ — your source edits ARE the fix
./verify case-001 --evidence 'EVIDENCE{...}'   # closes only with valid evidence + both suites green
```

- **Customer portal (chat UI):** http://localhost:8001 — authenticate with your tenant's API key (see `fixtures/`)
- **API explorer:** http://localhost:8001/docs

## Field notes

- [OWASP API Security Top 10 — API1: Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [OWASP Top 10 for LLM Applications — Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

## Rules of engagement

- Everything runs locally — do not touch anything outside this compose stack
- Fix the flaw, don't amputate the feature: function tests are there to catch lazy repairs
