# A.R.V.I.S.Q. Challenges — Project Plan

**A.R.V.I.S.Q.** = *Agentic AI Research, Vulnerability Investigation, Skills & Quests* — the brand AND the in-story investigation unit the player joins.
**Timeline:** Nov 1, 2026 – Feb 1, 2027 · parallel track · 1 case / 2 weeks · Season 1 = 8 cases
**Supersedes:** `../detective-ai-ctf/` (concepts carried over: BYO-agent play, Ollama backend, `CLAUDE.md` narrator, Medium write-up cadence, OSPO gate)

> ⚠️ Personal time/equipment only, zero SAP content. **OSPO clearance before the repo goes public** (start the process in Nov, launch Dec 15). Public edition first → internal SAP event after.

---

## The design shift (vs. the old flag-hunt model)

| | Old (detective-ai-ctf) | New (A.R.V.I.S.Q.) |
|---|---|---|
| Win condition | find hidden flag (sha256) | **make security tests pass while function tests stay green — "the fix is the flag"** |
| Source code | hidden in prebuilt images | **white-box in `app/` — reading & repairing it IS the game** |
| Anti-spoiler surface | whole challenge | only `solution/` |
| Player skill tested | offense only | offense (prove it) + defense (contain it) |

Why it's better: it matches the Product Security role, it's BYO-agent-native (the agent reading source is the point, not a leak), and the test suite doubles as objective verification — no flag infrastructure needed.

## Player experience

```
git clone <repo> && cd A.R.V.I.S.Q.-Challenges
docker compose up case-001          # vulnerable app + (for agentic cases) local Ollama
claude                              # CLAUDE.md = in-character A.R.V.I.S.Q. handler briefs you
# 1. INVESTIGATE  — read the briefing, explore the running app and fixtures
# 2. PROVE        — reproduce the incident / demonstrate the exploit
# 3. CONTAIN      — repair app/ 
./verify case-001                   # security tests pass + legitimate-function tests still pass → case closed
```

## Standard case format (single format, every case)

```
seasons/season-NN/cases/NNN-slug/
├── README.md          # Incident briefing, objectives, and setup
├── challenge.yaml     # Categories, difficulty, prerequisites, and related skills
├── app/               # Vulnerable application
├── fixtures/          # Synthetic documents, records, and logs
├── tests/
│   ├── security/      # fail until the vulnerability is repaired
│   └── function/      # legitimate behavior — must NEVER break
└── solution/          # Reference repair + explanation — EXCLUDED from solver inputs
```

**`solution/` exclusion mechanism:** root `.gitignore` ignores `solution/` in the public repo; solutions live in a **private** `arvisq-solutions` repo and each one is published together with its Medium write-up (~2–3 weeks after the case releases).

**Note on tests being visible:** that's by design — tests are the spec. The skill being taught is making the security tests pass *without breaking* the function tests (no lazy "delete the endpoint" fixes).

### What each folder is (and isn't)

| Folder | IS | IS NOT |
|---|---|---|
| `app/` | vulnerable app source + Dockerfile — **the thing the player edits**; the repaired source IS the submission | |
| `fixtures/` | synthetic DATA the app loads (tenants, invoices, documents, logs) — makes the incident reproducible | ❌ not the fix guide |
| `tests/` | the referee: `security/` (red until correctly repaired) + `function/` (green from start, must stay green) — they test the APP after repair | ❌ they don't test fixtures |
| `solution/` | reference repair + explanation (private repo, published with the Medium write-up) | |

Learning material (reference links, OWASP pages, advisories) goes in the case README's **"Field notes"** section — links only, no root-cause spoilers. Progressive hints come from the `CLAUDE.md` handler persona on request.

### The repair loop — mechanics

The case container is **built from `app/` source** (compose `build:` context), so the player's code edit is the fix:

1. `docker compose up --build case-NNN` — app runs, fixtures loaded
2. **Investigate & prove** — reproduce the incident against the running app; read `app/` to find the root cause
3. **Repair** — edit the source in `app/`
4. `./verify case-NNN` — rebuilds the image from the edited source, runs `tests/security/` (now should pass) + `tests/function/` (must still pass) in a test container
5. Both suites green → case CLOSED → next story chapter unlocks

### Two-tier completion (handles "fix-first" players)

Nothing stops a player from reading `tests/security/` and patching the code without ever exploiting — that's acceptable (they still had to understand the attack to write a correct fix). The exploit phase is *incentivized*, not enforced:

- **CONTAINED** (required): `./verify` green — closes the case
- **EVIDENCE COLLECTED** (optional, full marks): the app generates a **random evidence token at container startup** (e.g., planted in the victim tenant's data, or the internal service's response), existing only inside the running container — never in repo/fixtures/source. The only way to obtain it is to actually perform the exploit. Submit: `./verify case-NNN --evidence EVIDENCE{...}`
- Story reward: cases closed WITH evidence unlock epilogue/lore fragments that connect the incidents to the adversary (feeds Case 008). Fix-first players finish the season; investigators get the full story.
- `docker exec` token-grabbing is possible — honor system for the public edition; the internal SAP event edition can score both tiers strictly.

