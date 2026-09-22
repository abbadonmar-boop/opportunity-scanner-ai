# OPPORTUNITY SCANNER AI — PROJECT STATE

## CURRENT PHASE
Foundation

## CURRENT MODULE
Module 7 — X Collector — SCOPE APPROVED / PRE-IMPLEMENTATION / ACCESS GATED

## CURRENT STEP
SOURCE ACCESS PRECHECK remains COMPLETE / VERIFIED under D-033. D-034 through D-038 are FIXED / APPROVED. D-038 — X Development Project Access Authorization — authorizes only connecting the existing X App to the existing `Default Project — Pay Per Use` in the `Development` environment for controlled bounded live-verification readiness. `Staging` and `Production` are not authorized. Billing safety remains verified at Remaining Balance USD $5.00, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.00. Module 7 remains SCOPE APPROVED / PRE-IMPLEMENTATION / ACCESS GATED. The App is still disconnected from Pay Per Use, no paid live API request has been made, and collector implementation has not started.

## COMPLETED
- Product requirements and Architecture v1.0 are fixed.
- Module 1 — Development Environment completed with PASS.
- Module 2 — PostgreSQL completed with PASS.
- D-017 approved and verified: PostgreSQL is the single cross-cutting persistence layer.
- D-018 approved and verified: Module 2 scope and acceptance criteria are fixed.
- Module 2 implementation milestone: d033d94.
- Module 2 documentation closeout: ad558f2.
- D-019 approved and verified: Module 3 Telegram Bot scope and acceptance criteria are fixed.
- D-020 approved and verified: direct Telegram Bot API HTTPS access, getUpdates long polling, mandatory getWebhookInfo safety checking, no automatic deleteWebhook, and separate owner_id / target_chat_id configuration.
- Safe tracked Telegram configuration template added to .env.example.
- Local Telegram bot token, owner_id and target_chat_id configured in ignored .env without exposing values.
- Telegram bot identity verified through getMe.
- Empty webhook state verified through getWebhookInfo before long polling.
- Telegram Bot implemented with Python 3.12 standard library and direct HTTPS access.
- Local bot process verified with getUpdates long polling.
- Owner-authorized /start command verified with Russian response.
- Unauthorized user path verified to stop before sendMessage.
- Bidirectional Telegram communication verified.
- Test opportunity message verified in target_chat_id.
- Approved Module 3 opportunity presentation fields verified.
- Открыть inline URL button verified and confirmed to open its target URL.
- Existing-webhook safety path verified to stop before getUpdates.
- Local Telegram bot start, verification, webhook-safety and secret-safety procedure documented.
- Python runtime artifacts excluded from Git tracking.
- Module 3 implementation milestone: 3ffe707 — feat: establish module 3 telegram bot foundation.
- Clean Git working tree verified immediately after Module 3 milestone.
- Module 3 — Telegram Bot completed with PASS.
- D-021 approved and verified: Module 4 basic filtering is the minimum first implementation of the existing FILTER component; the full Filter Engine remains in Module 6.
- D-022 approved and verified: explicitly configured RSS / Atom feeds from official websites remain RSS / Atom sources; no Official Blogs source type or collector is introduced.
- D-023 approved and verified: Module 4 RSS Collector scope and acceptance criteria are fixed, including separate filter/delivery state, bounded initial live-feed behavior, and no absolute exactly-once Telegram guarantee.
- Module 4 persistence step completed: migration 002_rss_source_items.sql implemented and verified.
- Migration 002 creates rss_source_items with unique dedup_key and separate filter_state / telegram_delivery_state.
- Migration 002 application, ownership, schema structure and idempotency verified.
- Module 4 persistence-step commit: e8235c7 — feat: add module 4 rss persistence schema.
- Module 4 RSS allowlist configuration foundation implemented and verified.
- RSS_FEED_URLS safe tracked template added to .env.example.
- RSS config loader syntax, missing-config fail-safe and synthetic allowlist parsing verified.
- Synthetic RSS test URLs removed from local .env after verification.
- Module 4 collector-config commit: 2cdc9cf — feat: add module 4 rss collector config foundation.
- Module 4 deterministic RSS / Atom retrieval and normalization foundation implemented and verified.
- RSS 2.0 and Atom parsing verified with deterministic local cases, including Atom namespace handling and UTC publication timestamps.
- HTTP retrieval success, network-error, empty-response, invalid-XML, and retrieval-to-normalization paths verified without live network access.
- No PostgreSQL writes or Telegram delivery were introduced in this step.
- Module 4 retrieval/normalization commit: 17b0696 — feat: add module 4 rss retrieval and normalization.
- Module 4 deterministic dedup_key generation foundation implemented and verified.
- dedup_key uses feed_url-scoped SHA-256 identity with priority source_item_id → link → stable content fallback.
- collected_at is excluded from dedup identity so normal repeated collection does not create a new key.
- Different feeds with the same source item ID produce different dedup keys.
- Missing stable item identity is rejected fail-safe.
- Naive published_at values are normalized deterministically as UTC for content-fallback identity.
- Module 4 dedup-key commit: d80a730 — feat: add module 4 deterministic rss dedup keys.
- D-024 approved and verified: Module 4 uses Psycopg 3 for direct synchronous Python PostgreSQL access with dependencies tracked in requirements.txt; no ORM or SQLAlchemy is introduced.
- D-024 decision commit: c967551 — docs: approve psycopg 3 postgres access.
- Psycopg dependency foundation added with psycopg[binary]==3.3.5 and project .venv exclusion from Git.
- Module 4 dependency-foundation commit: a12fc75 — chore: add psycopg dependency foundation.
- Local project .venv created and verified with Python 3.12.10.
- Psycopg 3.3.5 installed and import-verified inside the project .venv.
- Git working tree verified clean after local .venv creation and Psycopg installation.
- Real Psycopg connection to opportunity_scanner verified as non-superuser opportunity_scanner_app without exposing the database password.
- Module 4 database configuration loader implemented and verified against the ignored local .env without exposing secrets.
- Module 4 PostgreSQL-config commit: cf38bd9 — feat: add module 4 postgres config loader.
- Normalized RSS / Atom source-item PostgreSQL persistence implemented and verified.
- Verified first controlled source-item INSERT through persist_feed_item() as opportunity_scanner_app.
- Verified persisted filter_state and telegram_delivery_state remain independently PENDING by database defaults.
- Verified normal repeated persistence of the same source item returns the existing database id and does not create a duplicate row.
- Verified database-level row count remains one after repeated persistence.
- Synthetic persistence verification row was removed after testing and absence was verified.
- Module 4 normalized-item persistence commit: 4a058c7 — feat: persist normalized rss items in postgres.
- D-025 approved and verified: Module 4 basic filter uses casefold(), stop-word priority, approved positive keywords, PASS / REJECT outcomes, and no multilingual-completeness claim.
- D-025 decision commit: 731411f — docs: define module 4 basic filter rules.
- D-026 approved and verified: SESSION_HANDOFF.md is the controlled MAIN DEVELOPMENT chat continuity mechanism and does not change architecture, roadmap, scope or current module decisions.
- Session handoff workflow commit: 5b57749 — docs: add main development session handoff workflow.
- Module 4 deterministic basic-filter evaluator implemented and verified.
- Verified positive-keyword PASS, casefold matching, stop-word priority REJECT, no-signal REJECT, conditional-context-only REJECT, and empty-text REJECT behavior.
- Verified PASS and REJECT results persist to filter_state in the existing rss_source_items row.
- Verified basic-filter persistence does not modify telegram_delivery_state, which remained PENDING in controlled integration tests.
- Synthetic PASS / REJECT database verification rows were removed after testing and absence was verified.
- Module 4 basic-filter implementation commit: 374d5c1 — feat: add module 4 basic rss filtering.
- Preliminary RSS Telegram message formatter and sender implemented using the existing Telegram Bot API client.
- RSS Telegram messages use only known title, source_name and link data; no AI, payment, KYC, risk or score fields are invented.
- Открыть inline URL button is generated when an RSS item link is available.
- Deterministic formatter and sender tests passed with zero real Telegram API calls.
- Persisted Telegram delivery transition implemented for PASS + PENDING → DELIVERED with telegram_delivered_at.
- Verified REJECT items cannot be marked DELIVERED.
- Verified repeated delivery-state persistence is idempotent and preserves the original telegram_delivered_at timestamp.
- PASS-only delivery orchestration implemented: PASS + PENDING sends first, then persists DELIVERED.
- Verified persisted DELIVERED items are not resent on a normal later orchestration call.
- Verified sender failure leaves the item in PASS + PENDING.
- PostgreSQL delivery-state and orchestration integration tests passed; all synthetic test rows were removed and zero test rows remained.
- Pre-real-delivery implementation tests used REAL_TELEGRAM_CALLS=0; the later controlled real Telegram delivery verification is recorded below.
- Module 4 RSS Telegram delivery implementation commit: 6bbd5c3 — feat: add module 4 rss telegram delivery.
- Module 4 Telegram-delivery documentation sync commit: 8e1a0af — docs: sync module 4 telegram delivery step.
- Performed one controlled real Telegram delivery using a synthetic persisted PASS RSS candidate.
- Verified Telegram configuration and empty webhook state before the real delivery.
- Verified the synthetic candidate transitioned from PASS + PENDING to PASS + DELIVERED after successful sendMessage.
- Verified telegram_delivered_at was persisted.
- Visually verified the real preliminary RSS opportunity message in the configured Telegram target chat.
- Verified the real Открыть inline button opens the configured source URL.
- Live RSS feed retrieval remained disabled during this verification.
- Removed the synthetic real-delivery verification row from PostgreSQL and verified zero matching test rows remained.
- D-033 — SOURCE ACCESS PRECHECK — completed and verified for all five approved V1 sources.
- Verified source statuses: Reddit — BLOCKED; X / Twitter — UNKNOWN — REQUIRES APPROVAL; Discord — AVAILABLE WITH LIMITATIONS; Telegram — BLOCKED; RSS / Atom — AVAILABLE WITH LIMITATIONS.
- SOURCE_ACCESS_PRECHECK.md contains the verification dates, evidence, limitations / blockers and collector proceed / do-not-proceed result for every approved V1 source.
- D-034 — X API Budget and Paid Access Policy — FIXED / APPROVED.
- D-034 approves official X Pay Per Use use in principle, fixes the initial personal-funded maximum at USD $15, requires Auto-recharge OFF, prohibits automatic top-up, and requires separately approved request-count / billable-resource / safe-stop limits before activation.
- D-035 — Quality / Noise / Dedup Policy — FIXED / APPROVED.
- D-035 fixes the cross-module objective MINIMUM NOISE → MAXIMUM ACTIONABLE OPPORTUNITIES, stable source identity, deterministic deduplication, Filter-before-AI behavior, duplicate-delivery prevention, expired / closed exclusion from the normal production Telegram flow, and final quality / risk / scoring gates for production Telegram delivery.
- D-036 — X Bounded Live-Access Envelope — FIXED / APPROVED.
- D-036 fixes the first controlled paid X verification envelope at maximum USD $1.00 spend, 20 paid API requests, 10 Posts maximum per Recent Search request and 200 maximum billable returned Posts / resources, with hard fail-safe stop conditions and Auto-recharge OFF.
- D-037 — X Minimum Credit Purchase Authorization — FIXED / APPROVED.
- D-037 authorizes one-time USD $5.00 prepaid credit purchase because the verified X Developer Console rejects USD $1.00 and requires a USD $5.00 minimum; it does not increase the D-036 live-spend authorization above USD $1.00.
- X Developer Console activation-readiness verification confirmed and saved Billing Cycle Cap at USD $1.00.
- D-037 authorized one-time USD $5.00 prepaid credit purchase executed successfully; verified remaining balance USD $5.00, Auto Recharge OFF and Current Spend USD $0.00.
- D-038 — X Development Project Access Authorization — FIXED / APPROVED.
- D-038 authorizes only `Connect · Development` to the existing `Default Project — Pay Per Use`; `Staging` and `Production` remain unauthorized, and the decision does not authorize credentials, paid API requests or X Collector implementation.

