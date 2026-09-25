# OPPORTUNITY SCANNER AI — TODO

## CURRENT PRIORITY

Synchronize approved D-046 and its D-033 source-status reconciliation into the remaining authoritative project documentation and Git. Formal X / Twitter source status is `AVAILABLE WITH LIMITATIONS`. Persistent production X collection remains `COMPLIANCE-GATED / NOT AUTHORIZED` until a mechanism is proven to satisfy the applicable 24-hour compliance requirement. After documentation synchronization, the next separate technical gate must focus on proving 24-hour compliance suitability. No X API request, Compliance Job, Posts Lookup, migration `003_x_source_items.sql`, PostgreSQL change, persistent production collection or X Collector implementation is authorized during this synchronization step.

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
- [x] X / Twitter — AVAILABLE WITH LIMITATIONS under the D-046 D-033 reconciliation — approved official X access path verified; persistent production X collection remains separately `COMPLIANCE-GATED / NOT AUTHORIZED`.
- [x] Discord — AVAILABLE WITH LIMITATIONS.
- [x] Telegram — BLOCKED — current AI-use terms conflict with the approved downstream AI stage.
- [x] RSS / Atom — AVAILABLE WITH LIMITATIONS.
- [x] Verify date and evidence for all five approved V1 sources.
- [x] Record collector proceed / do-not-proceed result for all five sources.
- [x] Mark SOURCE ACCESS PRECHECK COMPLETE / VERIFIED under D-033.

## D-034 / D-035 / D-036 / D-037 / D-038 / D-039 / D-040 / D-041 / D-042 / D-043 / D-044 / D-045 POLICY MILESTONE

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
- [x] Approve D-038 Development-only Project Access to existing `Default Project — Pay Per Use`.
- [x] Keep Staging and Production Project Access unauthorized.
- [x] Keep credential generation, paid API requests and X Collector implementation outside D-038 authorization.
- [x] Execute authorized D-038 `Connect · Development` action.
- [x] Verify Development Project Access is connected to `Default Project — Pay Per Use`.
- [x] Verify post-connection Remaining Balance remains USD $5.00.
- [x] Verify post-connection Billing Cycle Cap remains USD $1.00.
- [x] Verify post-connection Auto Recharge remains OFF.
- [x] Verify post-connection Current Spend remains USD $0.00.
- [x] Verify no new credentials were generated and no paid live API request was made.
- [x] Approve D-039 X Bearer Token generation and local secret handling.
- [x] Approve `X_BEARER_TOKEN` as the local environment variable name.
- [x] Verify repository-root `.env` is ignored by Git and not tracked.
- [x] Add safe `X_BEARER_TOKEN` placeholder to tracked `.env.example`.
- [x] Verify local `.env` contains exactly one empty `X_BEARER_TOKEN` key before generation.
- [x] Verify X Console `Generate` control opens `Regenerate Bearer Token` confirmation.
- [x] Explicitly approve D-039 execution clarification allowing Bearer Token regeneration and possible invalidation of the previous token.
- [x] Regenerate X Bearer Token through the verified `Generate → Regenerate` flow and store it only in local `.env`.
- [x] Verify regenerated Bearer Token using non-secret comparison only — `TOKEN_MATCH=True`; clipboard cleared.
- [x] Keep all X API requests and X Collector implementation outside D-039 authorization.
- [x] Require unused prepaid credit balance to remain unauthorized for further spend without separate explicit approval.
- [x] Approve D-040 — X First Bounded Live API Verification Authorization.
- [x] Restrict D-040 to exactly one `GET /2/tweets/search/recent` request.
- [x] Fix D-040 `max_results=10` and the approved deterministic query: `("paid testing" OR "user testing") lang:en has:links -is:retweet`.
- [x] Prohibit pagination, expansions, User lookups, additional endpoints and a second API request under D-040.
- [x] Prohibit persistence or logging of returned X Post content during D-040 verification.
- [x] Restrict verification evidence to HTTP status, `meta.result_count` and actual returned Post count.
- [x] Require pre-request and post-request billing / usage verification and immediate STOP on any D-040 safe-stop condition.
- [x] Verify required pre-request billing state: Remaining Balance USD $5.00; Billing Cycle Cap USD $1.00; Auto Recharge OFF; Current Spend USD $0.00.
- [x] Execute the single authorized D-040 live Recent Search verification request — HTTP 200; `meta.result_count=10`; 10 returned Posts.
- [x] Verify post-request billing / usage state before any further X action — Remaining Balance USD $4.95; Billing Cycle Cap USD $1.00; Auto Recharge OFF; Current Spend USD $0.05.