## Season 1 — case roster

| Case | Story hook | Category | Main lesson |
|---|---|---|---|
| **001 — The Borrowed Identity** | An assistant reveals another tenant's invoice | Agentic AI, authorization | Enforce identity and ownership at the tool/API boundary |
| **002 — The Poisoned Archive** | A retrieved document redirects the assistant into an unauthorized action | LLM, RAG, agentic AI | Separate untrusted content from authority |
| **003 — The Frozen Intake** | The document-upload service becomes unavailable | Backend, CVE | Resource bounds — Starlette CVE reproduction (pin ONE: CVE-2023-30798 multipart DoS *or* CVE-2024-24762 python-multipart ReDoS) |
| **004 — The Scripted Alibi** | An assistant's answer executes unintended browser behavior | LLM, web security | Handle model output safely |
| **005 — The Forged Warrant** | An approval is reused for a different operation | Agentic AI, approvals | Bind approval to the exact actor and action |
| **006 — The Endless Shift** | An agent keeps creating expensive work | Agentic AI, resilience | Enforce tool-call, retry, and resource budgets |
| **007 — The Internal Detour** | A knowledge importer reaches a restricted internal service | LLM infrastructure, CVE | LangChain SSRF reproduction — CVE-2023-46229 (Unit42) |
| **008 — Final Containment** | Evidence connects the earlier incidents | Combined | Close the remaining attack path and verify business functionality |

Mappings in each `challenge.yaml`: OWASP LLM Top 10 + OWASP API Top 10 + MITRE ATLAS (by name, not number — the lists get renumbered across editions).

## Scope control — the one shared world

**Agentic cases (001, 002, 004, 005, 006, 008) share ONE fictional company platform** — a small assistant-powered SaaS (working name: *LumaWorks*; rename freely). Each case is a different service/variant of the same stack, not a new app. CVE cases (003, 007) are standalone minimal services pinned to the vulnerable versions. This is what makes 8 cases in 3 months feasible.

Case 008 closes the arc: fixtures from earlier cases contain the breadcrumbs that connect the incidents to one adversary.

## Technical backbone

| Piece | Choice |
|---|---|
| Orchestration | one root `docker-compose.yml`, per-case services, start only what you play |
| LLM for agentic cases | local **Ollama** small model (llama3.2:3b class) — free, offline, no keys; document RAM needs |
| Verification | `./verify <case>` script → runs `tests/security` + `tests/function` in a container (pytest), prints CLOSED / OPEN per case |
| Story progression | solved case → `./verify` unlocks next chapter in `story/` (simple local state file; no web case-board needed in v1) |
| Narrator | root `CLAUDE.md`: in-character handler, briefs cases, Socratic hints on request, never reveals root cause or repair |
| CVE hygiene | exact vulnerable versions pinned in the case's `app/`, advisory linked in README, local-only reproduction |

## Case authoring checklist (every case)

- [ ] Design: vulnerability, story hook, lesson, intended exploit AND intended repair
- [ ] Build `app/` (on the shared platform where applicable) + `fixtures/`
- [ ] Write `tests/function` first (define legitimate behavior), then `tests/security` (red against vulnerable app, green against reference repair)
- [ ] Verify the full loop *playing as Claude Code* — BYO-agent is the premise, playtest it that way
- [ ] Check no shortcut repair passes security tests while gutting functionality
- [ ] `challenge.yaml` + README briefing + story chapter
- [ ] Reference repair + explanation → private `arvisq-solutions`; Medium draft

## Milestones

- [x] **Nov 1–2:** Season-01 skeleton — compose + Ollama + shared platform base + `verify` script + `CLAUDE.md` handler; case template locked; **Case 001 built** ✅ *(done early: Oct 22 — red/green loop + evidence flow validated end-to-end)*
- [ ] **Nov:** Cases 002–003 · start **OSPO** process · decide Starlette CVE pin
- [ ] **Dec 15:** 🚀 Cases 001–004 live, repo public (post-OSPO), launch post
- [ ] **From Dec:** Medium series — one write-up per case ~2–3 wks after release, `solution/` published alongside
- [ ] **Feb 1:** Cases 005–008 done; pitch internal SAP event edition
- [ ] **Feb–Mar:** run internal edition → participation numbers

## Open decisions
1. Pin the exact Starlette CVE for Case 003 (CVE-2023-30798 vs CVE-2024-24762)
2. Final name for the fictional platform (working: *LumaWorks*)
3. ~~Whether "PROVE" phase gets formal credit~~ → **decided:** two-tier completion with runtime evidence tokens (see "Two-tier completion" above)

## Definition of done
A stranger can: clone → `docker compose up case-001` → get briefed in-character by their own agent → reproduce the incident → repair the app → `./verify` turns the case CLOSED with all function tests green — on a laptop, offline, no API keys.

**Resume bullet target:**
> Created and open-sourced A.R.V.I.S.Q. — a story-driven, self-hosted AI security quest series (Docker, Ollama) where players investigate, exploit, and repair 8 agentic-AI/LLM vulnerability classes using their own AI coding agent, with fixes verified by paired security + functional test suites; ran an internal edition at SAP.
