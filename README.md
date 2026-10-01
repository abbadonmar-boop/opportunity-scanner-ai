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
- Module 7 — X Collector: SCOPE APPROVED / PRE-IMPLEMENTATION / ACCESS GATED — X status: AVAILABLE WITH LIMITATIONS under the D-046 D-033 reconciliation; approved official X access path verified; D-041 through D-049 are FIXED / APPROVED; D-048 records Batch Compliance `PRODUCTION SUITABILITY: NOT PROVEN` because current reviewed authoritative evidence does not establish a guaranteed worst-case lifecycle bound sufficient to prove the applicable 24-hour requirement will always be met; this does not prove Batch Compliance exceeds 24 hours; Compliance event streams remain a separate Enterprise mechanism requiring separate approval; persistent production X collection remains COMPLIANCE-GATED / NOT AUTHORIZED; D-049 does not complete, remove, reorder or waive Module 7 and authorizes no additional X API request, Enterprise activation, migration `003_x_source_items.sql`, PostgreSQL change or X Collector implementation.
- Module 8 — Telegram Sources: ACCESS PRECHECK BLOCKED — TELEGRAM CONTENT AI-USE TERMS CONFLICT
- Module 9 — Discord Collector: SCOPE APPROVED / IMPLEMENTATION IN PROGRESS — D-050, D-051, D-052, D-053 and D-054 are FIXED / APPROVED; Discord retains D-033 status `AVAILABLE WITH LIMITATIONS`; the first code-only / synthetic foundation remains verified in commit `35ee017`; the Discord PostgreSQL persistence schema remains implemented and verified in migration `003_discord_source_items.sql` and commit `3fe7b02`; Discord message lifecycle persistence remains implemented and verified in commit `edb758a`; Discord MESSAGE_CREATE persistence and integration with the existing Module 6 Filter Engine are implemented and verified in commit `3c4a444`; CREATE starts at `filter_state=PENDING`; identical duplicate CREATE is idempotent; conflicting duplicate CREATE fails safely without silent overwrite; PENDING CREATE and updated rows use the existing Module 6 `evaluate_filter()` path and persist `PASS / REJECT`; current Discord-focused verification passes 74 / 74 tests and the full project regression suite passes 97 / 97 tests; real local PostgreSQL synthetic CREATE / duplicate / conflict / UPDATE-refilter verification passed with stable identity preserved and final synthetic `discord_source_items` row count zero; host TCP SCRAM authentication for `opportunity_scanner_app` remains verified after the earlier credential-drift remediation; the D-050 criterion `integration with the existing Module 6 Filter Engine verified` now has evidence; D-052 — Module 9 Discord Rate-Limit and Error-Handling Contract — is FIXED / APPROVED in commit `87f019b`; D-052 code-only / synthetic rate-limit and error-handling implementation is verified in commit `030d59a`; the D-050 criterion `rate-limit / error handling verified` now has implementation and verification evidence; Module 9 is not PASS; D-053 bounded live Discord verification authorization is FIXED / APPROVED in commit `0e25824`; D-053 live Gateway execution has not started; D-054 selects `websockets==17.1` for D-053 bounded verification and the current controlled Gateway foundation in commit `7d15047`; dependency installation is verified in `requirements.txt` and the project `.venv` with imported version `17.1`; D-054 code-only / local-loopback verification is COMPLETED / PASS with 9 / 9 focused tests and 84 / 84 full regression tests using `127.0.0.1` only; D-053 live Gateway execution remains NOT STARTED; real Discord persistence and production activation remain NOT AUTHORIZED; live Discord actions, test-bot token use and test-guild installation are permitted only within the exact D-053 bounded verification envelope after its required pre-execution checks, and activity outside that envelope remains NOT AUTHORIZED. D-053 pre-execution preparation is COMPLETED / PASS on 2026-09-30: `MESSAGE_CONTENT` verified ON; `GUILD_MEMBERS` and `GUILD_PRESENCES` remain OFF; `Administrator` is not granted; one controlled test bot, private test guild and allowlisted test channel are configured; unrelated text and voice channels deny `View Channel` to the bot; exactly one authorized read-only `GET /api/v10/gateway/bot` precheck returned HTTP 200 with `session_start_limit.total=1000`, `remaining=1000` and `max_concurrency=1`; local token / guild / channel configuration was verified without printing the token; the D-053 in-memory verifier is implemented in commit `275bdb5`; focused verifier tests 5 / 5 PASS; the bounded D-053 live-verification runner is implemented and locally verified in commit `6da9a56`; final pre-live documentation re-verification identified the required initial Gateway heartbeat jitter, corrected and verified in commit `f42f8b2`; the D-054 transport retains controlled READY and lifecycle hooks; Gateway transport focused verification is 12 / 12 PASS; exact least-privilege Gateway intents remain `GUILD_MESSAGES | MESSAGE_CONTENT` (`33280`); current Discord-focused verification 74 / 74 PASS; current full project regression 97 / 97 PASS; Gateway connections 0; `IDENTIFY` 0; Gateway session starts 0; D-053 live Gateway execution remains NOT STARTED.
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
- D-047 — X 24-Hour Production Compliance Suitability Evidence Gate: FIXED / APPROVED — Batch Compliance is not production-approved without authoritative evidence of a sufficient worst-case bound; isolated fast executions, averages and best-case observations are insufficient evidence; Compliance event streams remain a separate Enterprise mechanism and are not automatically added to V1; persistent production X collection remains `COMPLIANCE-GATED / NOT AUTHORIZED`; D-047 authorizes no Enterprise activation, X API request, database change or X Collector implementation.
- D-048 — X 24-Hour Authoritative Evidence Review Result: FIXED / APPROVED — applicable 24-hour requirement and asynchronous Batch Compliance lifecycle confirmed by the completed D-047 authoritative review; current reviewed official Batch Compliance evidence does not establish a guaranteed worst-case bound sufficient to prove the requirement will always be met; result is `PRODUCTION SUITABILITY: NOT PROVEN`, not proven unsuitable; Compliance event streams remain a separate Enterprise mechanism requiring separate approval; persistent production X collection remains `COMPLIANCE-GATED / NOT AUTHORIZED`; D-048 authorizes no Enterprise activation, X API request, database change or X Collector implementation.
- D-049 — Controlled Roadmap Continuation Beyond Gated / Blocked Source Modules: FIXED / APPROVED — controlled roadmap continuation to Module 9 — Discord Collector is approved while Modules 7 and 8 retain their existing gated / blocked states; D-049 does not complete, remove, reorder or waive either module and does not change Architecture v1.0, the fixed ROADMAP, module order or V1 source list; Discord Collector implementation is not authorized until a separate Module 9 scope / official-access boundary / acceptance-criteria decision is explicitly approved.
- D-050 — Module 9 Discord Collector Scope, Official-Access Boundary and Acceptance Criteria: FIXED / APPROVED — Module 9 is limited to the official Discord access path and source-side pipeline `Discord → COLLECT → NORMALIZE → early PostgreSQL persistence → DEDUPLICATE → existing Module 6 Filter Engine`; scraping, self-bots, user-token automation, permission / intent bypass and global Discord search are prohibited; least privilege and guild / channel allowlisting are mandatory; `MESSAGE_CONTENT` availability must be re-verified against the then-current Discord requirements; Discord message content must not be used for AI / ML / LLM training without explicit Discord permission; code-only / synthetic implementation foundation is authorized after documentation synchronization, while real credentials, guild installation, live Gateway / API calls, Discord PostgreSQL schema changes and persistence of real Discord message content require separate controlled authorization.
- D-051 — Discord Message Lifecycle and PostgreSQL Persistence Contract: FIXED / APPROVED — one current row per Discord message; stable identity across edits; MESSAGE_UPDATE updates in place and resets filtering to PENDING; MESSAGE_DELETE and MESSAGE_DELETE_BULK use hard deletion with no retained tombstone or source-specific derived identity; incomplete unknown MESSAGE_UPDATE payloads fail safely without fabricated values, REST lookup or history crawling; production persistence requires separately verified encryption-at-rest for PostgreSQL and applicable backup / WAL / recovery paths, an up-to-date privacy policy plus accessible user modification / deletion request mechanism, and verified required `MESSAGE_CONTENT` access; D-051 does not authorize live Discord calls, token actions, real guild installation, real Discord persistence or production activation.
- D-052 — Module 9 Discord Rate-Limit and Error-Handling Contract: FIXED / APPROVED — Discord HTTP per-route limits must not be hardcoded; HTTP `429` may be retried only when a valid Discord-provided retry delay exists and never before that delay expires; `429` without a valid retry delay fails safely; `401` and `403` are non-retryable automatic collector failures; automatic retry for `5xx` and transport / network failures is not introduced during the current code-only / synthetic stage; Gateway outbound limits must be respected automatically and re-verified against then-current official Discord documentation before the first authorized live Gateway connection; D-052 remains transport-agnostic, adds no dependency and authorizes no live Discord activity.
- D-053 — Module 9 Bounded Live Discord Verification Authorization: FIXED / APPROVED - one strictly bounded live verification is authorized using one test bot, one private test guild, one allowlisted test channel and synthetic test messages; at most one Gateway connection attempt, one `IDENTIFY` and one session start are permitted; automatic reconnect, `RESUME`, re-identify and a second connection are prohibited; disconnect / close before completion is `STOP / FAIL`; real Discord persistence, Telegram delivery, AI / LLM processing and production activation remain unauthorized; live Gateway execution has not started.
- D-054 — D-053 Gateway Transport Selection and Pre-Live Technical Verification: FIXED / APPROVED in commit `7d15047` — `websockets==17.1` is selected for D-053 bounded verification and the current controlled Gateway foundation, but is not an irreversible production transport choice; one direct controlled `connect()` path is required; automatic reconnect, `RESUME`, second `connect()` and repeated `IDENTIFY` are prohibited; opcode `1` heartbeat requests may be serviced normally; missing Heartbeat ACK, opcode `7`, opcode `9` or unexpected disconnect require controlled close plus `STOP / FAIL`; code-only / local-loopback verification is mandatory before live Discord execution.
- Application code: IN PROGRESS — Modules 2, 3, 4 and 6 remain COMPLETED / PASS; Module 5 remains BLOCKED — DATA ACCESS NOT APPROVED; Module 7 remains SCOPE APPROVED / PRE-IMPLEMENTATION / ACCESS GATED and is not PASS; Module 8 remains BLOCKED and is not PASS; D-034 through D-054 are FIXED / APPROVED; formal X / Twitter source status remains AVAILABLE WITH LIMITATIONS; Batch Compliance production suitability remains `NOT PROVEN`, not proven unsuitable; persistent production X collection remains COMPLIANCE-GATED / NOT AUTHORIZED; Compliance event streams remain a separate Enterprise mechanism requiring separate approval; backup / WAL / restore compliance and recurring operating cost remain unresolved; Module 9 remains SCOPE APPROVED / IMPLEMENTATION IN PROGRESS and is not PASS; its first synthetic foundation is verified in commit `35ee017`; Discord migration `003_discord_source_items.sql` is implemented and verified in commit `3fe7b02`; Discord message lifecycle persistence is implemented and verified in commit `edb758a`; Discord MESSAGE_CREATE persistence and Module 6 Filter Engine integration are implemented and verified in commit `3c4a444`; current Discord-focused verification passes 74 / 74 and full regression passes 97 / 97; real local PostgreSQL synthetic CREATE / duplicate / conflict / UPDATE-refilter verification passed with stable identity preserved and final synthetic row count zero; the D-050 Module 6 integration criterion now has evidence; D-052 is FIXED / APPROVED in commit `87f019b`; D-052 code-only / synthetic rate-limit and error-handling implementation is verified in commit `030d59a`; the D-050 criterion `rate-limit / error handling verified` now has implementation and verification evidence; D-053 bounded live Discord verification authorization is FIXED / APPROVED in commit `0e25824`; D-053 live Gateway execution has not started; D-054 transport selection is complete; dependency installation is verified (`requirements.txt`, project `.venv`, imported version `17.1`); D-054 code-only / local-loopback verification is COMPLETED / PASS with 9 / 9 focused tests and 84 / 84 full regression tests using `127.0.0.1` only; D-053 live Gateway execution remains NOT STARTED; real Discord persistence and production activation remain NOT AUTHORIZED; live Discord actions, test-bot token use and test-guild installation are permitted only within the exact D-053 bounded verification envelope after its required pre-execution checks, and activity outside that envelope remains NOT AUTHORIZED; no new X API activity, Enterprise activation, migration `003_x_source_items.sql`, PostgreSQL change or X Collector implementation is authorized. D-053 pre-execution preparation is COMPLETED / PASS on 2026-09-30: `MESSAGE_CONTENT` verified ON; `GUILD_MEMBERS` and `GUILD_PRESENCES` remain OFF; `Administrator` is not granted; one controlled test bot, private test guild and allowlisted test channel are configured; unrelated text and voice channels deny `View Channel` to the bot; exactly one authorized read-only `GET /api/v10/gateway/bot` precheck returned HTTP 200 with `session_start_limit.total=1000`, `remaining=1000` and `max_concurrency=1`; local token / guild / channel configuration was verified without printing the token; the D-053 in-memory verifier is implemented in commit `275bdb5`; focused verifier tests 5 / 5 PASS; the bounded D-053 live-verification runner is implemented and locally verified in commit `6da9a56`; final pre-live documentation re-verification identified the required initial Gateway heartbeat jitter, corrected and verified in commit `f42f8b2`; the D-054 transport retains controlled READY and lifecycle hooks; Gateway transport focused verification is 12 / 12 PASS; exact least-privilege Gateway intents remain `GUILD_MESSAGES | MESSAGE_CONTENT` (`33280`); current Discord-focused verification 74 / 74 PASS; current full project regression 97 / 97 PASS; Gateway connections 0; `IDENTIFY` 0; Gateway session starts 0; D-053 live Gateway execution remains NOT STARTED.

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

