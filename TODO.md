# OPPORTUNITY SCANNER AI — TODO

## CURRENT PRIORITY

Await Reddit's decision or follow-up on the successfully submitted API access request. Do not begin Reddit Collector implementation until officially permitted access is confirmed.

## FOUNDATION

- [x] Verify Python 3.12.10.
- [x] Verify Git 2.55.0.windows.3.
- [x] Verify VS Code 1.132.0.
- [x] Install and verify WSL 2.7.12.
- [x] Install and verify Docker Desktop.
- [x] Verify Docker Engine.
- [x] Verify Docker Compose.
- [x] Pass Docker container execution smoke test.
- [x] Create project root.
- [x] Initialize local Git repository.
- [x] Create and verify PROJECT_STATE.md.
- [x] Create and verify ARCHITECTURE.md.
- [x] Create and verify DECISIONS.md.
- [x] Create and verify ROADMAP.md.
- [x] Create and verify TODO.md.
- [x] Create and verify CHANGELOG.md.
- [x] Create and verify README.md.
- [x] Resolve DATABASE placement contradiction — RESOLVED by D-017.

## MODULE 2 — POSTGRESQL

- [x] Approve Module 2 scope and acceptance criteria — D-018.
- [x] Configure local PostgreSQL 18.6 with Docker Compose.
- [x] Configure persistent PostgreSQL storage.
- [x] Protect local secrets from Git tracking.
- [x] Create and verify dedicated project database.
- [x] Create and verify dedicated non-superuser application role.
- [x] Verify application database connection.
- [x] Verify write and read operations.
- [x] Verify persistence after restart.
- [x] Create baseline migration 001_baseline.sql.
- [x] Verify migration execution and idempotency.
- [x] Verify clean-state database rebuild.
- [x] Verify application role recreation from clean state.
- [x] Verify baseline migration from clean state.
- [x] Document PostgreSQL start, stop, verification and data-safety procedure.
- [x] Protect Linux shell scripts with Git LF line-ending policy.
- [x] Create Module 2 Git milestone commit — d033d94.
- [x] Verify clean Git working tree after milestone commit.
- [x] Mark Module 2 PASS after all D-018 acceptance criteria are verified.
- [x] Create Module 2 documentation closeout commit — ad558f2.
- [x] Verify final clean Git working tree after documentation closeout.


## MODULE 3 — TELEGRAM BOT

- [x] Approve Module 3 scope and acceptance criteria — D-019.
- [x] Review the current official Telegram Bot API requirements relevant to Module 3.
- [x] Approve direct Telegram Bot API HTTPS client approach — D-020.
- [x] Approve getUpdates long polling for local Module 3.
- [x] Require getWebhookInfo before polling.
- [x] Prohibit automatic deleteWebhook when an existing webhook is detected.
- [x] Keep owner_id and target_chat_id as separate configuration parameters.
- [x] Keep Telegram bot token and real Telegram IDs outside tracked Git files.
- [x] Prepare safe local Telegram configuration.
- [x] Verify Telegram bot token is not tracked by Git.
- [x] Verify bot identity through Telegram Bot API.
- [x] Verify webhook state before polling.
- [x] Implement minimal owner-authorized /start interaction.
- [x] Verify unauthorized user IDs are not served.
- [x] Verify bidirectional bot communication.
- [x] Implement and verify test opportunity message formatting.
- [x] Implement and verify the Открыть URL button.
- [x] Document local Telegram bot start and verification procedure.
- [x] Synchronize relevant repository documentation.
- [x] Create Module 3 Git milestone — 3ffe707.
- [x] Verify final clean Git working tree after Module 3 milestone.
- [x] Mark Module 3 PASS after all D-019 acceptance criteria were verified.
## OPEN CROSS-MODULE ISSUE

- [x] Resolve the documented early basic-filter versus Module 6 Filter Engine contradiction — RESOLVED by D-021.

## ROADMAP

- [x] MODULE 2 — PostgreSQL
- [x] MODULE 3 — Telegram Bot
- [x] MODULE 4 — RSS Collector
- [ ] MODULE 5 — Reddit Collector
- [ ] MODULE 6 — Filter Engine
- [ ] MODULE 7 — X Collector
- [ ] MODULE 8 — Telegram Sources
- [ ] MODULE 9 — Discord Collector
- [ ] MODULE 10 — AI Analyzer
- [ ] MODULE 11 — Anti-Scam Engine
- [ ] MODULE 12 — Score Engine
- [ ] MODULE 13 — Personal Learning
- [ ] MODULE 14 — Reliability
- [ ] MODULE 15 — Production 24/7

## DEFERRED DECISIONS

Do not decide these until the relevant module requires them:

- Python libraries and frameworks
- ORM
- migration framework
- scheduler
- AI provider and model
- Telegram framework
- Scoring formulas and thresholds
- Anti-Scam providers and thresholds
- source-specific data retention rules

## CONTROL RULE

Do not add, remove, reorder, or silently complete tasks without verified evidence.
