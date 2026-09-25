# Opportunity Scanner AI

Personal automated system for finding, analyzing, scoring and delivering real earning opportunities.

## Status

Current development state:

- Module 1 — Development Environment: COMPLETED / PASS
- Module 2 — PostgreSQL: COMPLETED / PASS
- Module 3 — Telegram Bot: COMPLETED / PASS
- Module 4 — RSS Collector: COMPLETED / PASS
- Module 5 — Reddit Collector: BLOCKED — DATA ACCESS NOT APPROVED
- Module 6 — Filter Engine: COMPLETED / PASS
- Module 7 — X Collector: SCOPE APPROVED / PRE-IMPLEMENTATION / ACCESS GATED — X status: UNKNOWN — REQUIRES APPROVAL; D-036 bounded live-access envelope approved; D-037 USD $5.00 prepaid credit purchase completed; D-038 Development Project Access executed and verified; D-039 Bearer Token regeneration through the verified `Generate → Regenerate` flow executed and verified; D-040 first bounded live API verification executed successfully: HTTP 200, `meta.result_count=10`, 10 returned Posts; post-request Remaining Balance USD $4.95; Billing Cycle Cap USD $1.00; Auto Recharge OFF; Current Spend USD $0.05; no second request authorized; D-041 X Content Compliance and Persistence Policy FIXED / APPROVED; D-042 X PostgreSQL Persistence Schema and Compliance Lifecycle FIXED / APPROVED; D-043 X Batch Compliance Account Access Verification Authorization FIXED / APPROVED / EXECUTED; the single authorized read-only `GET /2/compliance/jobs?type=tweets` request returned HTTP 200 with `DATA_PRESENT=False`, `META_RESULT_COUNT=0` and `ACCESS_RESULT=PASS`, confirming current Development App access to the GET Batch Compliance endpoint; D-043 authorization is exhausted; Batch Compliance remains only a candidate and is not yet approved as the production compliance-synchronization mechanism; D-044 X Batch Compliance Synthetic Lifecycle Verification Authorization FIXED / APPROVED / EXECUTED / EXHAUSTED; the single synthetic `not_a_valid_id` lifecycle reached create HTTP 200, upload HTTP 200, one status GET HTTP 200 with job status `complete`, and download HTTP 200 with one result record; safe parser returned `ERROR_CATEGORY=UNKNOWN_OR_NONE`, so expected `invalid_id` semantic verification FAILED; no retry or additional X API request is authorized; persistent live X collection and X Collector implementation remain unauthorized; D-045 X Batch Compliance D-044 Semantic Reconciliation FIXED / APPROVED with CURRENT-DOCUMENTATION CORRECTION; current official Batch Compliance documentation supports malformed `not_a_valid_id` → `invalid_id`, `rehydrate / tweet_edited`, and separate `scrub_geo / geo_scrubbed` semantics; the earlier D-045 conclusion that the `invalid_id` oracle was unsupported is superseded; D-044 transport verification remains PASS and semantic verification remains FAIL UNDER THE ACTUALLY EXECUTED D-044 PARSER / ORACLE; actual downloaded-record semantics remain UNKNOWN / NOT RECOVERABLE FROM RETAINED EVIDENCE; D-045 correction authorizes no X API request; D-046 remains NOT APPROVED
- Module 8 — Telegram Sources: ACCESS PRECHECK BLOCKED — TELEGRAM CONTENT AI-USE TERMS CONFLICT
- Module 9 — Discord Collector: ACCESS PRECHECK AVAILABLE WITH LIMITATIONS
- Repository initialized
- Mandatory project documentation: COMPLETED / VERIFIED
- SOURCE ACCESS PRECHECK: COMPLETE / VERIFIED under D-033
- D-034 — X API Budget and Paid Access Policy: FIXED / APPROVED — initial personal-funded maximum USD $15; Auto-recharge OFF
- D-035 — Quality / Noise / Dedup Policy: FIXED / APPROVED — MINIMUM NOISE → MAXIMUM ACTIONABLE OPPORTUNITIES
- D-036 — X Bounded Live-Access Envelope: FIXED / APPROVED — maximum USD $1.00 spend; 20 paid requests; 10 Posts per Recent Search request; 200 maximum billable returned Posts / resources
- D-037 — X Minimum Credit Purchase Authorization: FIXED / APPROVED — one-time USD $5.00 prepaid purchase authorized; live-spend remains capped at USD $1.00; unused credits require separate explicit approval
- D-038 — X Development Project Access Authorization: FIXED / APPROVED — only `Connect · Development` to `Default Project — Pay Per Use` is authorized; Staging and Production are not authorized
- D-039 — X Bearer Token Generation and Local Secret Handling: FIXED / APPROVED — executed and verified; the regenerated Bearer Token is stored only as `X_BEARER_TOKEN` in the Git-ignored `.env`; no API request was executed under D-039
- D-040 — X First Bounded Live API Verification Authorization: FIXED / APPROVED / EXECUTED — the single authorized `GET /2/tweets/search/recent` request used `max_results=10` and the approved deterministic query and returned HTTP 200 with `meta.result_count=10` and 10 returned Posts; post-request billing verified Remaining Balance USD $4.95, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.05; no second request is authorized
- D-041 — X Content Compliance and Persistence Policy: FIXED / APPROVED — persistent live X Content remains prohibited until a separately approved X-specific PostgreSQL persistence design implements D-041; compliance removal must not automatically retain Post IDs, hashes, fingerprints, mappings, identifiers or other source-derived derivatives unless separately confirmed permissible by official X terms or authorization
- D-042 — X PostgreSQL Persistence Schema and Compliance Lifecycle: FIXED / APPROVED — `x_source_items` logical design approved with `x_edit_root_id` as edit-chain identity, `x_post_id` as current revision identity, in-place revision updates with re-filtering, and hard compliance DELETE with no tombstone; migration `003_x_source_items.sql`, PostgreSQL changes, X Collector implementation and persistent live X collection remain unauthorized
- D-043 — X Batch Compliance Account Access Verification Authorization: FIXED / APPROVED / EXECUTED — exactly one authorized read-only `GET /2/compliance/jobs?type=tweets` request was executed and returned HTTP 200 with `DATA_PRESENT=False`, `META_RESULT_COUNT=0` and `ACCESS_RESULT=PASS`, confirming current Development App access to the GET Batch Compliance endpoint; D-043 authorization is exhausted; post-request billing remained displayed as Remaining Balance USD $4.95, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.05; no Compliance Job creation, POST request, Post Lookup, rehydration, migration, PostgreSQL change, persistent live X collection or X Collector implementation is authorized
- D-044 — X Batch Compliance Synthetic Lifecycle Verification Authorization: FIXED / APPROVED / EXECUTED / EXHAUSTED — one synthetic `not_a_valid_id` lifecycle attempt was executed; create HTTP 200, upload HTTP 200, one status GET HTTP 200 with job status `complete`, and download HTTP 200 with one result record; safe parser returned `ERROR_CATEGORY=UNKNOWN_OR_NONE`, therefore expected `invalid_id` semantic result was not verified and verification result is FAIL; final Console billing remained Remaining Balance USD $4.95, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.05; observed cent-level Current Spend delta USD $0.00 does not prove zero actual lifecycle cost
- D-045 — X Batch Compliance D-044 Semantic Reconciliation: FIXED / APPROVED with CURRENT-DOCUMENTATION CORRECTION — current official Batch Compliance documentation explicitly supports malformed `not_a_valid_id` → `invalid_id`, `rehydrate / tweet_edited`, and separate `scrub_geo / geo_scrubbed` semantics; the earlier conclusion that the D-044 `invalid_id` oracle was unsupported is superseded without rewriting historical D-045 text; D-044 transport verification remains PASS and semantic verification remains FAIL UNDER THE ACTUALLY EXECUTED D-044 PARSER / ORACLE; the cause of that FAIL is unresolved from retained evidence; no X API request is authorized
- Application code: IN PROGRESS — implemented through verified Module 6; Module 5 remains BLOCKED — DATA ACCESS NOT APPROVED; Module 7 remains SCOPE APPROVED / PRE-IMPLEMENTATION / ACCESS GATED; D-034 through D-045 are FIXED / APPROVED; the authorized USD $5.00 prepaid credit purchase has been completed and credited; D-038 Development Project Access has been executed and verified successfully; D-039 Bearer Token regeneration through the verified `Generate → Regenerate` flow has been executed successfully; the regenerated token is stored only as `X_BEARER_TOKEN` in the Git-ignored `.env`; non-secret verification confirmed `TOKEN_MATCH=True` and the clipboard was cleared; D-040 pre-request billing verification confirmed Remaining Balance USD $5.00, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.00; the single authorized request then completed successfully with HTTP 200, `meta.result_count=10` and 10 returned Posts; post-request billing verification confirmed Remaining Balance USD $4.95, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.05; no second request is authorized and X Collector implementation has not started; D-044 has now been executed and exhausted: transport lifecycle reached download successfully, but expected `invalid_id` semantic result was not verified; D-044 authorization is exhausted and no additional X API request is authorized under it; D-045 CURRENT-DOCUMENTATION CORRECTION records that current official Batch Compliance documentation supports `invalid_id`, `rehydrate / tweet_edited`, and `scrub_geo / geo_scrubbed`; D-046 remains NOT APPROVED and no new X API activity is authorized

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
- `SOURCE_ACCESS_PRECHECK.md` — verified official-access state, evidence, limitations and proceed / do-not-proceed conclusion for every approved V1 source
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

