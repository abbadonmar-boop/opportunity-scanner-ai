# OPPORTUNITY SCANNER AI — CHANGELOG

All notable verified project changes are recorded here.

## 2026-09-02

### Environment
- Verified Python 3.12.10.
- Verified Git 2.55.0.windows.3.
- Verified VS Code 1.132.0.
- Installed and verified WSL 2.7.12.
- Installed Docker Desktop 4.89.0.
- Verified Docker Engine 29.7.2.
- Verified Docker Compose v5.5.0.
- Passed Docker container execution smoke test with hello-world.

### Repository
- Created project root:
  $HOME\Projects\opportunity-scanner-ai
- Initialized local Git repository.

### Documentation
- Created and verified PROJECT_STATE.md.
- Created and verified ARCHITECTURE.md.
- Created and verified DECISIONS.md.
- Created and verified ROADMAP.md.
- Created and verified TODO.md.

### Project Status
- Module 1 — Development Environment completed with PASS.
- Project implementation code has not started.
- Known architecture/roadmap contradictions remain explicitly unresolved.

### Architecture Decision
- Approved D-017: PostgreSQL is the single cross-cutting persistence layer.
- Primary persistence occurs after collection / normalization as early as necessary for recovery.
- The same record is progressively updated through DEDUPLICATE → FILTER → EXTRACT → AI → RISK → SCORE.
- No separate database or second persistence system is introduced.
- Database-placement conflict resolved.
- Fixed logical pipeline and roadmap remain unchanged.

### Module 2 — PostgreSQL
- Implemented local PostgreSQL 18.6 with Docker Compose.
- Added persistent PostgreSQL named volume and healthcheck.
- Added ignored local .env configuration and safe tracked .env.example.
- Added dedicated non-superuser application role opportunity_scanner_app.
- Verified application password login to opportunity_scanner.
- Verified write and read operations.
- Verified data persistence after container restart.
- Added baseline migration db/migrations/001_baseline.sql.
- Verified baseline migration execution and idempotency.
- Verified full clean-state down -v → rebuild.
- Verified application role recreation after clean-state rebuild.
- Verified baseline migration reproducibility from clean state.
- Verified migration version 1 after clean-state rebuild.
- Documented local PostgreSQL start, stop, health verification and data-safety procedure in README.md.
- Module 2 technical acceptance tests passed; final Git milestone and clean-tree verification remain.
- Added .gitattributes protection to keep Linux shell scripts on LF line endings.
- Module 2 — PostgreSQL acceptance completed with PASS; milestone commit d033d94 created and clean working tree verified.

### Module 3 — Telegram Bot
- Approved and recorded D-019 Module 3 scope and acceptance criteria.
- Approved and recorded D-020 Telegram transport and client approach.
- Added safe Telegram configuration template to .env.example.
- Configured local bot token, owner_id and target_chat_id in ignored .env without exposing values.
- Verified bot identity through Telegram Bot API getMe.
- Verified empty webhook state through getWebhookInfo before long polling.
- Implemented direct Telegram Bot API HTTPS client using Python 3.12 standard library.
- Implemented getUpdates long polling with update offset progression.
- Verified owner-authorized /start interaction with Russian response.
- Verified unauthorized user path stops before sendMessage.
- Verified bidirectional Telegram communication.
- Implemented and verified test opportunity message delivery to target_chat_id.
- Verified approved Module 3 opportunity presentation fields.
- Implemented and verified the Открыть inline URL button.
- Verified the Открыть button opens its target URL.
- Verified existing-webhook safety path stops before getUpdates.
- Added Python runtime artifact exclusions to .gitignore.
- Documented local Telegram bot start, verification, webhook safety and secret handling in README.md.
- Module 3 runtime acceptance checks passed; repository synchronization, Git milestone and final clean-tree verification remain.

- Module 3 — Telegram Bot completed with PASS; milestone commit 3ffe707 created and clean working tree verified.