## IN PROGRESS
D-038 documentation synchronization. Development Project Access is approved but has not yet been executed. The X App remains disconnected from `Default Project — Pay Per Use`. No credential generation, paid API request or X Collector implementation is authorized by D-038.

## NEXT STEP
Complete D-038 documentation synchronization and Git commit. After Git is clean, execute only the separately approved `Connect · Development` Project Access action and verify the resulting Project Access and billing-safety state before any further action. Do not connect to Staging or Production, generate credentials, make a paid live API request or begin X Collector implementation.

## BLOCKERS
Module 5 — Reddit Collector is BLOCKED — DATA ACCESS NOT APPROVED. The Reddit Data Team did not approve the submitted access request. This blocker applies to Reddit Collector implementation and must not be bypassed.

Module 7 — X Collector is not formally BLOCKED, but remains PRE-IMPLEMENTATION / ACCESS GATED. D-034 caps the initial personal-funded budget at USD $15. D-036 fixes the current live-verification envelope at USD $1.00 / 20 requests / 10 Posts per request / 200 billable returned Posts or resources with deterministic safe-stop conditions. D-037 authorized the completed one-time USD $5.00 prepaid credit purchase without increasing the D-036 live-spend limit. D-038 now authorizes only Development Project Access to the existing `Default Project — Pay Per Use`; Staging and Production remain unauthorized. Verified billing state remains Remaining Balance USD $5.00, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.00. The active X App is still disconnected from the Project, and no paid live request has been made.

