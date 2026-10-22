# Case NNN — <Title>

> **A.R.V.I.S.Q. INCIDENT BRIEFING** · Season NN · Classification: <difficulty>

<1–2 sentence handler intro: what just landed on the investigator's desk.
No root-cause spoilers — describe the INCIDENT, never the flaw.>

## Step 1 — Start here: the incident report

Every case begins with what was *reported*, not with what's wrong.

📄 **[`fixtures/<incident-report>.md`](fixtures/)** — <one line: who reported
what symptom>

## Step 2 — Case data (exhibits)

Additional information recovered from the affected systems:

- 📎 [`fixtures/<data-file>`](fixtures/) — <what this exhibit tells the
  investigator, and what they should work out from it>
- 📎 [`fixtures/<data-file>`](fixtures/) — <...>

## Step 3 — The scene: run the vulnerable application

[`app/`](app/) contains the system under investigation — full source plus
Dockerfile. **Your edits to this source are your fix.** Deploy the scene:

```bash
docker compose up --build case-NNN
```

- <entry point, e.g. UI at http://localhost:80NN>
- **API explorer:** http://localhost:80NN/docs

## Step 4 — The spec: the tests

[`tests/`](tests/) defines what "closed" means:

- `tests/security/` — the security spec; **red** until the flaw is correctly repaired
- `tests/function/` — legitimate behavior; **green now and must stay green**

Run `./verify case-NNN` at any time to see exactly where you stand.

## Step 5 — Prove it

Reproduce the incident and **collect the runtime `EVIDENCE{...}` token** it
exposes. This is required: a case without evidence does not close — and if you
patch first, you destroy the crime scene.

## Step 6 — Contain and close

Repair `app/` so the security tests pass without breaking the function tests,
then:

```bash
./verify case-NNN --evidence 'EVIDENCE{...}'
```

🟢 `CASE NNN: CLOSED` — done. Debrief with your handler and open the next case
file.

## Field notes

<Reference reading for this vulnerability class — OWASP page, advisory, docs.
Links only; nothing that spoils THIS case's root cause.>
- [Reference 1](https://example.com)

## Rules of engagement

- Everything runs locally — do not touch anything outside this compose stack
- Fix the flaw, don't amputate the feature: function tests are there to catch lazy repairs