### Module 4 — RSS Collector Planning
- Approved and recorded D-021 Module 4 basic filtering boundary.
- Conflict 2 resolved: Module 4 uses only the minimal basic filtering slice required for RSS → Database → Filter → Telegram.
- The full Filter Engine remains in Module 6; no duplicate filtering engine or roadmap change was introduced.
- Approved and recorded D-022 RSS feeds from Official Blogs boundary.
- Explicitly configured RSS / Atom feeds from official websites remain RSS / Atom sources.
- No Official Blogs source type, separate collector, scraping or crawling was introduced.
- Approved and recorded D-023 Module 4 RSS Collector scope and acceptance criteria.
- Fixed separate persisted state for basic filter processing and Telegram delivery.
- Defined duplicate-notification acceptance for normal repeated runs after successful persisted delivery; no absolute exactly-once guarantee is claimed for the crash window.
- Required safely bounded initial live-feed verification to prevent uncontrolled historical backlog delivery.

### Module 4 — RSS Collector Implementation
- Added migration db/migrations/002_rss_source_items.sql.
- Added minimal RSS / Atom source-item persistence schema required by D-023.
- Added unique dedup_key for database-level duplicate protection.
- Added separate filter_state and telegram_delivery_state persistence.
- Added telegram_delivered_at for successful delivery tracking.
- Verified migration 002 application as opportunity_scanner_app.
- Verified rss_source_items ownership by opportunity_scanner_app.
- Verified migration 002 schema structure and constraints.
- Verified migration 002 idempotency and single schema_migrations version 2 record.
- Module 4 persistence-step commit: e8235c7 — feat: add module 4 rss persistence schema.
- Added safe RSS_FEED_URLS template to .env.example.
- Added Module 4 RSS allowlist configuration loader.
- Verified rss_collector.py Python syntax.
- Verified fail-safe behavior when RSS_FEED_URLS is missing.
- Verified parsing of a synthetic comma-separated RSS / Atom allowlist without network access.
- Removed synthetic RSS test URLs from local .env after verification.
- Module 4 collector-config commit: 2cdc9cf — feat: add module 4 rss collector config foundation.
- Added deterministic RSS 2.0 and Atom parsing and normalization.
- Added normalized feed-item representation for the minimum D-023 fields.
- Verified RSS 2.0 parsing with a deterministic local case.
- Verified Atom parsing with namespace handling using a deterministic local case.
- Verified RSS and Atom publication timestamps normalize to UTC.
- Added standard-library HTTP feed retrieval with explicit timeout and User-Agent.
- Verified retrieval success, network-error handling, empty-response rejection, invalid-XML rejection, and retrieval-to-normalization integration without live network access.
- No PostgreSQL writes or Telegram delivery were introduced in this step.
- Module 4 retrieval/normalization commit: 17b0696 — feat: add module 4 rss retrieval and normalization.
- Added deterministic feed-item dedup_key generation using SHA-256.
- Verified source_item_id → link → stable content fallback priority.
- Verified collected_at does not affect dedup identity.
- Verified identical item IDs from different feeds remain isolated by feed_url.
- Verified missing stable identity is rejected fail-safe.
- Verified naive published_at handling is deterministic and UTC-based.
- Module 4 dedup-key commit: d80a730 — feat: add module 4 deterministic rss dedup keys.
- Approved D-024: Psycopg 3 for direct synchronous PostgreSQL access and requirements.txt for Python dependency tracking; no ORM or SQLAlchemy introduced.
- D-024 decision commit: c967551 — docs: approve psycopg 3 postgres access.
- Added psycopg[binary]==3.3.5 dependency and .venv Git exclusion.
- Dependency-foundation commit: a12fc75 — chore: add psycopg dependency foundation.
- Created and verified project .venv with Python 3.12.10.
- Installed and import-verified Psycopg 3.3.5 inside the project .venv.
- Verified .venv remains excluded from Git and installation leaves the tracked working tree clean.
- Verified real Psycopg connection to PostgreSQL as opportunity_scanner_app without exposing the password.
- Added and verified Module 4 database configuration loader for POSTGRES_DB, APP_DB_USER and APP_DB_PASSWORD.
- PostgreSQL-config commit: cf38bd9 — feat: add module 4 postgres config loader.
- Added PostgreSQL persistence for normalized RSS / Atom source items.
- Verified controlled INSERT through persist_feed_item() using opportunity_scanner_app.
- Verified filter_state and telegram_delivery_state remain PENDING after initial persistence.
- Verified repeated persistence of the same source item returns the existing id and creates no duplicate database row.
- Verified database-level row count remains one after repeated persistence.
- Removed the synthetic persistence test row and verified cleanup.
- Module 4 normalized-item persistence commit: 4a058c7 — feat: persist normalized rss items in postgres.
- Approved D-025: minimum deterministic Module 4 basic-filter rules with casefold(), stop-word priority and explicit PASS / REJECT behavior.
- D-025 decision commit: 731411f — docs: define module 4 basic filter rules.
- Approved D-026: controlled MAIN DEVELOPMENT session handoff workflow using SESSION_HANDOFF.md.
- Added SESSION_HANDOFF.md continuity template and README handoff guidance without changing architecture, roadmap, scope or current Module 4 decisions.
- Session-handoff workflow commit: 5b57749 — docs: add main development session handoff workflow.
- Added deterministic Module 4 basic-filter evaluation for normalized RSS / Atom title and content_text.
- Verified positive-keyword PASS, Unicode casefold matching, stop-word-priority REJECT, no-signal REJECT, conditional-context-only REJECT and empty-text REJECT cases.
- Added PostgreSQL persistence of PASS / REJECT results to the existing rss_source_items.filter_state.
- Verified PASS and REJECT persistence with real PostgreSQL integration tests while telegram_delivery_state remained PENDING.
- Removed both synthetic filter-verification database rows and verified zero test rows remained.
- Module 4 basic-filter implementation commit: 374d5c1 — feat: add module 4 basic rss filtering.
- Added preliminary RSS candidate Telegram formatting using only known title, source_name and link fields.
- Added Открыть inline URL button for RSS candidates with a source link.
- Verified RSS Telegram formatter and sender deterministically with zero real Telegram API calls.
- Added persisted Telegram delivery transition for PASS + PENDING → DELIVERED.
- Verified REJECT items cannot be marked delivered.
- Verified repeated delivered-state persistence is idempotent and preserves telegram_delivered_at.
- Added PASS-only RSS delivery orchestration: successful sender call precedes DELIVERED persistence.
- Verified already DELIVERED items are not resent during a normal later orchestration call.
- Verified sender failure leaves the RSS item in PASS + PENDING.
- Verified delivery-state and orchestration behavior against real PostgreSQL with synthetic rows.
- Removed all synthetic delivery verification rows and verified zero test rows remained.
- Real RSS-candidate Telegram delivery was intentionally not performed in this implementation step.
- Module 4 RSS Telegram delivery implementation commit: 6bbd5c3 — feat: add module 4 rss telegram delivery.
- Module 4 Telegram-delivery documentation sync commit: 8e1a0af — docs: sync module 4 telegram delivery step.
- Performed one controlled real Telegram delivery of a synthetic persisted PASS RSS candidate.
- Verified empty webhook state immediately before the real Telegram delivery.
- Verified successful PASS + PENDING → DELIVERED transition after real sendMessage.
- Verified telegram_delivered_at persistence.
- Visually verified the preliminary RSS opportunity message in the configured Telegram target.
- Verified the Открыть inline button opens the configured source URL.
- Live RSS feed retrieval was not performed during the real Telegram verification.
- Removed the synthetic real-delivery database row and verified zero matching test rows remained.
- D-027 — Module 4 Initial Live Feed Safety — FIXED / APPROVED.
- Initial live verification is bounded to exactly one configured RSS / Atom feed URL and at most one parser item entering persistence and downstream processing.
- D-027 uses deterministic first-item parser order and prevents creation of an uncontrolled historical PostgreSQL / Telegram backlog during the initial live verification.
- D-027 introduces no scheduler, queue, ORM, migration framework or additional infrastructure.
- D-027 decision commit: 2310058 — docs: define initial live rss safety.
- Live RSS feed retrieval has still not been performed.
- Implemented D-027 bounded initial live-feed verification mode in rss_collector.py.
- Bounded processing permits only the first parser item to enter persistence and downstream processing.
- Added allowlist enforcement before live feed retrieval.
- Deterministic bounded processor test passed with three parsed items and only item-1 persisted/downstream.
- Allowlist wrapper test passed: blocked URL caused zero fetch/process calls; allowed URL caused one fetch and one processor call.
- Real PostgreSQL D-027 integration test passed for PASS, normal repeated-run deduplication, REJECT and empty-feed behavior.
- Invalid-feed verification passed with zero false PostgreSQL rows.
- Synthetic D-027 PostgreSQL test rows were removed and zero matching rows remained.
- All pre-live D-027 implementation tests used REAL_TELEGRAM_CALLS=0 and LIVE_RSS_RETRIEVAL=0.
- D-027 implementation commit: 826b051 — feat: add bounded live rss verification mode.
- Live RSS feed retrieval has still not been performed.
- Configured exactly one allowlisted RSS feed for the first D-027 live verification: https://openai.com/news/rss.xml.
- Verified load_rss_feed_urls() returns exactly that one configured feed before network retrieval.
- Performed the first controlled live RSS retrieval under D-027.
- The real feed parsed 1192 items while only the deterministic first parser item entered persistence and downstream processing.
- Verified ROW_COUNT_DELTA=1 and D027_BOUND_CHECK=PASS.
- The selected real item evaluated to REJECT, so Telegram delivery correctly did not occur.
- The real item persisted as REJECT + PENDING with no telegram_delivered_at timestamp.
- FIRST_CONTROLLED_LIVE_RSS_TEST=PASS.
- Git working tree remained clean after the live RSS run.
- Completed focused Module 4 acceptance review against D-023.
- Confirmed the remaining local run / verification documentation gap was closed in README.md.
- Module 4 local verification procedure commit: ff04bff — docs: add module 4 local verification procedure.
- All Module 4 D-023 acceptance criteria are now verified with recorded evidence.
- Module 4 — RSS Collector: COMPLETED / PASS.
- Next controlled project step is transition to Module 5 — Reddit Collector scope and acceptance criteria.
- D-028 — Module 5 Reddit Collector Scope and Access Gate — FIXED / APPROVED.
- Module 5 requires an officially permitted Reddit developer access path before collector implementation.
- Scraping fallbacks, unofficial mirrors and access-restriction bypasses are prohibited.
- Module 5 scope is limited to COLLECT → NORMALIZE → early PostgreSQL persistence → DEDUPLICATE.
- Reddit-specific retention/deletion compliance is required before real Reddit User Content is retained beyond controlled verification.
- Added a future compliance gate requiring separate approval before Reddit User Content may later be sent to an AI provider.
- The future AI compliance gate does not expand Module 5 and does not block the current access / collector stage.
- D-028 decision commit: d341146 — docs: define module 5 reddit access gate.
- Reddit Collector implementation has not started.