Application code includes completed / verified Modules 2, 3, 4 and 6 plus the verified Module 9 Discord Collector synthetic foundation, PostgreSQL persistence-schema milestone, message lifecycle persistence milestone and MESSAGE_CREATE / Module 6 Filter Engine integration milestone. Module 5 remains BLOCKED — DATA ACCESS NOT APPROVED. Module 7 remains SCOPE APPROVED / PRE-IMPLEMENTATION / ACCESS GATED and is not PASS. D-034 through D-054 are FIXED / APPROVED. Formal X / Twitter source status remains AVAILABLE WITH LIMITATIONS. D-048 records Batch Compliance `PRODUCTION SUITABILITY: NOT PROVEN`: current reviewed authoritative evidence does not establish a guaranteed worst-case lifecycle bound sufficient to prove the applicable 24-hour requirement will always be met, but does not prove that Batch Compliance exceeds 24 hours. Compliance event streams remain a separate Enterprise-access mechanism requiring separate approval. Persistent production X collection remains COMPLIANCE-GATED / NOT AUTHORIZED. Backup / WAL / restore compliance and recurring production operating cost remain unresolved. Module 8 — Telegram Sources remains BLOCKED and is not PASS. D-049 permits controlled roadmap continuation to Module 9 without completing, removing, reordering or waiving Modules 7 or 8. D-050, D-051, D-052, D-053 and D-054 are FIXED / APPROVED. Module 9 has verified D-033 status AVAILABLE WITH LIMITATIONS and remains SCOPE APPROVED / IMPLEMENTATION IN PROGRESS, but is not PASS. The first code-only / synthetic foundation is verified in commit `35ee017`. Migration `003_discord_source_items.sql` is implemented and verified in commit `3fe7b02`, including application-role execution, ownership, schema / constraints, idempotency, controlled synthetic INSERT and cleanup with final row count zero. Discord message lifecycle persistence is implemented and verified in commit `edb758a`. Discord MESSAGE_CREATE persistence and integration with the existing Module 6 Filter Engine are implemented and verified in commit `3c4a444`: CREATE starts at `filter_state=PENDING`; identical duplicate CREATE is idempotent; conflicting duplicate CREATE fails safely without silent overwrite; PENDING CREATE and updated rows use the existing Module 6 `evaluate_filter()` implementation and persist `PASS / REJECT`. Current Discord-focused verification passes 74 / 74 tests and the full project regression suite passes 97 / 97 tests using the project `.venv`. Real local PostgreSQL synthetic verification passed for CREATE filtering, identical duplicate idempotency, conflicting duplicate protection and UPDATE re-filtering, with stable identity preserved and final synthetic row count zero. Host TCP SCRAM authentication for `opportunity_scanner_app` remains verified after the earlier credential-drift remediation. The D-050 acceptance criterion `integration with the existing Module 6 Filter Engine verified` now has implementation and verification evidence. D-052 — Module 9 Discord Rate-Limit and Error-Handling Contract — is FIXED / APPROVED in commit `87f019b`; it defines transport-agnostic synthetic handling boundaries for HTTP `429`, `401 / 403`, `5xx` / transport failures and Gateway outbound rate limits without selecting a Discord client library or authorizing live activity. D-052 code-only / synthetic rate-limit and error-handling implementation is verified in commit `030d59a`. The D-050 criterion `rate-limit / error handling verified` now has implementation and verification evidence. D-051 production gates for encryption-at-rest, privacy / deletion requests and required `MESSAGE_CONTENT` access remain in force. D-053 bounded live Discord verification authorization is FIXED / APPROVED in commit `0e25824`, but D-053 live Gateway execution has not started. D-054 selects `websockets==17.1` for D-053 bounded verification and the current controlled Gateway foundation in commit `7d15047`. Dependency installation is verified in `requirements.txt` and the project `.venv` with imported version `17.1`. D-054 code-only / local-loopback verification is COMPLETED / PASS: 9 / 9 focused Gateway transport tests and 84 / 84 full project regression tests passed using `127.0.0.1` local loopback only. D-053 live Gateway execution remains NOT STARTED. Successful D-053 execution will still require a separate final D-050 acceptance review before Module 9 PASS. Real Discord persistence and production activation remain NOT AUTHORIZED. Live Discord actions, test-bot token use and test-guild installation are permitted only within the exact D-053 bounded verification envelope after its required pre-execution checks; activity outside that envelope remains NOT AUTHORIZED. D-053 pre-execution preparation is COMPLETED / PASS on 2026-09-30: `MESSAGE_CONTENT` verified ON; `GUILD_MEMBERS` and `GUILD_PRESENCES` remain OFF; `Administrator` is not granted; one controlled test bot, private test guild and allowlisted test channel are configured; unrelated text and voice channels deny `View Channel` to the bot; exactly one authorized read-only `GET /api/v10/gateway/bot` precheck returned HTTP 200 with `session_start_limit.total=1000`, `remaining=1000` and `max_concurrency=1`; local token / guild / channel configuration was verified without printing the token; the D-053 in-memory verifier is implemented in commit `275bdb5`; focused verifier tests 5 / 5 PASS; the bounded D-053 live-verification runner is implemented and locally verified in commit `6da9a56`; final pre-live documentation re-verification identified the required initial Gateway heartbeat jitter, corrected and verified in commit `f42f8b2`; the D-054 transport retains controlled READY and lifecycle hooks; Gateway transport focused verification is 12 / 12 PASS; exact least-privilege Gateway intents remain `GUILD_MESSAGES | MESSAGE_CONTENT` (`33280`); current Discord-focused verification 74 / 74 PASS; current full project regression 97 / 97 PASS; Gateway connections 0; `IDENTIFY` 0; Gateway session starts 0; D-053 live Gateway execution remains NOT STARTED.

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