Module 8 — Telegram Sources has a verified D-033 status of BLOCKED under the currently approved end-to-end architecture because Telegram's current AI-use terms conflict with downstream use of Telegram-derived content in the approved AI stage. Resolution requires a separate explicit project decision and must not be bypassed.

## KNOWN ISSUES
- Conflict 1 — RESOLVED by D-017.
- Conflict 2 — RESOLVED by D-021. Module 4 uses only the minimal basic filtering slice required for RSS → Database → Filter → Telegram; Module 6 remains the location of the full Filter Engine.

## ARCHITECTURE VERSION
Opportunity Scanner AI Architecture v1.0 — FIXED
D-017 defines cross-cutting PostgreSQL persistence without changing the logical pipeline or roadmap.
D-019 and D-020 define the completed Module 3 Telegram Bot foundation without changing the logical pipeline or roadmap.
D-021 resolves the Module 4 basic-filtering boundary without changing the logical pipeline, roadmap or Module 6 position.
D-022 resolves the RSS / Official Blogs source ambiguity without adding a new source type.
D-023 fixes the Module 4 RSS Collector scope and acceptance criteria without changing the logical pipeline or roadmap.
D-024 fixes the direct Python PostgreSQL access mechanism as Psycopg 3 with requirements.txt and no ORM, without changing the PostgreSQL architecture, logical pipeline or roadmap.
D-025 fixes the minimum deterministic Module 4 basic-filter rules without moving the full multilingual Filter Engine out of Module 6.
D-026 fixes the MAIN DEVELOPMENT session handoff workflow without changing architecture, roadmap, scope or module decisions.
D-027 fixes the Module 4 initial live-feed safety mechanism: exactly one configured feed URL, at most one parser item entering persistence/downstream processing, deterministic first-item selection, and no uncontrolled historical backlog.
D-028 fixes the Module 5 Reddit Collector scope, official-access gate, Reddit data compliance boundary, and future AI compliance gate without changing the approved architecture, roadmap, module order or source list.
D-029 records the verified Reddit access denial and permits controlled roadmap execution to continue beyond blocked Module 5 without changing the approved architecture, source list, roadmap definitions or Module 5 scope.
D-030 fixes the Module 6 Filter Engine scope and acceptance criteria without changing the fixed logical pipeline, approved architecture, roadmap definitions, source list or module order.
D-031 fixes the exact Module 6 multilingual filtering rules, deterministic matching semantics and downstream responsibility boundaries without changing the approved architecture or Module 6 scope.
D-032 fixes the Module 7 X Collector scope, official-access boundary, cost boundary and pre-persistence compliance gate without changing the approved architecture, source list or roadmap order.
D-033 fixes the SOURCE ACCESS PRECHECK process, formal source-status criteria, verification-date requirement and evidence requirement without changing the approved architecture, roadmap, module order or V1 source list.
D-034 fixes the X API budget, paid-access and fail-safe cost boundaries without changing the approved architecture, roadmap, module order or V1 source list.
D-035 fixes the cross-module quality, noise and deduplication policy without changing the approved architecture, roadmap, source list or module order.
D-036 fixes the first bounded X live-access envelope without changing the approved architecture, roadmap, source list or module order.
D-037 fixes the minimum prepaid X credit purchase authorization without changing the D-036 live-spend envelope or the approved architecture, roadmap, source list or module order.
D-038 fixes Development-only X Project Access authorization without changing the D-036 live envelope or the approved architecture, roadmap, source list or module order.
- D-027 bounded live-feed verification mode implemented in rss_collector.py.
- Added deterministic first-parser-item processing with at most one item entering persistence and downstream processing.
- Added allowlist enforcement before live feed retrieval.
- Verified bounded processor with three parsed items: only the first item entered persistence/downstream processing.
- Verified allowlist rejection occurs before fetch for a non-configured URL.
- Verified real PostgreSQL integration: PASS delivery state, normal repeated-run deduplication, REJECT behavior, empty-feed behavior, and cleanup.
- Verified invalid feed creates zero false PostgreSQL rows.
- All D-027 implementation verification before live use completed with REAL_TELEGRAM_CALLS=0 and LIVE_RSS_RETRIEVAL=0.
- D-027 implementation commit: 826b051 — feat: add bounded live rss verification mode.
- Configured exactly one initial live RSS feed URL: https://openai.com/news/rss.xml.
- Verified the project configuration loader sees exactly one configured RSS feed before live retrieval.
- Performed the first controlled D-027 live RSS retrieval.
- The real feed parsed 1192 items; only the deterministic first parser item entered PostgreSQL and downstream processing.
- Verified ROW_COUNT_DELTA=1, satisfying the D-027 persistence bound.
- The selected real RSS item evaluated to REJECT and therefore produced no Telegram notification.
- The real item persisted with filter_state=REJECT, telegram_delivery_state=PENDING and no telegram_delivered_at timestamp.
- FIRST_CONTROLLED_LIVE_RSS_TEST=PASS and D027_BOUND_CHECK=PASS.
- The live verification did not modify tracked repository files.
- Focused D-023 acceptance review completed.
- The remaining local run / verification documentation gap was closed in README.md.
- Module 4 local verification procedure commit: ff04bff — docs: add module 4 local verification procedure.
- All D-023 acceptance criteria are now verified with recorded evidence.
- Module 4 — RSS Collector: COMPLETED / PASS.

## LAST VERIFIED STATE
2026-09-22 — GitHub main is synchronized through purchase-execution milestone commit 2ac2e21. D-038 — X Development Project Access Authorization — is FIXED / APPROVED. Only `Connect · Development` to the existing `Default Project — Pay Per Use` is authorized; Staging and Production are not authorized. The App remains disconnected pending D-038 documentation synchronization and clean Git state. Verified billing state remains Remaining Balance USD $5.00, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.00. No paid live API request has been made and X Collector implementation has not started.
