# OPPORTUNITY SCANNER AI — TODO

## CURRENT PRIORITY

Complete documentation synchronization and Git commit for the executed D-037 USD $5.00 prepaid credit purchase. After Git is clean, perform the next separate controlled Project Access connection-readiness step. Do not connect the App to Pay Per Use, generate credentials, make a paid live API request or begin X Collector implementation automatically.

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

## SOURCE ACCESS PRECHECK

- [x] Reddit — BLOCKED — DATA ACCESS NOT APPROVED.
- [x] X / Twitter — UNKNOWN — REQUIRES APPROVAL — active App remains disconnected from Default Project — Pay Per Use.
- [x] Discord — AVAILABLE WITH LIMITATIONS.
- [x] Telegram — BLOCKED — current AI-use terms conflict with the approved downstream AI stage.
- [x] RSS / Atom — AVAILABLE WITH LIMITATIONS.
- [x] Verify date and evidence for all five approved V1 sources.
- [x] Record collector proceed / do-not-proceed result for all five sources.
- [x] Mark SOURCE ACCESS PRECHECK COMPLETE / VERIFIED under D-033.

## D-034 / D-035 / D-036 / D-037 POLICY MILESTONE

- [x] Approve official X API Pay Per Use use in principle — D-034.
- [x] Fix maximum initial personal-funded X API budget at USD $15.
- [x] Require Auto-recharge OFF.
- [x] Prohibit automatic top-up and automatic budget increase.
- [x] Require separate explicit approval for every later top-up.
- [x] Require paid X collection to stop rather than consume additional personal funds after the approved personal-funded allocation is exhausted.
- [x] Define and approve exact maximum X API request count before paid activation — D-036: 20.
- [x] Define and approve exact maximum billable returned Posts / resources before paid activation — D-036: 200.
- [x] Define and approve deterministic safe-stop conditions before paid activation — D-036.
- [x] Approve cross-module Quality / Noise / Dedup Policy — D-035.
- [x] Fix governing objective: MINIMUM NOISE → MAXIMUM ACTIONABLE OPPORTUNITIES.
- [x] Require stable source identity and deterministic deduplication.
- [x] Require deterministic Filter before AI.
- [x] Prevent repeated production Telegram delivery of the same logical opportunity without a separately specified substantial-change rule.
- [x] Exclude expired / closed opportunities from the normal production Telegram flow.
- [x] Require applicable quality / risk / scoring gates before final production Telegram delivery.
- [x] Approve D-036 bounded live-access envelope: maximum USD $1.00 spend, 20 paid requests, 10 Posts per Recent Search request, 200 maximum billable returned Posts / resources.
- [x] Verify X Developer Console accepts and saves Billing Cycle Cap at USD $1.00.
- [x] Verify X Developer Console minimum prepaid credit purchase is USD $5.00.
- [x] Approve D-037 one-time USD $5.00 prepaid credit purchase without increasing D-036 live-spend authorization above USD $1.00.
- [x] Execute D-037 authorized USD $5.00 prepaid credit purchase.
- [x] Verify credited Remaining Balance USD $5.00.
- [x] Verify Auto Recharge remains OFF after purchase.
- [x] Verify Billing Cycle Cap remains USD $1.00 after purchase.
- [x] Verify Current Spend remains USD $0.00 after purchase.
- [x] Require unused prepaid credit balance to remain unauthorized for further spend without separate explicit approval.

## ROADMAP

- [x] MODULE 2 — PostgreSQL
- [x] MODULE 3 — Telegram Bot
- [x] MODULE 4 — RSS Collector
- [ ] MODULE 5 — Reddit Collector — BLOCKED — DATA ACCESS NOT APPROVED
- [x] MODULE 6 — Filter Engine — COMPLETED / PASS
- [ ] MODULE 7 — X Collector — SCOPE APPROVED / PRE-IMPLEMENTATION / ACCESS GATED — X status: UNKNOWN — REQUIRES APPROVAL; D-036 bounded live-access envelope approved; D-037 USD $5.00 prepaid credit purchase completed; Remaining Balance USD $5.00; Billing Cycle Cap USD $1.00; Auto Recharge OFF; Current Spend USD $0.00
- [ ] MODULE 8 — Telegram Sources — BLOCKED — TELEGRAM CONTENT AI-USE TERMS CONFLICT
- [ ] MODULE 9 — Discord Collector — ACCESS PRECHECK: AVAILABLE WITH LIMITATIONS
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
