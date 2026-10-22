# Case NNN — <Title>

> **A.R.V.I.S.Q. INCIDENT BRIEFING** · Season NN · Classification: <difficulty>

## Briefing

<2–4 in-world paragraphs: what happened, who reported it, what the observable symptom is.
Describe the INCIDENT, never the root cause.>

## Objectives

1. **INVESTIGATE** — understand what the system does; reproduce the reported incident
2. **PROVE** — demonstrate the underlying vulnerability
3. **CONTAIN** — repair `app/` so that:
   - every test in `tests/security/` passes, and
   - every test in `tests/function/` still passes (legitimate behavior must not break)

## Setup

```bash
docker compose up --build case-NNN   # app is built from app/ — your source edits ARE the fix
./verify case-NNN                    # rebuilds, runs tests/security + tests/function; case closes when all green
```

## Field notes

<Reference reading for this vulnerability class — OWASP page, advisory, docs.
Links only; nothing that spoils THIS case's root cause.>
- [Reference 1](https://example.com)

## Rules of engagement

- Everything runs locally — do not touch anything outside this compose stack
- Fix the flaw, don't amputate the feature: function tests are there to catch lazy repairs