- [x] Approve D-041 — X Content Compliance and Persistence Policy.
- [x] Prohibit persistent live X Content until a separately approved X-specific PostgreSQL persistence design implements D-041.
- [x] Prohibit automatic retention after compliance removal of Post IDs, hashes, fingerprints, mappings, identifiers or other source-derived derivatives unless separately confirmed permissible by official X terms or authorization.
- [x] Require any retained internal processing history after compliance removal to be independent of removed X Content and unable to reconstruct, identify or link the removed source item.
- [x] Defer exact compliant tombstone representation, schema, migration and deletion mechanics to a separate schema / persistence decision.
- [x] Keep D-041 outside X API request authorization, X Collector implementation and PostgreSQL schema-change authorization.
- [x] Define and explicitly approve D-042 — X PostgreSQL Persistence Schema and Compliance Lifecycle.

- [x] Approve `x_edit_root_id` as the retained logical edit-chain identity and `x_post_id` as the current revision identity.
- [x] Require `UNIQUE(x_edit_root_id)` for retained logical deduplication and in-place revision updates with re-filtering.
- [x] Approve hard compliance DELETE with no tombstone and no retained source-derived identity after removal.
- [x] Keep migration `003_x_source_items.sql`, PostgreSQL changes, new API requests, Batch Compliance jobs and X Collector implementation outside D-042 authorization.
- [x] Record Batch Compliance only as a candidate compliance-synchronization mechanism pending separate verification.
- [x] Keep Compliance Streams outside the assumed V1 solution because current documentation requires Enterprise access.
- [ ] Verify and explicitly approve an officially permitted compliance-synchronization mechanism for Module 7.

- [x] Approve D-043 — X Batch Compliance Account Access Verification Authorization.
- [x] Confirm documented unit cost of USD $0.005 for `GET /2/compliance/jobs`.
- [x] Authorize exactly one future read-only `GET /2/compliance/jobs?type=tweets` request solely for Development App access verification.
- [x] Keep Compliance Job creation, POST, Post Lookup, rehydration, migration, PostgreSQL changes, persistent live X collection and X Collector implementation outside D-043 authorization.
- [x] Verify pre-request billing state — Remaining Balance USD $4.95; Billing Cycle Cap USD $1.00; Auto Recharge OFF; Current Spend USD $0.05.
- [x] Execute exactly one authorized D-043 GET — HTTP 200; `DATA_PRESENT=False`; `META_RESULT_COUNT=0`; `ACCESS_RESULT=PASS`; authorization exhausted.
- [x] Verify post-request billing state — Remaining Balance USD $4.95; Billing Cycle Cap USD $1.00; Auto Recharge OFF; Current Spend USD $0.05; exact USD $0.005 charge not independently visible at Console cent precision.