- Sanitized the local Windows user path from tracked CHANGELOG.md before public publication; main repository commit: 495e938 — docs: sanitize local path in changelog.
- Created an independent public snapshot without the original local Git history or real .env file.
- Published the sanitized snapshot to the public GitHub repository for the Reddit API access request; public snapshot root commit: 028aa72 — Initial public snapshot.
- Submitted the official Reddit API access request for Opportunity Scanner AI on 2026-09-12.
- Reddit Support confirmed successful receipt of the API access request.
- Reddit approval has not yet been granted.
- Module 5 — Reddit Collector implementation remains not started and is awaiting the external Reddit access decision.

- Reddit Data Team denied the Opportunity Scanner AI Data Access request in its response dated 2026-09-12.
- Module 5 — Reddit Collector entered BLOCKED — DATA ACCESS NOT APPROVED.
- Reddit Collector implementation remains not started.
- The Reddit denial must not be bypassed through scraping, unofficial mirrors, alternate accounts, credential workarounds or other unapproved access paths.
- Reddit remains an approved V1 source; the SOURCE layer and approved architecture remain unchanged.
- D-029 — Reddit Access Denial Handling and Roadmap Continuation — FIXED / APPROVED.
- D-029 permits controlled project execution to continue to Module 6 — Filter Engine while Module 5 remains blocked and incomplete.
- A future official Reddit application or appeal remains possible only through an officially permitted path with a more complete compliant use case.

- Controlled roadmap execution transitioned to Module 6 — Filter Engine while Module 5 — Reddit Collector remains BLOCKED — DATA ACCESS NOT APPROVED under D-029.
- D-030 — Module 6 Filter Engine Scope and Acceptance Criteria — FIXED / APPROVED.
- Module 6 extends the existing Module 4 FILTER implementation into one reusable deterministic rule-based Filter Engine rather than introducing a second filtering system.
- Module 6 must support the approved EN / RU / UA / DE source languages.
- Existing PASS / REJECT persistence compatibility and verified RSS Telegram delivery semantics must be preserved.
- Module 6 does not implement AI, Anti-Scam, Risk, Score, source collection or Telegram delivery redesign.
- Exact multilingual positive-keyword rules, stop-word rules and the hard-REJECT versus downstream risk / scoring boundary remain pending a separate explicit project decision before implementation.
- Module 6 implementation has not started.