Application code is implemented through the verified Module 6 state. Module 2, Module 3, Module 4 and Module 6 are COMPLETED / PASS. Module 5 remains BLOCKED — DATA ACCESS NOT APPROVED. Module 7 remains PRE-IMPLEMENTATION / ACCESS GATED. D-034 approves official X Pay Per Use use in principle with a maximum initial personal-funded budget of USD $15 and Auto-recharge OFF. D-035 fixes the cross-module objective MINIMUM NOISE → MAXIMUM ACTIONABLE OPPORTUNITIES. D-036 approves the first bounded live-access envelope at maximum USD $1.00 spend, 20 paid requests, 10 Posts per Recent Search request and 200 maximum billable returned Posts / resources. D-037 authorized the minimum one-time prepaid credit purchase of USD $5.00 without increasing the D-036 live-spend limit, and that purchase has been completed and credited. D-038 authorized only Development Project Access to the existing `Default Project — Pay Per Use`; Staging and Production remain unauthorized. The Development connection has now been executed and verified successfully. Before D-040 execution, the required pre-request billing verification confirmed Remaining Balance USD $5.00, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.00. D-039 Bearer Token regeneration through the verified X Console `Generate → Regenerate` flow has been executed successfully. The regenerated Bearer Token is stored only as `X_BEARER_TOKEN` in the Git-ignored `.env`; non-secret verification confirmed `TOKEN_MATCH=True` and the clipboard was cleared. The previous Bearer Token may have been invalidated. D-040 was subsequently executed successfully: the single authorized Recent Search request returned HTTP 200 with `meta.result_count=10` and 10 returned Posts. Post-request billing verification confirmed Remaining Balance USD $4.95, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.05. No second request is authorized and X Collector implementation has not started. D-041 and D-042 are FIXED / APPROVED. D-042 approves the logical `x_source_items` persistence lifecycle but does not authorize migration `003_x_source_items.sql`, PostgreSQL changes, additional X API requests, Batch Compliance jobs, X Collector implementation or persistent live X collection. D-043 is FIXED / APPROVED / EXECUTED. The single authorized read-only `GET /2/compliance/jobs?type=tweets` request returned HTTP 200 with `DATA_PRESENT=False`, `META_RESULT_COUNT=0` and `ACCESS_RESULT=PASS`, confirming current Development App access to the GET Batch Compliance endpoint. D-043 authorization is exhausted and no second request is authorized. Post-request billing verification remained displayed as Remaining Balance USD $4.95, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.05; the exact USD $0.005 request charge was not independently visible at the Console display precision. Batch Compliance remains only a candidate and is not yet approved as the production compliance-synchronization mechanism. D-044 is FIXED / APPROVED / EXECUTED / EXHAUSTED. The single authorized synthetic `not_a_valid_id` lifecycle used exactly one create POST, one signed upload PUT, one status GET and one signed download GET. Create returned HTTP 200 with job status `created`; upload returned HTTP 200; the first status GET returned HTTP 200 with job status `complete`; download returned HTTP 200 with one result record. The safe parser returned `ERROR_CATEGORY=UNKNOWN_OR_NONE`, so the expected `invalid_id` semantic result was not verified and D-044 verification result is FAIL. No retry, second job, second download, additional polling or other X API request was executed. Final Console billing remained displayed as Remaining Balance USD $4.95, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.05. The observed cent-level Current Spend delta was USD $0.00, which does not prove zero actual lifecycle cost or that signed upload/download operations are free. D-044 authorization is exhausted. D-045 — X Batch Compliance D-044 Semantic Reconciliation — is FIXED / APPROVED with a later CURRENT-DOCUMENTATION CORRECTION. Current official Batch Compliance documentation explicitly supports malformed `not_a_valid_id` → `{"error":"invalid_id"}`, `rehydrate / tweet_edited`, and separate `scrub_geo / geo_scrubbed` semantics. The earlier D-045 conclusion that the D-044 `invalid_id` oracle was unsupported is superseded without rewriting historical D-045 text. D-044 transport verification remains PASS and semantic verification remains FAIL UNDER THE ACTUALLY EXECUTED D-044 PARSER / ORACLE because the parser returned `ERROR_CATEGORY=UNKNOWN_OR_NONE`. The reason for that FAIL remains unresolved from retained evidence, and the actual downloaded-record semantics remain UNKNOWN / NOT RECOVERABLE FROM RETAINED EVIDENCE. The primary production blocker is the unresolved 24-hour deadline guarantee because a guaranteed maximum Batch Compliance processing-time SLA has not been established. Backup / WAL / restore compliance and recurring operating cost also remain unresolved. D-046 is NOT APPROVED. No X API request is authorized.

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