- [x] Approve D-044 — X Batch Compliance Synthetic Lifecycle Verification Authorization.
- [x] Limit D-044 to one synthetic `not_a_valid_id` lifecycle attempt.
- [x] Limit D-044 to one create POST, one signed upload PUT, at most six status GET requests and one signed download GET.
- [x] Prohibit automatic retries, second job creation and requests outside the D-044 envelope.
- [x] Fix maximum pre-verified create-plus-polling cost at USD $0.040.
- [x] Record signed upload PUT cost as UNKNOWN / NOT SEPARATELY VERIFIED.
- [x] Record signed download GET cost as UNKNOWN / NOT SEPARATELY VERIFIED.
- [x] Keep Billing Cycle Cap at USD $1.00 and Auto Recharge OFF.
- [x] Complete D-044 execution-result documentation / Git synchronization — commit `1e42808` pushed to `origin/main` and final branch synchronization verified.
- [x] Verify pre-request billing state before the first D-044 network operation — Remaining Balance USD $4.95; Billing Cycle Cap USD $1.00; Auto Recharge OFF; Current Spend USD $0.05.
- [x] Execute exactly one D-044 synthetic lifecycle attempt within the approved envelope — create HTTP 200; upload HTTP 200; one status GET HTTP 200 with job status `complete`; download HTTP 200 with one result record; safe parser returned `ERROR_CATEGORY=UNKNOWN_OR_NONE`; expected `invalid_id` semantic result not verified; D-044 verification result FAIL; authorization exhausted.
- [x] Verify final billing state after D-044 — Remaining Balance USD $4.95; Billing Cycle Cap USD $1.00; Auto Recharge OFF; Current Spend USD $0.05; observed cent-level Current Spend delta USD $0.00, which does not prove zero actual lifecycle cost.

- [x] Approve D-045 — X Batch Compliance D-044 Semantic Reconciliation.
- [x] Preserve D-044 historical result without silently rewriting the approved test or execution record.
- [x] Record D-044 transport verification as PASS.
- [x] Preserve D-044 semantic verification as FAIL UNDER THE APPROVED D-044 TEST ORACLE.
- [x] Record D-045 CURRENT-DOCUMENTATION CORRECTION: current official Batch Compliance documentation supports malformed `not_a_valid_id` → `invalid_id`, `rehydrate / tweet_edited`, and separate `scrub_geo / geo_scrubbed`; the earlier D-045 conclusion is superseded without rewriting historical D-045 text.
- [x] Record actual D-044 downloaded-record semantics as UNKNOWN / NOT RECOVERABLE FROM RETAINED EVIDENCE.
- [x] Record `not_a_valid_id` as a currently documented malformed-input example producing `invalid_id`; D-044 parser failure remains unexplained because the raw downloaded record was not retained.
- [x] Require any future Batch Compliance semantic test to define parser / oracle and PASS / FAIL conditions from then-current official documentation before execution.
- [x] Confirm D-045 authorizes no X API request.
- [x] Complete D-045 CURRENT-DOCUMENTATION CORRECTION / Git synchronization — commit `1f09a40` pushed to `origin/main`; final branch synchronization verified.
## ROADMAP

- [x] MODULE 2 — PostgreSQL
- [x] MODULE 3 — Telegram Bot
- [x] MODULE 4 — RSS Collector
- [ ] MODULE 5 — Reddit Collector — BLOCKED — DATA ACCESS NOT APPROVED
- [x] MODULE 6 — Filter Engine — COMPLETED / PASS
- [ ] MODULE 7 — X Collector — SCOPE APPROVED / PRE-IMPLEMENTATION / ACCESS GATED — formal D-033 X / Twitter status: AVAILABLE WITH LIMITATIONS under D-046; official access path verified; D-034 through D-046 are FIXED / APPROVED; Module 7 is not PASS; Batch Compliance is not approved as the production compliance-synchronization mechanism; persistent production X collection remains `COMPLIANCE-GATED / NOT AUTHORIZED` until the applicable 24-hour compliance requirement is proven satisfiable; production cadence, backup / WAL / restore compliance and recurring operating cost remain unresolved; D-046 authorizes no additional X API request, Compliance Job, Posts Lookup, migration `003_x_source_items.sql`, PostgreSQL change, X Collector implementation, Staging connection or Production connection.
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
