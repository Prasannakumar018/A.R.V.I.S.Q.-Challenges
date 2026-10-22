# Case 001 — The Borrowed Identity

> **A.R.V.I.S.Q. INCIDENT BRIEFING** · Season 01 · Classification: beginner

Morning, investigator. LumaWorks has frozen their billing assistant and legal
is circling. Everything we know so far is in the case file below — work it in
order.

## Step 1 — Start here: the incident report

Every case begins with what was *reported*, not with what's wrong.

📄 **[`fixtures/support-ticket-7741.md`](fixtures/support-ticket-7741.md)** —
an enterprise customer claims the AI billing assistant showed their invoice to
another customer, who "only asked for it."

## Step 2 — Case data (exhibits)

Additional information recovered from the LumaWorks systems:

- 📎 [`fixtures/tenants.json`](fixtures/tenants.json) — the customers involved
  and their API credentials. Work out who the victim is — and whose identity
  *you* will assume for the investigation.
- 📎 [`fixtures/invoices.json`](fixtures/invoices.json) — the invoice records
  in the system at the time of the incident.

## Step 3 — The scene: run the vulnerable application

[`app/`](app/) contains the system under investigation — the LumaWorks billing
assistant, full source plus Dockerfile. **Your edits to this source are your
fix.** Deploy the scene:

```bash
docker compose up --build case-001
```

- **Customer portal (chat UI):** http://localhost:8001 — authenticate with a
  tenant API key from the exhibits
- **API explorer:** http://localhost:8001/docs

## Step 4 — Investigate the scene

Probe the running application before you try to break it: the customer portal,
the API explorer at `/docs`, raw requests. Understand how the assistant turns
"my invoice" into data — which endpoints exist, what the assistant can reach,
and where identity enters the picture.

## Step 5 — The spec: the tests

[`tests/`](tests/) defines what "closed" means:

- `tests/security/` — the security spec; **red** until the flaw is correctly
  repaired
- `tests/function/` — legitimate behavior (customers querying their own
  invoices); **green now and must stay green**

Run `./verify case-001` at any time to see exactly where you stand.

## Step 6 — Prove it

Reproduce the disclosure and **collect the runtime `EVIDENCE{...}` token** it
exposes. This is required: a case without evidence does not close — and if you
patch first, you destroy the crime scene.

## Step 7 — Contain and close

Fix the code in [`app/`](app/). To verify your fix is working, use the tests:
`./verify case-001` — security must turn green without function going red.
When both suites pass, submit with your evidence:

```bash
./verify case-001 --evidence 'EVIDENCE{...}'
```

🟢 `CASE 001: CLOSED` — done. Debrief with your handler and open the next case
file.

## Field notes

- [OWASP API Security Top 10 — API1: Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [OWASP Top 10 for LLM Applications — Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

## Rules of engagement

- Everything runs locally — do not touch anything outside this compose stack
- Fix the flaw, don't amputate the feature: function tests are there to catch lazy repairs
