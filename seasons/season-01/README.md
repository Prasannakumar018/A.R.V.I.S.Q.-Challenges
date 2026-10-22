# Season 1 — "The Conductor"

> **A.R.V.I.S.Q. — Agentic AI Research, Vulnerability Investigation, Skills & Quests**
> *Prove it, then fix it.*

## Origin — how this season began

**LumaWorks** was a mid-size SaaS company nobody outside its industry had heard
of — until the quarter it bolted an AI assistant onto everything it shipped.
Billing, document intake, support, approvals, knowledge import: one ambitious
rollout, and suddenly "Luma" was answering questions, summarizing archives,
filing requests, and clicking buttons on behalf of thousands of customers.

Revenue went up. So did the strange tickets.

A customer opened a support case with a screenshot: Luma had cheerfully
summarized **another company's invoice** — they'd only *asked*. A week later an
archived document made an assistant do something nobody had requested. Then the
document-intake service froze solid during a routine upload. An approval that a
manager had granted once was somehow honored *twice* — for a different
operation. Each incident looked like an isolated bug. Bad luck. Sloppy code.

The board didn't believe in that much bad luck. They retained **A.R.V.I.S.Q.**,
an independent unit that investigates AI-era incidents the way detectives work
crime scenes: **evidence first, repair second, lessons always.**

You are the unit's newest field investigator. Your handler will brief you one
case at a time. Two rules before your first assignment:

1. **Collect evidence before you touch anything.** A patched system tells no
   tales. If you fix the flaw before capturing proof, you've destroyed the
   crime scene — and the case stays open.
2. **Fix the flaw, don't amputate the feature.** LumaWorks still has to run a
   business. A repair that breaks legitimate customers is not a repair.

One more thing. The fragments recovered so far — tokens, logs, patterns across
systems that should have nothing in common — suggest these incidents are not
accidents. Someone, or something, is orchestrating them. The analysts have
started calling it **the Conductor**. Close cases, collect evidence, and by the
final containment you'll know what that name means.

## Quickstart

**Requirements:** Docker (with Compose), git, a terminal. Recommended: an AI
coding agent such as [Claude Code](https://claude.com/claude-code) — this
season is designed to be investigated *with* your agent, and the repo's
`CLAUDE.md` puts it in character as your handler. Optional: Ollama for the
assistants' conversational layer (every case also works without it).

```bash
# 0. Star this repo, then FORK it — you'll be editing code, so work in your fork
git clone https://github.com/<you>/A.R.V.I.S.Q.-Challenges.git
cd A.R.V.I.S.Q.-Challenges

# 1. Deploy your first crime scene
docker compose up --build case-001

# 2. Get briefed (optional, recommended): open your AI agent in the repo root
claude   # your agent becomes your A.R.V.I.S.Q. handler

# 3. Read the case file and start investigating
#    seasons/season-01/cases/001-borrowed-identity/README.md
#    Customer portal: http://localhost:8001   API explorer: http://localhost:8001/docs

# 4. When you've exploited the flaw and collected EVIDENCE{...}, repair app/ and:
./verify case-001 --evidence 'EVIDENCE{...}'
# CASE 001: CLOSED → move to the next case file
```

Full rules of the game, the case roster with difficulties, and what you earn:
**[cases/Player_Guide.md](cases/Player_Guide.md)**.
