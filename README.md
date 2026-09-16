# Opportunity Scanner AI

Personal automated system for finding, analyzing, scoring and delivering real earning opportunities.

## Status

Current development state:

- Module 1 — Development Environment: COMPLETED / PASS
- Module 2 — PostgreSQL: COMPLETED / PASS
- Module 3 — Telegram Bot: COMPLETED / PASS
- Module 4 — RSS Collector: COMPLETED / PASS
- Module 5 — Reddit Collector: BLOCKED — DATA ACCESS NOT APPROVED
- Module 6 — Filter Engine: SCOPE APPROVED / IN PROGRESS
- Repository initialized
- Mandatory project documentation: COMPLETED / VERIFIED
- Application code: IN PROGRESS — implemented through the verified Module 4 state; Module 5 remains BLOCKED — DATA ACCESS NOT APPROVED; Module 6 scope is approved under D-030 but implementation has not started

See `PROJECT_STATE.md` for the latest verified state.

## Purpose

Opportunity Scanner AI is designed to:

- automatically monitor approved sources;
- collect potential earning opportunities;
- normalize and deduplicate incoming data;
- remove low-value noise using rule-based filtering;
- extract requirements and payment conditions;
- analyze opportunities with AI only after inexpensive filtering;
- evaluate risk using Anti-Scam logic;
- calculate multidimensional scores;
- store processing history in PostgreSQL;
- send suitable opportunities to Telegram;
- operate continuously in production.

This is a personal tool, not SaaS and not a disposable prototype.

## Approved V1 Sources

- X / Twitter
- Reddit
- Telegram channels
- Discord servers
- RSS / Atom

## Category Priority

1. AI / Data
2. Testing
3. Beginner-friendly Remote Work
4. Web3

## Supported Publication Languages

- English
- Russian
- Ukrainian
- German

User-facing explanations are intended to be in Russian.

## Fixed Logical Architecture

SOURCE
→ COLLECT
→ NORMALIZE
→ DEDUPLICATE
→ FILTER
→ EXTRACT
→ AI
→ RISK
→ SCORE
→ DATABASE
→ TELEGRAM

See `ARCHITECTURE.md` for the authoritative repository architecture document.

## Core Technology Baseline

- Python 3.12
- Git + GitHub
- VS Code
- Docker Desktop
- Docker Compose
- PostgreSQL
- Telegram Bot API
- source-specific official APIs / feeds where applicable
- AI API provider to be selected only when the relevant module requires it

Specific application frameworks and libraries that are not yet approved must not be assumed from this README.

## Security Principles

The system must not automatically:

- perform third-party tasks for the user;
- connect wallets;
- sign transactions;
- send money;
- make deposits;
- expose secrets.

API keys, passwords, tokens, private keys and seed phrases must never be committed to source control.

## Development Roadmap

The approved roadmap contains Module 0 through Module 15.

See `ROADMAP.md` for the fixed module order.

## Repository Documents

- `PROJECT_STATE.md` — latest verified implementation state
- `ARCHITECTURE.md` — approved architecture and boundaries
- `DECISIONS.md` — fixed and deferred decisions
- `ROADMAP.md` — approved module sequence
- `TODO.md` — active work and remaining tasks
- `CHANGELOG.md` — verified project changes
- `README.md` — repository overview
- `SESSION_HANDOFF.md` — controlled MAIN DEVELOPMENT chat continuity template

## Development Method

Development follows:

CURRENT STATE
→ ONE REQUIRED STEP
→ USER RESULT
→ VERIFICATION
→ PASS / FAIL
→ DOCUMENTATION / GIT WHEN REQUIRED
→ NEXT STEP

No module is considered complete merely because code was written.

PASS requires evidence.

## Work Usage

The MAIN DEVELOPMENT chat controls the project.

ChatGPT Work is auxiliary and may be used only at an explicitly declared WORK CHECKPOINT according to `WORK_USAGE_POLICY_v1.0.md`.

## Session Handoff

`SESSION_HANDOFF.md` is used only when preparing an actual transition to a new MAIN DEVELOPMENT chat.

Before handoff, current repository state documentation must be synchronized as required. The new MAIN DEVELOPMENT chat must continue strictly from the recorded `NEXT STEP` and must not restart the project, begin a new audit, or repeat already verified work without a demonstrated technical reason.

This continuity workflow does not change the approved architecture, roadmap, scope, module order or current module decisions.

## Known Unresolved Issues

Known architecture/roadmap contradictions are recorded in `ARCHITECTURE.md`, `DECISIONS.md` and `PROJECT_STATE.md`.

They must not be silently resolved.

## Current Implementation

Application code is implemented through the verified Module 4 state. Module 2, Module 3 and Module 4 are COMPLETED / PASS.

Module 2 — PostgreSQL is COMPLETED / PASS. The local PostgreSQL foundation is implemented, tested, documented and recorded in milestone commit d033d94.

