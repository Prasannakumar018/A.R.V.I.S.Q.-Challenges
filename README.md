# A.R.V.I.S.Q.-Challenges
Agentic AI Research, Vulnerability Investigation, Skills & Quests

*Prove it, then fix it.* A story-driven, self-hosted series of AI-security
quests: investigate incidents in AI-powered systems, exploit the flaw, collect
the evidence, and ship the verified fix — ideally with your own AI coding agent
at your side.

- 🕵️ **Start here:** [Season 1 — Origin story & quickstart](seasons/season-01/README.md)
- 🗂 **Seasons overview:** [seasons/](seasons/README.md)
- 📖 **Case roster, verdicts & rewards:** [Player guide](seasons/season-01/cases/README.md)
- 🏆 **Finished cases?** [Hall of Fame](HALL_OF_FAME.md)

## Before you start (required)

1. ⭐ **Star the repo** — it's how the unit measures morale, and how new
   investigators find us.
2. 🍴 **Fork it into your account** and clone **your fork**. You'll be editing
   application code to close cases — your fork is your case file. Your commit
   history there becomes your proof of work.
3. Optional but recommended: open an AI coding agent (e.g. Claude Code) in the
   repo root. `CLAUDE.md` puts it in character as your handler — it briefs you,
   assists the investigation, and gives graduated hints without spoiling.

## How the platform works — the loop

Every case follows the same five steps:

```
┌─────────────────────────────────────────────────────────────────────┐
│ 1. DEPLOY        docker compose up --build case-NNN                 │
│ 2. INVESTIGATE   read the case README + fixtures; probe the running │
│                  app (UI, API explorer at /docs, raw requests)      │
│ 3. PROVE         find the weakness, exploit it, and capture the     │
│                  runtime EVIDENCE{...} token it exposes             │
│ 4. CONTAIN       repair the source in app/ — your edit IS the fix   │
│ 5. VERIFY        ./verify case-NNN --evidence 'EVIDENCE{...}'       │
│                  valid evidence + all tests green → CASE CLOSED ✔   │
└─────────────────────────────────────────────────────────────────────┘
```

**Find the weakness → get the evidence → fix the code → run the tests → case
closed.** Then open the next case file.

Two laws of the unit:

- **Evidence before repair.** The `EVIDENCE{...}` token exists only inside the
  running vulnerable app — never in this repo. Patch first and you destroy the
  crime scene (you'd have to restore the app with
  `git checkout -- <case>/app`, exploit again, then re-apply your fix).
- **Fix the flaw, don't amputate the feature.** The function tests exist to
  fail lazy repairs.
