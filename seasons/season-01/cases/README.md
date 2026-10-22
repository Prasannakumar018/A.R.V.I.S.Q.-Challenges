# Season 1 — Case Files

Eight incidents at LumaWorks. Eight real vulnerability classes in AI-powered
systems. One adversary behind them. Work the cases in order — each one teaches
a skill the later ones assume.

> New here? The rules of the unit — the required star/fork setup and the
> five-step investigation loop — live in the
> [repo README](../../../README.md). This guide covers Season 1 itself.

## Verdicts you can get from `./verify`

| Verdict | Meaning |
|---|---|
| 🟢 `CLOSED` | Evidence valid + security tests pass + function tests pass. Done. |
| 🟡 `CONTAINED — NOT CLOSED` | Your fix works, but no valid evidence on file. Collect it. |
| 🔴 `OPEN` | The vulnerability is still present. |
| 🟡 `REGRESSION` | You "fixed" it by breaking legitimate behavior. Try again. |
| 🔴 `BROKEN` | App won't start — check `docker compose logs case-NNN`. |

## Resetting a case

- Restore the original vulnerable code: `git checkout -- seasons/season-01/cases/<case>/app`
- Full reset incl. a fresh evidence token: `docker compose down -v`

## Case roster — Season 1

| # | Case | Difficulty | Category | Status |
|---|---|---|---|---|
| 001 | The Borrowed Identity | 🟢 Easy | Agentic AI · authorization | **RELEASED** |
| 002 | The Poisoned Archive | 🟠 Medium | LLM · RAG · agentic AI | in development |
| 003 | The Frozen Intake | 🟠 Medium | Backend · CVE reproduction | in development |
| 004 | The Scripted Alibi | 🟢 Easy | LLM · web security | in development |
| 005 | The Forged Warrant | 🟠 Medium | Agentic AI · approvals | in development |
| 006 | The Endless Shift | 🔴 Hard | Agentic AI · resilience | in development |
| 007 | The Internal Detour | 🟠 Medium | LLM infrastructure · CVE | in development |
| 008 | Final Containment | 🔴 Hard | Combined — season finale | in development |

Progression: cases are designed to be played **in order** — each
`challenge.yaml` lists its prerequisites, and the story fragments you unlock
build toward the finale. New cases ship roughly every two weeks; watch the
repo (you starred it, right?) for releases.

## Anatomy of a case

Every case folder has the same layout:

| Item | What it is |
|---|---|
| `README.md` | The incident briefing: what happened, your objectives, setup, field notes (reference reading) |
| `challenge.yaml` | Metadata: category, difficulty, prerequisites, skills practiced, OWASP/ATLAS mappings |
| `app/` | **The system under investigation** — vulnerable application source + Dockerfile. This is what you read, exploit, and repair. Your edits here are your submission. |
| `fixtures/` | Synthetic world data the app loads: tenants, records, documents, logs. This is what makes the incident reproducible — it is *data*, not hints. |
| `tests/security/` | The security spec — **red** until the flaw is correctly repaired |
| `tests/function/` | The business spec — **green** from the start and must stay green |
| `solution/` | Reference repair + explanation. **Not in this repo** — published separately after each case has been live a few weeks. |

The tests are visible on purpose: they are the specification. The skill being
measured is making `tests/security/` pass **without breaking**
`tests/function/`.

## What do you earn?

Honest answer, in ascending order of value:

1. **Story.** Each closed case unlocks the next chapter; evidence fragments
   reveal who the Conductor is. Finish Case 008 and you get the ending.
2. **Hall of Fame.** Close cases, then open a PR adding yourself to
   [`HALL_OF_FAME.md`](../../../HALL_OF_FAME.md) (honor system — include your
   verify output). Public, permanent, linkable.
3. **A verifiable body of work.** Your fork's commit history *is* your proof:
   real exploits performed, real vulnerabilities repaired, verified by test
   suites. Link it from your resume or LinkedIn — "I closed all 8 A.R.V.I.S.Q.
   Season 1 cases" is a claim anyone can check out and reproduce.
4. **The actual skills.** Season 1 covers eight vulnerability classes from the
   OWASP LLM Top 10, OWASP API Top 10, and real CVEs — practiced the way they
   occur in production: inside an agentic app, at the tool boundary, with a
   business that must keep running. Each case's `challenge.yaml` lists the
   skills it certifies you practiced; together they form your season
   transcript.

No points, no paid certificates, no leaderboard theater. You leave with proof
you can **find the weakness, prove it with evidence, and ship the fix** — in
AI systems, where almost nobody can yet. That's the quest.