## Local PostgreSQL — Module 2

Run these commands from the repository root.

### Start PostgreSQL

```powershell
docker compose --env-file .env -f compose.yaml up -d postgres
```

### Verify PostgreSQL

```powershell
docker compose --env-file .env -f compose.yaml ps postgres
```

Expected status must include:

```text
(healthy)
```

### Stop PostgreSQL

```powershell
docker compose --env-file .env -f compose.yaml stop postgres
```

### Start Again After Stop

```powershell
docker compose --env-file .env -f compose.yaml up -d postgres
```

### Data Safety

PostgreSQL data is stored in the Docker named volume `postgres_data`.

Do not use:

```powershell
docker compose down -v
```

during normal operation because `-v` removes the PostgreSQL data volume.

A destructive `down -v` is used only for an intentional clean-state reproducibility test.

## Local Telegram Bot — Module 3

The local bot uses the official Telegram Bot API directly over HTTPS with Python 3.12 standard library.

### Configuration

Real Telegram values are stored only in the ignored local .env file.

Required variables:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_OWNER_ID
- TELEGRAM_TARGET_CHAT_ID

TELEGRAM_OWNER_ID authorizes owner-only bot commands.
TELEGRAM_TARGET_CHAT_ID defines the chat used for opportunity notifications.
These remain separate configuration parameters even when they currently refer to the same personal chat.

### Webhook Safety

Before long polling starts, the bot calls getWebhookInfo.
- Empty webhook URL: getUpdates long polling may start.
- Existing webhook URL: the bot stops with BOT_STATUS=BLOCKED_EXISTING_WEBHOOK.
- The bot never calls deleteWebhook automatically.

### Start and Verify

From the repository root run:
python .\src\opportunity_scanner\telegram_bot.py

Expected startup status:
WEBHOOK_CHECK=PASS EMPTY
TELEGRAM_CONFIG=READY
BOT_STATUS=RUNNING

Send /start from the configured owner account.
Expected Russian response: Opportunity Scanner AI запущен. Доступ владельца подтверждён.

Send /test to send the test opportunity message to TELEGRAM_TARGET_CHAT_ID.
The test message includes the approved Module 3 fields and an Открыть URL button.

Stop the bot with Ctrl+C.
Expected shutdown status: BOT_STATUS=STOPPED.

### Secret Safety

Do not print or commit the Telegram bot token or real Telegram IDs.
The real .env file must remain ignored by Git.

## Local RSS Collector — Module 4

Module 4 implements the first working bounded RSS / Atom pipeline:

RSS / Atom → COLLECT → NORMALIZE → PostgreSQL persistence → DEDUPLICATE → basic FILTER → Telegram

The first controlled live verification follows D-027.

### Configuration

Real local configuration is stored only in the ignored `.env` file.

Required Module 4 variable:

```text
RSS_FEED_URLS=<comma-separated explicitly approved RSS / Atom feed URLs>
```

For the first D-027 controlled live verification, configure exactly one explicitly approved RSS / Atom feed URL.

### Preconditions

- PostgreSQL is running and healthy.
- Application PostgreSQL credentials in `.env` are valid.
- Telegram Module 3 configuration is valid.
- Telegram webhook state is empty before Bot API delivery.
- Exactly one RSS / Atom feed URL is configured for the first D-027 live verification.

### Controlled One-Shot Verification

Run from the repository root only when an intentional real live-feed verification is required:

```powershell
.\.venv\Scripts\python.exe -c "import sys; from pathlib import Path; sys.path.insert(0,str(Path.cwd()/'src')); from opportunity_scanner.rss_collector import load_rss_feed_urls,load_database_config,run_bounded_live_feed_verification; from opportunity_scanner.telegram_bot import load_config,verify_no_webhook; urls=load_rss_feed_urls(); assert len(urls)==1,'D-027 requires exactly one configured feed'; token,_,chat=load_config(); verify_no_webhook(token); result=run_bounded_live_feed_verification(urls[0],token,chat,load_database_config()); print(result)"
```

This command performs a real network request to the configured feed and may send at most one Telegram message.

### Expected D-027 Safety Behavior

- The feed may contain many parsed items.
- Only the first item in parser output order may enter persistence and downstream processing.
- Later parser items are not persisted or queued by the bounded verification run.
- A REJECT item sends no Telegram message.
- A PASS item may send at most one Telegram message.
- A normal repeated run remains subject to deduplication and persisted Telegram delivery state.
- An empty or invalid feed must not create false source-item records.

Module 4 does not claim absolute exactly-once Telegram delivery. The D-023 crash window between successful sendMessage and persisted delivery state remains accepted and documented.

Successful D-027 verification does not authorize uncontrolled historical-feed processing and does not introduce scheduler infrastructure.

### Secret Safety

Do not print or commit PostgreSQL passwords, Telegram tokens, Telegram IDs, or the real `.env` file.
