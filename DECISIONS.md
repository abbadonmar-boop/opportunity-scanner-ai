# OPPORTUNITY SCANNER AI — DECISIONS

## STATUS
Baseline project decisions — FIXED unless explicitly changed with user approval.

## D-001 — PRODUCT TYPE
Status: FIXED

Opportunity Scanner AI v1 is a personal software product.

- Personal tool, not SaaS.
- Automatic monitoring, not a manual Search Hub.
- Designed for continuous production operation.

## D-002 — PRIMARY USER INTERFACE
Status: FIXED

Telegram is the primary user interface for v1.

User-facing opportunity explanations are in Russian.

## D-003 — SUPPORTED SOURCE LANGUAGES
Status: FIXED

The system must process publications in:
- English
- Russian
- Ukrainian
- German

## D-004 — LOGICAL ARCHITECTURE
Status: FIXED

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

Architecture changes require a demonstrated technical reason and user approval.

## D-005 — APPROVED V1 SOURCES
Status: FIXED

Only the following source types are approved for the initial version:
- X / Twitter
- Reddit
- Telegram channels
- Discord servers
- RSS / Atom

The source list must not be expanded before the approved core pipeline is stable unless explicitly approved.

## D-006 — CATEGORY PRIORITY
Status: FIXED

Priority order:
1. AI / Data
2. Testing
3. Beginner-friendly Remote Work
4. Web3

Web3 is one category, not the whole product.

## D-007 — MINIMUM PAYOUT
Status: FIXED

Default minimum payout for the main Telegram flow: $5.

Lower-value opportunities may be stored but must not create unnecessary noise in the primary Telegram flow.

## D-008 — KYC
Status: FIXED

KYC is allowed.

KYC must be explicitly represented as:
- YES
- NO
- UNKNOWN

KYC affects accessibility and risk but is not an automatic rejection.

## D-009 — UNKNOWN TOKENS
Status: FIXED

Unknown project tokens are not automatically rejected.

They must be treated as speculative rewards, receive lower priority, and be checked for liquidity, tradability and withdrawal when possible.

## D-010 — AI PROCESSING ORDER
Status: FIXED

AI must not process the entire raw incoming stream.

Candidates must first pass:
- normalization;
- deduplication;
- inexpensive rule-based filtering.

AI analysis occurs only after those stages.

## D-011 — DATA STORAGE
Status: FIXED

PostgreSQL is the approved database for v1.

The system must store processing history.

Source-specific retention and deletion policies remain unresolved and must be defined when required by the relevant source integration.

## D-012 — SECURITY BOUNDARIES
Status: FIXED

The system must not automatically:
- perform third-party tasks on behalf of the user;
- connect wallets;
- sign transactions;
- send money;
- make deposits;
- expose secrets.

API keys, passwords, tokens, private keys and seed phrases must never be stored in source code or committed configuration.

## D-013 — ANTI-SCAM SAFETY PRINCIPLE
Status: FIXED

Anti-Scam must not claim absolute safety.

The system must not label an opportunity as a scam without sufficient evidence.

Safety controls cannot be overridden by AI or personalization.

## D-014 — PROHIBITED UNAPPROVED INFRASTRUCTURE
Status: FIXED

Do not introduce without demonstrated need and explicit approval:
- Kafka or another message broker
- Redis
- Microservice decomposition
- Kubernetes
- Web UI
- Mobile app

## D-015 — DEVELOPMENT METHOD
Status: FIXED

Development follows:

CURRENT STATE
→ ONE REQUIRED STEP
→ USER RESULT
→ VERIFICATION
→ PASS / FAIL
→ DOCUMENTATION / GIT WHEN REQUIRED
→ NEXT STEP

A module is not complete merely because code exists.

Technical PASS requires evidence.

## D-016 — WORK ROLE
Status: FIXED

The MAIN DEVELOPMENT chat controls the project.

ChatGPT Work is auxiliary only and may be used only through an explicitly declared WORK CHECKPOINT according to WORK_USAGE_POLICY_v1.0.md.

## D-017 — POSTGRESQL CROSS-CUTTING PERSISTENCE LAYER
Status: FIXED / APPROVED

PostgreSQL is the single cross-cutting persistence layer for Opportunity Scanner AI.

Primary persistence occurs after collection / normalization as early as necessary to support reliable recovery.

The same persisted record is then updated as it progresses through:

DEDUPLICATE
→ FILTER
→ EXTRACT
→ AI
→ RISK
→ SCORE

No separate database or second persistence system is introduced.

This decision defines persistence behavior across the processing lifecycle.

It does not change or reorder the fixed logical pipeline:

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

The approved roadmap is unchanged.
## D-018 — MODULE 2 POSTGRESQL SCOPE AND ACCEPTANCE CRITERIA
Status: FIXED / APPROVED

Module 2 implements the local PostgreSQL foundation required by the approved architecture and D-017.

### SCOPE

Module 2 must provide:

1. One local PostgreSQL instance for development.
2. PostgreSQL execution through the approved Docker / Docker Compose environment.
3. Persistent storage that survives container restart.
4. A dedicated project database.
5. A dedicated project database user; application access must not rely on the PostgreSQL superuser.
6. Database credentials and secrets kept outside tracked Git files.
7. Verified connectivity to the project database.
8. A minimal reproducible baseline schema / migration mechanism only to the extent required for subsequent pipeline development.
9. Verified write → read → restart → persistence behavior.
10. Documented commands / procedure for starting, stopping and verifying the local database.

### OUT OF SCOPE FOR MODULE 2

Module 2 does not implement:

- source collectors;
- Telegram integration;
- AI Analyzer;
- Filter Engine;
- Anti-Scam Engine;
- Scoring Engine;
- production PostgreSQL deployment or VPS deployment;
- an ORM unless a demonstrated requirement arises during this module.

Deferred technical decisions must not be selected merely for convenience.

### ACCEPTANCE CRITERIA

Module 2 receives PASS only when all of the following are verified with evidence:

- PostgreSQL container starts without blocking errors.
- PostgreSQL healthcheck passes.
- Dedicated project database exists.
- Dedicated project database user exists.
- Credentials / secrets are not stored in tracked Git files.
- Connection to the project database succeeds.
- A test record can be written and read successfully.
- Test data remains available after PostgreSQL container restart.
- Baseline schema / migration setup is reproducible from a clean state.
- Database start / stop / verification procedure is documented.
- Relevant repository documentation is synchronized.
- The logical milestone is recorded in Git.
- Final Git working tree state is verified.

### ARCHITECTURE RELATION

D-018 does not change the fixed logical pipeline or roadmap.

PostgreSQL remains the single cross-cutting persistence layer defined by D-017.
## UNRESOLVED / DEFERRED DECISIONS

The following must not be invented prematurely:

- specific Python libraries and frameworks;
- ORM;
- migration framework;
- scheduler;
- AI provider and model;
- AI response schema and retry/cost policy;
- Telegram framework;
- detailed Filter Engine rules;
- detailed Anti-Scam providers and thresholds;
- Scoring weights, formulas and thresholds;
- Risk scale direction;
- PostgreSQL source-specific retention policy;
- exact handling of deleted or modified source content.

## KNOWN DECISION CONFLICTS

1. RESOLVED — D-017 defines PostgreSQL as the single cross-cutting persistence layer, with early persistence for recovery and progressive updates to the same record. The fixed logical pipeline and roadmap remain unchanged.
2. RESOLVED — D-021 defines Module 4 basic filtering as the minimum first implementation of the existing FILTER component required for RSS → Database → Filter → Telegram. The full Filter Engine remains in Module 6.

Conflict 1 is resolved by D-017.
Conflict 2 is resolved by D-021. Neither resolution changes the fixed logical pipeline or roadmap.





## D-019 — MODULE 3 TELEGRAM BOT SCOPE AND ACCEPTANCE CRITERIA
Status: FIXED / APPROVED

Module 3 establishes the minimal Telegram Bot foundation required by the approved Telegram-first product architecture.

### SCOPE

Module 3 must provide:

1. One personal Telegram Bot interface for Opportunity Scanner AI.
2. Integration through the approved Telegram Bot API.
3. Russian user-facing bot responses.
4. Bot token and Telegram secrets kept outside tracked Git files.
5. Access restricted to the configured owner; other Telegram user IDs must not be served by the personal bot flow.
6. A minimal `/start` interaction with a verified Russian response.
7. Verified bidirectional communication between the configured user and the bot.
8. A test opportunity message formatter using the Telegram fields already defined by the project requirements.
9. A working `Открыть` URL button for the test opportunity message.
10. A documented local start and verification procedure.

### TELEGRAM OPPORTUNITY PRESENTATION

The test opportunity message may present the project-defined user-facing fields, including where available:

- title;
- source;
- category;
- payment;
- KYC;
- deposit;
- geography;
- deadline;
- risk;
- final assessment;
- source link.

The `Открыть` button may be implemented as a normal URL button.

The planned buttons:

- `Сохранить`
- `Подходит`
- `Не подходит`
- `Мошенничество`
- `Уже закрыто`

must not receive database or opportunity-status semantics during Module 3 unless that behavior is separately defined and approved.

### DEFERRED TECHNICAL CHOICES

Module 3 does not approve a Telegram Python framework merely for convenience.

The Telegram framework remains deferred until the implementation step demonstrates the minimum technical requirement and current official Telegram documentation is reviewed.

The exact local update transport mechanism must likewise be selected only when implementation requires it and after verification against current official Telegram Bot API documentation.

### OUT OF SCOPE FOR MODULE 3

Module 3 does not implement:

- Telegram source collection;
- RSS collection;
- Reddit collection;
- X / Twitter collection;
- Discord collection;
- Filter Engine;
- AI Analyzer;
- Anti-Scam Engine;
- Score Engine;
- scheduler;
- production deployment;
- unapproved database semantics for Telegram status buttons.

### ACCEPTANCE CRITERIA

Module 3 receives PASS only when all of the following are verified with evidence:

- Telegram bot token is not stored in tracked Git files.
- Connection to the Telegram Bot API succeeds.
- Bot identity is verified.
- Local bot process starts without blocking errors.
- Configured owner receives a Russian response to `/start`.
- An unauthorized Telegram user ID is not served by the personal bot flow.
- Bidirectional bot communication is verified.
- A test opportunity message renders the approved project fields correctly.
- The `Открыть` URL button works.
- Secrets are not exposed in logs or committed configuration.
- Local start and verification procedure is documented.
- Relevant repository documentation is synchronized.
- The logical Module 3 milestone is recorded in Git.
- Final Git working tree state is verified.

### ARCHITECTURE RELATION

D-019 does not change the fixed logical pipeline, roadmap, product scope or security boundaries.

Telegram remains the primary user interface defined by D-002.

The Telegram framework remains a deferred technical decision until justified by the implementation step.

## D-020 — MODULE 3 TELEGRAM TRANSPORT AND CLIENT APPROACH
Status: FIXED / APPROVED

Module 3 uses the official Telegram Bot API directly over HTTPS.

### CLIENT APPROACH

For the local Module 3 implementation:

- Python 3.12 standard library is used for direct HTTPS communication with the Telegram Bot API.
- No external Telegram framework is introduced unless a demonstrated technical requirement arises later.
- `getUpdates` long polling is the approved local update transport for Module 3.
- Webhook-based update delivery is not used for the normal local Module 3 flow.

This decision does not prohibit a Telegram framework or webhook in a later module if a demonstrated technical requirement arises and the change is explicitly approved.

### WEBHOOK SAFETY RULE

Before starting `getUpdates` long polling, the bot must call `getWebhookInfo`.

Behavior is fixed as follows:

1. If `getWebhookInfo` reports an empty `url`, long polling may continue.
2. If `getWebhookInfo` reports a non-empty `url`, the current implementation step must stop.
3. The bot must not call `deleteWebhook` automatically.
4. Existing webhook state must be returned to MAIN DEVELOPMENT for a separate explicit decision before any modification is made.

The system must not silently modify an existing Telegram webhook configuration.

### LOCAL TELEGRAM CONFIGURATION

The local configuration must keep the following parameters separate:

- `owner_id`
- `target_chat_id`

Their responsibilities are different:

- `owner_id` is used to authorize the owner for bot commands and owner-only interaction.
- `target_chat_id` identifies the Telegram chat where Opportunity Scanner AI sends opportunity notifications.

If the personal owner chat is also used as the notification destination, `owner_id` and `target_chat_id` may resolve to the same effective recipient, but they must remain separate configuration parameters.

Real Telegram IDs and bot tokens must not be committed to tracked Git configuration.

### BOT TOKEN

The Telegram bot token must:

- be loaded from local configuration outside tracked Git files;
- never be hard-coded in source code;
- never be printed in logs or diagnostic output;
- never be included in committed configuration.

### IMPLEMENTATION BOUNDARY

D-020 defines only the minimal Telegram transport and client approach required by Module 3.

It does not add:

- Telegram source collection;
- production webhook infrastructure;
- public HTTPS endpoints;
- an external Telegram framework;
- scheduler infrastructure;
- database semantics for Telegram status buttons.

### ARCHITECTURE RELATION

D-020 does not change the fixed logical pipeline, roadmap, product scope or security boundaries.

Telegram remains the primary user interface defined by D-002.

D-019 remains the authoritative Module 3 scope and acceptance criteria.

## D-021 — MODULE 4 BASIC FILTERING BOUNDARY
Status: FIXED / APPROVED

Module 4 does not introduce a separate or second Filter Engine.

### MODULE 4 FILTERING BOUNDARY

Module 4 implements only the minimum first slice of the existing architectural FILTER component required for the working RSS pipeline:

RSS → Database → basic rule-based Filter → Telegram

Module 4 may implement only:

- deterministic filtering using the minimum required keywords and stop-words;
- a PASS or REJECT result for an RSS record;
- persistence of the filtering result in the existing PostgreSQL record;
- Telegram delivery only for records that pass the basic filter.

### OUT OF SCOPE FOR MODULE 4 BASIC FILTERING

Module 4 does not implement:

- the full Filter Engine;
- advanced filtering logic;
- scoring;
- AI analysis;
- Anti-Scam analysis;
- personalization;
- complex rule systems;
- a second or temporary filtering mechanism;
- new infrastructure or technologies solely for filtering.

### MODULE 6 RELATION

Module 6 remains the roadmap location of the full Filter Engine.

The basic filtering introduced in Module 4 is not a disposable duplicate. It is the minimal first implementation of the same architectural FILTER component, which Module 6 later extends into the full Filter Engine.

### ARCHITECTURE RELATION

D-021 resolves Conflict 2 only to the minimum extent required for Module 4.

It does not change the fixed logical pipeline, roadmap, product scope, database architecture, or Module 6 position.

Rule-based filtering remains before AI in the logical pipeline.


## D-022 — RSS FEEDS FROM OFFICIAL BLOGS BOUNDARY
Status: FIXED / APPROVED

Official Blogs are not introduced as a new source type or separate collector.

### ALLOWED RSS / ATOM BEHAVIOR

An RSS or Atom feed published by an official company, project, organization or product website may be used by Module 4 as a normal RSS / Atom source when that feed is explicitly configured as an approved RSS source.

Such a feed remains source type RSS / Atom and follows the same Module 4 pipeline:

RSS → Database → basic Filter → Telegram

### OUT OF SCOPE

Module 4 does not introduce:

- HTML or general web scraping;
- automatic discovery of official blogs;
- website crawling;
- a separate Official Blogs Collector;
- a new Official Blogs source category;
- expansion of the approved V1 source-type list.

### SOURCE CLASSIFICATION

The publisher being an official company, project, organization or product website does not create a new source type.

If the input is consumed through an explicitly configured RSS or Atom feed, it is treated as RSS / Atom.

### ARCHITECTURE RELATION

D-022 resolves the ambiguity between approved RSS / Atom sources and the exclusion of Official Blogs as a separate source category.

It does not change the fixed source list, logical pipeline, roadmap, product scope or collector architecture.


## D-023 — MODULE 4 RSS COLLECTOR SCOPE AND ACCEPTANCE CRITERIA
Status: FIXED / APPROVED

Module 4 implements the first working end-to-end pipeline:

RSS / Atom → COLLECT → NORMALIZE → early PostgreSQL persistence → DEDUPLICATE → basic FILTER → Telegram

Early PostgreSQL persistence follows D-017 and does not change the fixed logical pipeline.

### SCOPE

Module 4 must provide:

1. An explicitly configured allowlist of RSS / Atom feed URLs. Automatic feed discovery is not introduced.
2. Network retrieval of configured RSS / Atom feeds.
3. Minimal normalization of source items including, where available: source, source item identifier, title, link, text or summary, publication time, and collection time.
4. A minimal PostgreSQL migration for normalized source items and their processing state. This is not the final universal opportunity schema.
5. Deduplication sufficient to prevent repeated processing of the same RSS / Atom item from creating a second database row.
6. Separate persisted state for basic filter processing and Telegram delivery.
7. Telegram delivery state sufficient to prevent a successfully delivered item from being sent again during a normal subsequent run after successful delivery state has been persisted.
8. Basic filtering strictly within D-021: minimal deterministic keywords and stop-words with PASS or REJECT result.
9. Persistence of the basic filter result in the same PostgreSQL source-item record.
10. REJECT items are not delivered to Telegram.
11. PASS items are delivered to the configured TELEGRAM_TARGET_CHAT_ID.
12. Module 4 Telegram messages represent preliminary RSS candidates, not final AI analysis. Only data actually known at this stage may be presented.
13. Payment, KYC, risk, score and other not-yet-extracted or not-yet-analyzed fields must not be invented.
14. A working Открыть URL button links to the original source publication.
15. RSS / Atom feeds from official websites are handled according to D-022 and remain RSS / Atom sources.
16. Local Module 4 execution may use a manual one-shot run. Scheduler infrastructure is not introduced in Module 4.
17. The first live RSS verification must use safely limited initial-feed behavior so historical backlog cannot be sent to Telegram without control.
18. No framework, ORM or migration framework is introduced unless a demonstrated technical requirement arises during implementation.

### TELEGRAM DELIVERY SEMANTICS

Module 4 does not claim an absolute exactly-once delivery guarantee.

The acceptance requirement that a repeated run does not create a duplicate Telegram notification applies to the normal case in which Telegram delivery succeeded and the successful delivery state was subsequently persisted in PostgreSQL.

A crash or process failure in the window between a successful Telegram sendMessage response and persistence of the delivery state may result in a later duplicate notification.

Module 4 must not falsely represent this crash window as solved unless a separate later design explicitly addresses it.

### INITIAL FEED SAFETY

The first live RSS verification must not cause uncontrolled delivery of historical feed backlog.

Initial-feed behavior must be deliberately limited for verification before broader live operation is allowed.

The exact minimal mechanism may be selected during implementation, but it must be deterministic, testable and documented before live verification.

### OUT OF SCOPE

Module 4 does not implement:

- the full Filter Engine;
- EXTRACT;
- AI Analyzer;
- Anti-Scam Engine;
- Score Engine;
- Reddit, X / Twitter, Telegram-source or Discord collectors;
- HTML scraping or website crawling;
- automatic RSS / Atom feed discovery;
- scheduler infrastructure;
- production 24/7 deployment;
- the final universal data model;
- source-specific retention policy;
- generalized handling of deleted or modified source content;
- an absolute exactly-once Telegram delivery guarantee.

### ACCEPTANCE CRITERIA

Module 4 receives PASS only when all of the following are verified with evidence:

- A configured RSS feed is successfully collected.
- Atom parsing succeeds in at least one deterministic verification case.
- A source item is normalized and persisted in PostgreSQL.
- A normal repeated run does not create a duplicate database row for the same source item.
- Basic filter PASS behavior is verified.
- Basic filter REJECT behavior is verified.
- Basic filter state is persisted independently from Telegram delivery state.
- PASS and REJECT filter outcomes are persisted in PostgreSQL.
- REJECT items are not sent to Telegram.
- PASS items are delivered to the configured Telegram target.
- A normal repeated run after successful persisted delivery does not create a duplicate Telegram notification.
- No absolute exactly-once guarantee is claimed for the crash window between successful sendMessage and delivery-state persistence.
- Initial live-feed verification is safely bounded so uncontrolled historical backlog is not sent to Telegram.
- The Telegram message contains no invented AI, extraction, risk, payment, KYC or scoring data.
- The Открыть button opens the source URL.
- A broken or invalid feed does not create false source-item records in PostgreSQL.
- Secrets are not exposed in source code, tracked Git configuration or diagnostic output.
- Local run and verification procedure is documented.
- Relevant repository documentation is synchronized.
- The logical Module 4 milestone is recorded in Git.
- Final Git working tree state is verified.

### ARCHITECTURE RELATION

D-023 defines the Module 4 RSS Collector scope and acceptance criteria.

It implements only the minimum first working RSS → Database → Filter → Telegram pipeline required by the fixed roadmap.

D-017 remains authoritative for PostgreSQL persistence behavior.
D-021 remains authoritative for the Module 4 basic filtering boundary.
D-022 remains authoritative for RSS / Atom feeds published by official websites.

D-023 does not move Module 5 or Module 6 work forward and does not change the fixed logical pipeline, roadmap, product scope or approved source list.

## D-024 — PYTHON POSTGRESQL ACCESS
Status: FIXED / APPROVED

Module 4 uses Psycopg 3 for direct synchronous PostgreSQL access from Python.

Python dependencies are tracked through requirements.txt.

### IMPLEMENTATION BOUNDARY

- Psycopg 3 is the approved PostgreSQL driver.
- PostgreSQL access remains direct; no ORM is introduced.
- SQLAlchemy is not introduced.
- No migration framework is introduced by this decision.
- The existing PostgreSQL database, schema and migration approach remain unchanged.
- This decision is limited to the Python-to-PostgreSQL access required by the current implementation.
- The exact Psycopg package version will be fixed when the dependency file is created and verified.

### ARCHITECTURE RELATION

D-024 implements the Python database-access mechanism required by D-017 and the Module 4 persistence work defined by D-023.

It does not change the fixed logical pipeline, PostgreSQL architecture, roadmap, product scope or Module 4 acceptance criteria.

## D-025 — MODULE 4 BASIC FILTER RULES
Status: FIXED / APPROVED

Module 4 implements only the minimum deterministic basic-filter slice allowed by D-021.

This is not the full Filter Engine.

### INPUT

The filter evaluates only the normalized RSS / Atom:

- title;
- content_text.

The two fields are combined into one text value and normalized with Unicode casefold() before matching.

### DECISION ORDER

Filtering is deterministic and follows this exact order:

1. If any configured stop-word is present, the result is REJECT.
2. Otherwise, if any configured positive keyword is present, the result is PASS.
3. Otherwise, the result is REJECT.

Stop-words therefore have priority over positive keywords.

### MODULE 4 POSITIVE KEYWORDS

The minimum automatic PASS keywords are:

- freelance
- remote
- tester
- testing
- data annotation
- data labeling

The generic keyword bounty is not included.

The following terms do not automatically produce PASS in Module 4:

- hackathon
- grant
- airdrop
- testnet
- bug bounty

These terms require additional context that belongs outside this minimum Module 4 rule set.

### MODULE 4 STOP-WORDS

The minimum deterministic stop-words are:

- unpaid
- volunteer
- giveaway
- lottery
- raffle

### MATCHING BOUNDARY

Module 4 uses simple deterministic substring matching after casefold().

Module 4 does not introduce:

- regex-based classification;
- stemming or lemmatization;
- scoring;
- semantic matching;
- AI classification;
- category-specific weighting;
- contextual interpretation of conditional terms.

### PERSISTENCE

The filter result is exactly PASS or REJECT.

The result must be persisted to filter_state in the existing rss_source_items PostgreSQL record.

Filtering must not modify telegram_delivery_state.

Telegram delivery is not part of this implementation step.

### LANGUAGE BOUNDARY

This minimum Module 4 filter is not considered a complete multilingual filter implementation.

Full multilingual filtering for the approved EN / RU / UA / DE source languages remains work for the full Filter Engine in Module 6.

### ARCHITECTURE RELATION

D-025 specifies only the minimum concrete rules required to implement the Module 4 basic-filter slice defined by D-021 and D-023.

It does not expand Module 4 into the full Filter Engine, does not move Module 6 forward, and does not change the fixed logical pipeline, roadmap or product scope.

## D-026 — MAIN DEVELOPMENT SESSION HANDOFF WORKFLOW
Status: FIXED / APPROVED

The project uses `SESSION_HANDOFF.md` as the controlled continuity mechanism when moving from one MAIN DEVELOPMENT chat to a new MAIN DEVELOPMENT chat.

This decision affects project continuity and workflow only.

It does not change the approved architecture, roadmap, product scope, module scope, module order or existing technical decisions.

### WHEN SESSION_HANDOFF.md IS USED

`SESSION_HANDOFF.md` is used only when an actual transition to a new MAIN DEVELOPMENT chat is being prepared.

It is not a second `PROJECT_STATE.md` document and is not maintained after every normal development step.

### PRE-HANDOFF SYNCHRONIZATION

Before a MAIN DEVELOPMENT chat is replaced, the current chat must synchronize the repository state first.

The following documents must be updated when required by the work completed since their last verified state:

- `PROJECT_STATE.md`
- `TODO.md`
- `CHANGELOG.md`
- `DECISIONS.md`

Relevant implementation changes and documentation changes must be verified before handoff.

The handoff must record the last verified Git commit and the exact working-tree state.

### REQUIRED HANDOFF CONTENT

`SESSION_HANDOFF.md` must contain these sections:

- `LAST VERIFIED STATE`
- `CURRENT MODULE`
- `CURRENT STEP`
- `COMPLETED`
- `IN PROGRESS`
- `NEXT STEP`
- `BLOCKERS`
- `KNOWN ISSUES`
- `LAST VERIFIED GIT COMMIT`
- `WORKING TREE`
- `IMPORTANT DECISIONS`
- `DO NOT REPEAT`

### NEW MAIN DEVELOPMENT CHAT START RULE

A new MAIN DEVELOPMENT chat must read the mandatory project documentation and the prepared `SESSION_HANDOFF.md`.

It must continue strictly from the recorded `NEXT STEP`.

It must not restart the project, start a new audit, redesign the project, or repeat already verified work unless a demonstrated technical reason requires re-verification.

Any contradiction between the handoff and authoritative repository documentation must be shown explicitly and must not be silently resolved.

### AUTHORITY BOUNDARY

`SESSION_HANDOFF.md` is a continuity document, not a replacement for the project's authoritative documentation.

`PROJECT_STATE.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `ROADMAP.md`, `TODO.md`, `CHANGELOG.md`, `README.md`, `MASTER_PROJECT_INSTRUCTION_v1.0.md`, `SOURCE_OF_TRUTH_HISTORY.md` and `WORK_USAGE_POLICY_v1.0.md` retain their existing roles.

### CURRENT MODULE CONTINUITY

Introducing this workflow does not interrupt or restart the current Module 4 work.

After the continuity mechanism is documented, development resumes from the already verified Module 4 `NEXT STEP`.

## D-027 — MODULE 4 INITIAL LIVE FEED SAFETY
Status: FIXED / APPROVED

The first live RSS / Atom verification in Module 4 must use a deliberately bounded verification mode.

### RULES

1. One verification run operates on exactly one explicitly selected RSS / Atom feed URL from the configured allowlist.
2. The live feed may be retrieved and parsed normally, but no more than one parsed item may enter persistence and downstream processing during that verification run.
3. The selected item is deterministic: the first item in the parser output order.
4. The verification mode does not attempt to infer a newer or more important item using publication timestamps, scoring, AI or source-specific heuristics.
5. Items after the first parser item are not persisted, filtered or queued for Telegram during the bounded verification run.
6. Therefore the verification run cannot create a hidden historical PostgreSQL backlog of unprocessed or undelivered feed items.
7. The selected item follows the already approved Module 4 path:
   NORMALIZE → PostgreSQL persistence → DEDUPLICATE → basic FILTER → Telegram delivery when PASS.
8. If the selected item evaluates to REJECT, the run sends zero Telegram messages.
9. If the selected item evaluates to PASS and is eligible for delivery, the run may send at most one Telegram message.
10. A previously persisted item is handled through the existing deduplication and delivery-state rules; the bounded verification mode does not create a second database row or bypass persisted delivery state.
11. A normal repeated verification run against the same first item must therefore remain subject to the existing deduplication and Telegram delivery-state protections.
12. The existing D-023 crash-window semantics remain unchanged: a failure after successful Telegram sendMessage but before delivery-state persistence may still allow a later duplicate.
13. If the feed is empty, broken, invalid, or yields no parsed item, no source-item record is created and no Telegram message is sent.
14. The bounded verification mechanism introduces no scheduler, queue, ORM, migration framework, additional database, Redis, Kafka, microservice or other infrastructure.
15. Successful bounded verification does not itself authorize unbounded historical-feed processing. Any broader live-processing behavior must be introduced through a later controlled project step.

### RATIONALE

Persisting an entire previously unseen live feed while sending only one item could leave historical PASS + PENDING records that may later be delivered unintentionally.

Restricting the initial verification run to one deterministic parser item bounds both database effects and Telegram effects without adding new infrastructure or changing the approved logical pipeline.

### ARCHITECTURE RELATION

D-027 implements the initial-feed safety requirement already fixed by D-023.

It does not change D-017 PostgreSQL persistence behavior, D-021 basic filtering boundaries, D-022 RSS / Atom source classification, D-023 Module 4 scope, the fixed logical pipeline, roadmap, product scope or approved source list.

D-027 applies only to the first controlled live RSS / Atom verification behavior in Module 4.

## D-028 — MODULE 5 REDDIT COLLECTOR SCOPE AND ACCESS GATE
Status: FIXED / APPROVED

Module 5 implements the Reddit Collector only through an officially permitted Reddit access path.

Module 5 does not assume that unrestricted or legacy public Reddit API access is available.

### ACCESS GATE

1. Before real Reddit collection is implemented, the project must confirm an officially permitted Reddit developer access path for the approved Opportunity Scanner AI use case.
2. Required authentication, credentials and access approval must be obtained and kept outside tracked source control.
3. Module 5 must not bypass Reddit access restrictions.
4. HTML scraping, browser scraping, unofficial mirrors, scraping fallbacks, credential workarounds or other attempts to substitute for unavailable approved Reddit access are not introduced.
5. If an officially permitted access path for the approved use case is unavailable, Module 5 becomes BLOCKED pending a separate project decision.
6. A blocked Reddit access path does not silently change the approved architecture, roadmap, source list or Module 5 position.

### SOURCE BOUNDARY

7. Reddit collection uses explicitly configured Reddit sources such as approved subreddits or other specifically approved Reddit source targets.
8. Uncontrolled platform-wide crawling is not introduced.
9. Source configuration must remain deterministic and reviewable.
10. Any actual request cadence and rate-limit behavior must follow the approved Reddit access mechanism and its applicable limits.
11. No fixed polling interval is assumed before the approved access mechanism and its limits are confirmed.

### MODULE 5 PIPELINE BOUNDARY

12. Module 5 is responsible for the Reddit collector slice required to feed the already approved logical pipeline.
13. The Module 5 collector scope is limited to:
    COLLECT → NORMALIZE → early PostgreSQL persistence → DEDUPLICATE.
14. PostgreSQL behavior continues to follow D-017 as the single cross-cutting persistence layer.
15. Module 5 does not move the full Filter Engine out of Module 6.
16. Module 5 does not implement EXTRACT, AI Analyzer, Anti-Scam Engine or Score Engine.
17. Module 5 does not add a second database, queue, Redis, Kafka, microservice, scheduler framework or other unapproved infrastructure.

### NORMALIZATION AND DEDUPLICATION

18. Reddit source records must be normalized only from data actually supplied by the approved Reddit interface.
19. Minimal normalized fields may include, where available and technically permitted: source identity, Reddit item identifier, title, body/text, canonical Reddit URL, author identifier or name when permitted, publication time, collection time and source/subreddit identity.
20. No unavailable or not-yet-analyzed fields may be invented.
21. Deduplication must prevent a normal repeated collection of the same Reddit item from creating a second source-item record.

### REDDIT DATA COMPLIANCE GATE

22. Before real Reddit User Content is retained beyond the minimum required controlled verification, the project must explicitly define and document a Reddit-specific retention and deletion policy compatible with the approved Reddit use case and applicable Reddit requirements.
23. The retention/deletion policy must define what Reddit data is retained, for how long, and how data that must no longer be retained is removed.
24. Generalized deleted/modified-content handling is not silently implemented beyond the compliance behavior required for the approved Reddit access path.
25. Any compliance requirement discovered during access approval that conflicts with the current persistence design must be surfaced explicitly before implementation proceeds; it must not be silently worked around.

### FUTURE AI COMPLIANCE GATE

26. Module 5 does not send Reddit User Content to the AI Analyzer.
27. Before any later module sends Reddit User Content to an AI provider, the project must separately confirm that this use is permitted by:
    - the approved Reddit use case and applicable Reddit conditions; and
    - the applicable terms and data-use conditions of the selected AI provider.
28. That future confirmation must be documented before Reddit User Content is transmitted to the AI Analyzer.
29. This future AI compliance gate does not expand Module 5 scope and does not block the current Reddit access / collector stage.

### ACCEPTANCE CRITERIA

Module 5 may receive COMPLETED / PASS only when all applicable criteria below are verified with evidence:

- an officially permitted Reddit access path for the approved use case is confirmed;
- required authentication works without exposing secrets;
- explicitly configured Reddit sources are used;
- at least one controlled real Reddit collection succeeds through the approved interface;
- collected Reddit data is normalized into the approved Module 5 representation;
- normalized Reddit source data is persisted through the existing PostgreSQL persistence layer;
- a normal repeated collection of the same Reddit item does not create a duplicate source-item row;
- source configuration and request behavior remain deterministic and bounded;
- broken, unauthorized or invalid Reddit requests fail safely without creating false source-item records;
- Reddit-specific retention and deletion requirements required for real content persistence are documented and verified;
- Module 5 does not implement the full Filter Engine, EXTRACT, AI, Anti-Scam or Score layers;
- no scraping fallback or access-restriction bypass is introduced;
- secrets are not exposed in source code, tracked configuration or diagnostic output;
- local run and verification procedure is documented;
- relevant repository documentation is synchronized;
- the Module 5 milestone is recorded in Git;
- the final Git working tree state is verified clean.

### ARCHITECTURE RELATION

D-028 defines the Module 5 Reddit Collector scope, access gate and compliance boundaries.

Reddit remains an already approved V1 source under D-005.

D-017 remains authoritative for PostgreSQL persistence behavior.

Module 6 remains the approved location of the full Filter Engine.

The future AI compliance gate applies only before Reddit User Content is later transmitted to an AI provider and does not move AI Analyzer work into Module 5.

D-028 does not change the fixed logical pipeline, roadmap, product scope, module order or approved source list.

## D-029 — REDDIT ACCESS DENIAL HANDLING AND ROADMAP CONTINUATION
Status: FIXED / APPROVED

The Reddit Data Access request submitted for Opportunity Scanner AI was not approved by the Reddit Data Team on 2026-09-12.

Under D-028, Module 5 therefore enters:

BLOCKED — DATA ACCESS NOT APPROVED

### BLOCKED MODULE HANDLING

1. Reddit Collector implementation must not begin while officially permitted Reddit data access is not approved.
2. The access denial must not be bypassed through HTML scraping, browser scraping, unofficial mirrors, alternate accounts, credential workarounds or other unapproved access paths.
3. Reddit remains an approved V1 source under D-005. The SOURCE layer, approved architecture and source list are not changed by this denial.
4. Module 5 remains incomplete and BLOCKED. It must not be marked COMPLETED / PASS.
5. Because the Module 5 blocker is external to the other approved modules, project execution may continue to Module 6 — Filter Engine while Module 5 remains blocked.
6. Continuing with Module 6 does not rewrite or reorder the fixed roadmap. It records an execution exception caused by an external access blocker while preserving Module 5 in its approved roadmap position.
7. The project may later return to an official Reddit application or appeal only through an officially permitted path after preparing a more complete compliant use case.
8. Any future Reddit access approval, conditions or compliance requirements must be reviewed before Module 5 implementation resumes.
9. No Reddit User Content may be collected through Module 5 before officially permitted access is confirmed.

### ARCHITECTURE RELATION

D-029 records the verified external Reddit access denial and the approved project-continuation handling required by D-028.

D-029 does not change the fixed logical architecture, approved source list, roadmap definitions, Module 5 scope or D-028 compliance boundaries.

Module 6 remains the approved location of the full Filter Engine.

## D-030 — MODULE 6 FILTER ENGINE SCOPE AND ACCEPTANCE CRITERIA
Status: FIXED / APPROVED

Module 6 extends the existing architectural FILTER component into the full deterministic rule-based Filter Engine.

The Module 4 basic filter defined by D-021 and D-025 is not replaced by a second filtering system. Its verified behavior becomes the baseline that Module 6 generalizes into a reusable FILTER component.

### SCOPE

1. Module 6 implements one reusable deterministic rule-based Filter Engine.
2. The Filter Engine remains before AI in the fixed logical pipeline.
3. Module 6 extends the existing Module 4 filtering behavior rather than introducing a parallel or disposable filter.
4. Filtering must support the approved source languages:
   - EN
   - RU
   - UA
   - DE
5. The Filter Engine must remain usable by the existing RSS pipeline and by later approved source collectors without duplicating filtering logic inside each collector.
6. Module 6 must preserve compatibility with the existing persisted filter states:
   - PASS
   - REJECT
7. Existing verified RSS Telegram delivery behavior must remain unchanged: only items whose persisted filter_state is PASS are eligible for the current RSS Telegram delivery path.
8. Filtering remains deterministic, inexpensive and rule-based before AI analysis.
9. Module 6 does not introduce a second database, queue, Redis, Kafka, microservice, scheduler framework or other new infrastructure.

### IMPLEMENTATION BOUNDARY

10. RSS-specific filtering rules currently located in rss_collector.py may be moved or refactored into the common Filter Engine only through verified incremental changes.
11. Such refactoring must preserve the already verified Module 4 behavior until an explicitly approved Module 6 rule change supersedes it.
12. Module 6 does not implement:
    - EXTRACT;
    - AI Analyzer;
    - Anti-Scam Engine;
    - Risk Engine;
    - Score Engine;
    - source collection logic;
    - Telegram delivery redesign.
13. Module 6 must not silently classify uncertain scam, risk, quality or scoring signals as hard REJECT rules when their correct downstream treatment has not yet been approved.
14. The exact multilingual positive-keyword rules, stop-word rules and the boundary between hard REJECT versus later risk / scoring treatment require a separate explicit project decision before those rules are implemented.
15. No keyword, stop-word, language rule or rejection rule may be invented merely for convenience.

### ACCEPTANCE CRITERIA

Module 6 may receive COMPLETED / PASS only when all applicable criteria below are verified with evidence:

- one reusable Filter Engine is implemented;
- the existing Module 4 basic filter is integrated into that common engine rather than duplicated;
- EN / RU / UA / DE filtering behavior required by the approved Module 6 rules is implemented and tested;
- PASS and REJECT behavior is deterministic and tested;
- filter results continue to persist through the approved PostgreSQL persistence layer;
- existing RSS PASS / REJECT persistence behavior remains correct;
- existing RSS Telegram delivery semantics remain correct after Filter Engine integration;
- REJECT items remain ineligible for the current RSS Telegram delivery path;
- normal repeated processing does not create a second filtering mechanism or duplicate source-item record;
- invalid or unsupported input fails safely;
- no AI, Anti-Scam, Risk or Score logic is introduced into Module 6;
- no unapproved infrastructure or technology is introduced;
- relevant local verification procedure is documented;
- relevant repository documentation is synchronized;
- the Module 6 milestone is recorded in Git;
- the final Git working tree is verified clean.

### ARCHITECTURE RELATION

D-030 defines the Module 6 Filter Engine scope and acceptance criteria.

D-021 remains authoritative for the relationship between the Module 4 basic filtering slice and the full Filter Engine.

D-025 remains the baseline specification for the already verified Module 4 basic-filter behavior until an explicitly approved Module 6 rule decision changes that behavior.

D-017 remains authoritative for PostgreSQL persistence.

D-029 permits Module 6 execution while Module 5 — Reddit Collector remains BLOCKED — DATA ACCESS NOT APPROVED.

D-030 does not change the fixed logical pipeline, approved architecture, roadmap definitions, source list or module order.

## D-031 — MODULE 6 MULTILINGUAL FILTER RULES AND MATCHING SEMANTICS
Status: FIXED / APPROVED

D-031 defines the exact deterministic multilingual rule set and matching semantics required by D-030 before Module 6 Filter Engine implementation begins.

The Filter Engine remains rule-based, inexpensive and deterministic. No AI, NLP or semantic interpretation is introduced.

### INPUT AND NORMALIZATION

1. Filtering evaluates the normalized source-item title and content text available to the FILTER component.
2. Available text fields are combined into one text value before matching.
3. Matching uses Unicode casefold() normalization.
4. No stemming, lemmatization, fuzzy matching, embeddings, semantic similarity, language model inference or other NLP behavior is introduced.
5. Module 6 does not analyze grammatical context, intent, negation or semantic meaning.

### MATCHING SEMANTICS

6. Rules containing whitespace or otherwise defined as phrases use literal casefolded phrase matching.
7. Phrase matching requires the configured phrase to occur as a contiguous casefolded text sequence.
8. Single-word rules must use word / token boundaries and must not match as arbitrary substrings inside a larger token.
9. For single-word matching, a token boundary exists at the start or end of text, or where the adjacent character is not a Unicode letter, digit or underscore.
10. No rule may silently fall back from token-boundary matching to arbitrary substring matching.
11. Stop / hard-REJECT rules are evaluated before positive rules.
12. If any hard-REJECT rule matches, the result is REJECT.
13. Otherwise, if any positive rule matches, the result is PASS.
14. Otherwise, the result is REJECT.

### HARD-REJECT RULES — EN

- unpaid
- volunteer
- giveaway
- lottery
- raffle
- xp only
- points only

### HARD-REJECT RULES — RU

- без оплаты
- неоплачиваем
- волонтёр
- волонтер
- розыгрыш
- лотерея
- только xp
- только баллы

### HARD-REJECT RULES — UA

- без оплати
- неоплачув
- волонтер
- розіграш
- лотерея
- лише xp
- лише бали

### HARD-REJECT RULES — DE

- unbezahlt
- ehrenamt
- gewinnspiel
- lotterie
- verlosung
- nur xp
- nur punkte

### POSITIVE RULES — EN

- freelance
- freelance task
- remote work
- remote job
- part-time remote
- entry level
- no experience
- hiring now
- contributors wanted
- tester
- testing
- qa tester
- bug testing
- usability testing
- paid beta testing
- beta tester
- data annotation
- data labeling
- ai rater
- ai evaluator
- llm trainer
- model reviewer
- search evaluator
- data collection
- paid testnet
- web3 task

### POSITIVE RULES — RU

- фриланс
- удалённая работа
- удаленная работа
- удалённая подработка
- удаленная подработка
- без опыта
- тестировщик
- тестирование
- qa тестировщик
- поиск багов
- юзабилити тестирование
- платное бета-тестирование
- разметка данных
- оценщик ии
- оценщик ai
- тренер llm
- проверка модели
- проверка ответов ии
- сбор данных
- платный тестнет
- оплачиваемое web3 задание

### POSITIVE RULES — UA

- фриланс
- віддалена робота
- віддалена підробітка
- без досвіду
- тестувальник
- тестування
- qa тестувальник
- пошук багів
- юзабіліті тестування
- платне бета-тестування
- розмітка даних
- оцінювач ші
- оцінювач ai
- тренер llm
- перевірка моделі
- перевірка відповідей ші
- збір даних
- платний тестнет
- оплачуване web3 завдання

### POSITIVE RULES — DE

- freelance
- freiberuflich
- remote arbeit
- remote-arbeit
- homeoffice
- teilzeit remote
- berufseinsteiger
- ohne erfahrung
- tester
- softwaretester
- testing
- qa tester
- bug testing
- usability testing
- bezahlter betatest
- datenannotation
- datenlabeling
- datenerfassung
- ki-bewertung
- ai evaluator
- llm-trainer
- modellbewertung
- bezahltes testnet
- bezahlte web3-aufgabe

### DOWNSTREAM BOUNDARY

15. The following signals are not hard-REJECT rules in Module 6 merely because the term is present:

- contest
- leaderboard
- top winners
- ambassador
- staking
- deposit
- trading volume
- mandatory purchase
- prepayment
- seed phrase
- phishing
- wallet connection
- smart contract
- KYC
- unknown token

16. These signals may require later EXTRACT, Anti-Scam, Risk or Score handling according to the applicable future module decisions.
17. Excluding these terms from Module 6 hard-REJECT rules does not classify them as safe.
18. Module 6 must not implement Anti-Scam, Risk or Score behavior indirectly through filter rules.

### MINIMUM PAYOUT BOUNDARY

19. The approved minimum payout requirement of $5 is not implemented as a Module 6 text-filter rule.
20. Payment amount handling requires extracted payment information and therefore remains a downstream concern after FILTER.
21. Module 6 must not guess or infer payout amounts from incomplete text merely to enforce the minimum payout requirement.

### REQUIRED VERIFICATION

22. Module 6 tests must verify hard-REJECT priority over positive matches.
23. Tests must verify case-insensitive behavior through casefold().
24. Tests must verify literal phrase matching.
25. Tests must verify that single-word rules match complete tokens.
26. Tests must verify that a single-word rule does not match when it appears only as part of a larger token.
27. Tests must cover approved EN / RU / UA / DE rules.
28. Tests must verify default REJECT when neither hard-REJECT nor positive rules match.
29. No test may rely on AI, NLP, context understanding or negation analysis.

### ARCHITECTURE RELATION

D-031 supplies the exact multilingual rule set and matching semantics required by D-030.

D-021 remains authoritative that Module 6 extends the same architectural FILTER component first implemented in Module 4.

D-025 remains the verified Module 4 baseline whose behavior is superseded only where D-031 explicitly defines the approved Module 6 rules and matching semantics.

D-031 does not change the fixed logical pipeline, architecture, roadmap definitions, source list, Module 6 scope or downstream module responsibilities.

## D-032 — MODULE 7 X COLLECTOR SCOPE, ACCESS, COST AND COMPLIANCE GATE

Status: FIXED / APPROVED

1. Module 7 implements only the X / Twitter Collector as the existing `COLLECT → NORMALIZE → early PostgreSQL persistence → DEDUPLICATE` path, with saved records passed to the already implemented common Filter Engine.

2. Only an officially permitted X API access path may be used. HTML/browser scraping, unofficial mirrors, credential workarounds and restriction bypasses are prohibited.

3. The initial access path is the official X API v2 Recent Search endpoint (`/2/tweets/search/recent`) if it is available for the project developer account and approved use case at implementation time.

4. Before real X API collection is implemented, valid X developer credentials must be obtained. Credentials and secrets must remain outside tracked Git files.

5. Before any paid live verification, an explicit maximum verification budget must be approved.

6. The live-verification cost boundary must limit both:
   - the maximum number of API requests; and
   - the maximum number of billable returned Posts / resources.

7. X billing deduplication behavior, including any 24-hour billing deduplication, must not be treated as a guaranteed budget-control mechanism.

8. The historical 10–15 minute collection interval is not automatically fixed as the Module 7 implementation interval. The actual polling interval must be decided only after evaluating current API pricing, returned-resource cost, applicable API limits and permitted usage conditions.

9. The first live API verification must be strictly bounded by both request count and maximum returned Posts / resources.

10. X search queries and source targets must be explicitly configured and deterministic. Module 7 must not perform arbitrary global X collection.

11. Each collected X item must have a stable source identity / deduplication identity so that normal repeated collection of the same Post does not create a duplicate source-item record.

12. Collected X records must use the common Module 6 Filter Engine. No parallel X-specific Filter Engine may be introduced.

13. Module 7 does not implement AI Analyzer, Anti-Scam Engine, Risk, Score, Telegram Sources, Discord Collector or scheduler infrastructure.

14. An X-specific content compliance policy must be explicitly defined and approved before the first real X Content is persistently stored.

15. Before approval of the X-specific content compliance policy:
   - fixtures and mocked X data may be used;
   - bounded official API verification may be performed only without permanent persistence of real X Content.

16. The X-specific content compliance policy must define the required handling of retained X Content, including synchronization or removal behavior for deleted or modified source content as required by the applicable X developer requirements.

17. If X requirements for retained, deleted or modified content conflict with the current PostgreSQL persistence design, the conflict must be surfaced for a separate explicit project decision and must not be silently worked around.

18. Module 7 receives PASS only when all of the following are verified with evidence:
   - deterministic collector behavior;
   - officially permitted X API access;
   - bounded live API verification;
   - approved request-count and billable-resource cost boundaries;
   - X-specific content compliance policy approved before any persisted live X Content;
   - PostgreSQL persistence behavior consistent with the approved X compliance policy;
   - stable source identity and deduplication behavior;
   - integration with the common Filter Engine;
   - invalid, unauthorized or broken requests fail safely;
   - secrets are not exposed in tracked Git files or diagnostic output;
   - relevant repository documentation is synchronized;
   - the Module 7 milestone is recorded in Git;
   - the final Git working tree state is verified clean.

19. D-032 does not change the approved architecture, source list or roadmap order.

## D-033 — SOURCE ACCESS PRECHECK

Status: FIXED / APPROVED

### PURPOSE

1. A separate SOURCE ACCESS PRECHECK must be completed before further collector implementation.

2. The SOURCE ACCESS PRECHECK does not change:
   - the approved architecture;
   - the roadmap;
   - module order;
   - the approved V1 source list.

3. The SOURCE ACCESS PRECHECK is not collector implementation.

### SOURCES

4. The precheck covers exactly the approved V1 sources:
   - Reddit;
   - X / Twitter;
   - Discord;
   - Telegram;
   - RSS / Atom.

### ACCESS BOUNDARY

5. Only officially permitted APIs, feeds and access paths may be used.

6. The following are prohibited:
   - HTML scraping;
   - browser scraping;
   - unofficial mirrors;
   - credential workarounds;
   - access-restriction bypasses;
   - other unapproved substitute access paths.

7. Paid API access, paid subscriptions, paid credits or other paid source access must not be purchased or activated without separate explicit user approval.

8. Credentials, tokens and secrets must not be stored in tracked Git files or exposed in diagnostic output.

### FORMAL STATUS CRITERIA

9. Each source must receive exactly one of the following statuses:

#### AVAILABLE

A source is `AVAILABLE` only when all of the following are true:

- an official permitted access path exists for the approved Opportunity Scanner AI use case;
- no unresolved external access denial or mandatory approval gate blocks use;
- no unresolved user approval is required before the access path can be used for controlled implementation;
- required technical prerequisites are known and do not prevent compliant collector implementation;
- required compliance obligations are known sufficiently to proceed safely;
- no prohibited workaround is required.

#### AVAILABLE WITH LIMITATIONS

A source is `AVAILABLE WITH LIMITATIONS` when an official permitted access path exists and compliant collector implementation can proceed, but one or more material limitations apply, including for example:

- rate limits;
- quotas;
- free-tier limits;
- paid-use boundaries already separately approved;
- restricted endpoint coverage;
- restricted source scope;
- permission constraints;
- retention / deletion obligations;
- polling or delivery limitations;
- other documented technical or compliance constraints.

The limitations must be explicitly documented and must not make compliant implementation impossible.

#### BLOCKED

A source is `BLOCKED` when any of the following is true:

- the required official access path is unavailable for the approved use case;
- required access has been explicitly denied;
- applicable official rules prohibit the intended use;
- mandatory technical or compliance conditions make the approved collector implementation impossible without changing project decisions;
- proceeding would require scraping, unofficial access, restriction bypasses or another prohibited workaround.

A BLOCKED status does not automatically remove the source from the architecture, roadmap or approved V1 source list.

#### UNKNOWN — REQUIRES APPROVAL

A source is `UNKNOWN — REQUIRES APPROVAL` when a final availability classification cannot yet be established because an unresolved approval or user-controlled prerequisite must be completed first, including for example:

- creating or authorizing a developer application;
- submitting an official access request;
- granting required permissions;
- approving a paid tier, credits or cost exposure;
- accepting a source-specific access condition;
- completing another explicit approval-dependent step required before availability can be verified.

No paid action or irreversible approval-dependent action may be taken automatically.

### REQUIRED CHECK FOR EACH SOURCE

10. For every source, the precheck must determine and document:

- official access path;
- whether a developer account is required;
- whether an application or external approval is required;
- whether credentials are required;
- whether a paid access / cost gate exists;
- technical limitations relevant to the approved use case;
- retention / deletion / content-compliance requirements relevant before persistence;
- whether collector implementation may safely proceed;
- final formal status.

### DATE AND EVIDENCE REQUIREMENT

11. Every source result must include a verification date in `YYYY-MM-DD` format.

12. Every source result must include evidence sufficient to support and later audit the classification.

13. Evidence must use authoritative sources wherever available, including as applicable:

- official API documentation;
- official developer policies;
- official pricing / rate-limit documentation;
- official developer-console or account-state evidence;
- official approval / denial correspondence;
- deterministic local verification output from an officially permitted access path.

14. Evidence must identify what fact it supports. A status must not be assigned from unsupported assumptions.

15. Secrets, tokens, credentials and sensitive authentication values must never be included in stored evidence.

16. Because source access conditions can change, the recorded verification date is part of the evidence and must not be omitted.

### SOURCE-SPECIFIC BASELINE

17. Reddit retains the already verified status `BLOCKED — DATA ACCESS NOT APPROVED` unless new official evidence changes that state.

18. A source that is blocked or approval-dependent is not silently removed, reordered or replaced. Any roadmap consequence requires a separate explicit project decision.

### COMPLETION CRITERIA

19. SOURCE ACCESS PRECHECK is complete only when all five approved V1 sources have:

- a formal status;
- a verification date;
- documented evidence;
- documented limitations or blockers where applicable;
- a clear statement whether collector implementation may proceed.

20. Relevant repository documentation must be synchronized after the five-source precheck is complete.

21. Collector implementation must not resume until the SOURCE ACCESS PRECHECK is completed and its results are verified.

22. D-033 does not change the approved architecture, roadmap, module order or V1 source list.

## D-034 — X API BUDGET AND PAID ACCESS POLICY

Status: FIXED / APPROVED

### PURPOSE

1. D-034 defines the financial, budget-control and paid-access safety policy for official X API Pay Per Use use in Module 7.

2. D-034 extends the cost-control requirements already established by D-032. It does not authorize collector implementation by itself.

### OFFICIAL PAID ACCESS

3. Use of the official X API Pay Per Use access path for Module 7 is approved in principle.

4. This approval does NOT by itself authorize:
   - purchasing credits;
   - connecting the X App to the Pay Per Use Project;
   - enabling Auto-recharge;
   - making live paid API requests;
   - starting X Collector implementation.

5. Any activation step remains prohibited until the remaining D-034 activation gates are explicitly satisfied.

### INITIAL PERSONAL BUDGET

6. The maximum initial personal-funded X API budget is USD $15 total.

7. The user funds this initial maximum $15 allocation personally one time only.

8. The project must never automatically increase this personal-funded budget.

9. Auto-recharge must remain OFF.

10. No automatic credit purchase, automatic top-up or automatic budget increase is permitted.

### FUTURE FUNDING

11. After the initially approved $15 has been consumed, additional X API funding may be authorized only from actual realized income obtained from opportunities found by Opportunity Scanner AI.

12. Every later top-up requires separate explicit user approval.

13. The system must not infer that future funds are available and must not automatically authorize a later top-up.

14. If sufficient realized Opportunity Scanner AI income is not available or has not been explicitly approved for reuse, paid X collection must stop rather than consume additional personal funds.

### HARD LIVE-ACCESS BOUNDARIES

15. Before any Pay Per Use activation or live paid API request, one explicit bounded live-access envelope must be separately defined and approved.

16. That envelope must define all of the following:
   - maximum spend;
   - maximum number of API requests;
   - maximum number of billable returned Posts / resources;
   - deterministic safe-stop conditions.

17. For the initial personal-funded period, maximum spend must never exceed the approved $15 total personal-funded budget.

18. Exact numerical values for:
   - maximum API requests; and
   - maximum billable returned Posts / resources

   are NOT fixed by D-034 and must not be invented.

19. Those numerical limits must be decided from verified current X pricing, billing behavior, endpoint behavior and applicable API limits before paid activation.

20. Until those exact numerical limits are separately approved, the X App must remain disconnected from Pay Per Use and no paid live request may be made.

### SAFE STOP

21. Paid collection must fail safe when any approved spend, request-count or billable-resource boundary is reached or would be exceeded.

22. If remaining cost exposure cannot be bounded sufficiently before the next paid operation, the operation must not proceed.

23. Exhausting an approved budget must stop paid collection. It must not trigger automatic recharge, fallback personal spending or an unapproved paid access path.

24. X billing deduplication behavior, including any time-based billing deduplication, must not be relied upon as a budget-control guarantee.

### QUERY EFFICIENCY

25. X search queries must be explicitly configured, deterministic and intentionally narrow.

26. Queries must target realistic paid earning opportunities relevant to the approved Opportunity Scanner AI categories rather than collect a broad general X stream.

27. Paid API budget must not be consumed merely to maximize collected Post volume.

28. X effectiveness is evaluated primarily by useful actionable opportunities surviving the complete approved pipeline, not by raw Posts collected.

### RELATION TO OTHER DECISIONS

29. D-032 remains authoritative for Module 7 collector scope, official API access, stable source identity, bounded live verification and X-specific content-compliance requirements.

30. D-033 remains authoritative for the SOURCE ACCESS PRECHECK evidence and formal-status model.

31. D-034 does not change the approved architecture, roadmap, module order or V1 source list.

32. Module 7 remains PRE-IMPLEMENTATION / ACCESS GATED until the remaining activation gates are separately satisfied.


## D-035 — QUALITY / NOISE / DEDUP POLICY

Status: FIXED / APPROVED

### PURPOSE

1. D-035 defines a cross-module product policy for opportunity quality, noise reduction, deduplication and production Telegram eligibility.

2. The governing objective is:

`MINIMUM NOISE → MAXIMUM ACTIONABLE OPPORTUNITIES`

3. D-035 applies across approved sources and downstream processing. It does not introduce a second pipeline or a source-specific replacement for existing common components.

### SOURCE IDENTITY AND DEDUPLICATION

4. Every collected source item must use stable source identity and deterministic deduplication wherever the source provides sufficient stable identity.

5. Normal repeated collection of the same source item must not create a new logical source item or a new opportunity.

6. Obvious deterministic duplicates must be rejected or merged as early as reasonably possible rather than consuming unnecessary downstream processing.

7. The system must prevent the same logical opportunity from being repeatedly delivered merely because it was collected more than once.

8. Opportunity-level duplicate handling across equivalent source records must be deterministic before production Telegram delivery.

9. The exact canonical cross-source opportunity identity algorithm is not invented by D-035. It must be specified and tested when the relevant implementation step requires it.

### FILTER BEFORE AI

10. The existing deterministic Filter remains before AI in the fixed logical pipeline.

11. Cheap deterministic filtering must reject clearly irrelevant or low-value candidates before expensive AI processing.

12. AI must be invoked only for candidates that pass the applicable deterministic pre-AI filtering rules.

13. D-035 does not create a parallel source-specific Filter Engine.

### REPEATED TELEGRAM DELIVERY

14. An opportunity already delivered to the production Telegram flow must not be delivered again merely because the same source item or equivalent opportunity is collected again.

15. Re-delivery may occur only when a separately specified deterministic rule establishes that the opportunity has changed substantially enough to justify a new notification.

16. D-035 does not invent the exact definition of `substantial change`.

17. That definition must be formally specified and tested before substantial-change re-delivery behavior is enabled.

### EXPIRED / CLOSED OPPORTUNITIES

18. Opportunities determined to be expired or closed must not return to the normal production Telegram opportunity flow.

19. The exact deterministic rules for determining expired / closed state must be defined in the relevant implementation stage and must not be guessed by the collector or AI.

### PRODUCTION TELEGRAM QUALITY GATE

20. Production Telegram opportunity delivery must contain only opportunities that have passed all applicable approved quality, risk and scoring gates required by the completed end-to-end pipeline.

21. High raw collection volume is not a success metric by itself.

22. Product quality is measured by useful actionable opportunities reaching the user with minimum duplicate and irrelevant noise.

### EXISTING DEVELOPMENT PIPELINE BOUNDARY

23. Existing Module 4 controlled RSS → Filter → Telegram verification remains valid development and integration evidence.

24. The preliminary Module 4 Telegram delivery path must not be interpreted as the final production eligibility policy after AI, Risk and Score modules are implemented.

25. D-035 therefore does not invalidate completed Module 4 verification and does not retroactively change its acceptance result.

### ARCHITECTURE BOUNDARY

26. D-035 reinforces the existing fixed pipeline ordering:

`SOURCE → COLLECT → NORMALIZE → DEDUPLICATE → FILTER → EXTRACT → AI → RISK → SCORE → DATABASE → TELEGRAM`

27. D-035 does not change the approved architecture, roadmap, source list or module order.

28. Exact future scoring thresholds, risk thresholds, substantial-change semantics, expiry rules and canonical cross-source opportunity identity remain subject to their relevant formal implementation decisions and must not be invented prematurely.

## D-036 — X BOUNDED LIVE-ACCESS ENVELOPE

Status: FIXED / APPROVED

### PURPOSE

1. D-036 defines the first bounded live-access envelope required by D-034 before any controlled paid X API verification.

2. D-036 does not by itself authorize X Collector implementation or production polling.

### APPROVED LIVE-ACCESS ENVELOPE

3. Maximum spend for the first controlled live-verification envelope:

`USD $1.00`

4. Maximum number of paid X API requests:

`20`

5. Maximum `max_results` per Recent Search request:

`10 Posts`

6. Maximum billable returned Posts / resources for this envelope:

`200`

7. The approved endpoint scope for this first controlled verification is limited to the official X API v2 Recent Search path defined by D-032.

8. Additional User lookups, expansions, unrelated endpoints or broad data collection are not authorized by this envelope.

### HARD SAFE-STOP CONDITIONS

9. Paid X activity must stop before or when any one of the following limits is reached or would be exceeded:

- USD $1.00 maximum spend;
- 20 paid API requests;
- 200 billable returned Posts / resources.

10. Paid activity must also stop immediately if:

- actual pricing differs from the verified pricing basis used to define this envelope;
- an unexpected billable resource or charge appears;
- remaining cost exposure cannot be bounded before the next request;
- usage / billing information is inconsistent or cannot be verified;
- the request would require an endpoint or paid resource outside the approved envelope.

11. Billing deduplication or any soft billing guarantee must not be relied upon to remain within budget.

### FUNDING AND BILLING SAFETY

12. Auto-recharge must remain OFF.

13. This envelope authorizes at most USD $1.00 of the D-034 maximum initial personal-funded USD $15 allocation.

14. The remaining USD $14 of the D-034 personal-funded ceiling is not automatically authorized for live use by D-036.

15. No automatic top-up, automatic budget increase or additional personal funding is permitted.

### ACTIVATION BOUNDARY

16. D-036 approves the numerical bounded live-access envelope required by D-034.

17. D-036 does NOT by itself authorize:

- purchasing credits;
- connecting the X App to the Pay Per Use Project;
- enabling Auto-recharge;
- generating or exposing credentials;
- making a paid live API request;
- starting X Collector implementation.

18. Any actual activation action remains a separate controlled development step and requires verification before proceeding.

### RELATION TO EXISTING DECISIONS

19. D-032 remains authoritative for Module 7 scope, official X API access and content-compliance requirements.

20. D-033 remains authoritative for the formal SOURCE ACCESS PRECHECK status model.

21. D-034 remains authoritative for the total personal-funded ceiling, future funding rules and paid-access safety policy.

22. D-035 remains authoritative for quality, noise reduction and deduplication.

23. D-036 does not change the approved architecture, roadmap, source list or module order.

24. Module 7 remains PRE-IMPLEMENTATION / ACCESS GATED. X Collector implementation has not started.

## D-037 — X MINIMUM CREDIT PURCHASE AUTHORIZATION

Status: FIXED / APPROVED

### PURPOSE

1. D-037 authorizes the minimum prepaid X API credit purchase required by the currently verified X Developer Console purchase flow.

2. The verified console does not accept a USD $1.00 credit purchase and reports a minimum purchase amount of USD $5.00.

3. D-037 resolves only the credit-purchase amount mismatch discovered during controlled activation-readiness verification.

### PURCHASE AUTHORIZATION

4. A one-time prepaid X API credit purchase of:

`USD $5.00`

is explicitly approved.

5. This USD $5.00 purchase remains within the D-034 maximum initial personal-funded ceiling of USD $15.

6. This purchase authorization does not increase the D-034 personal-funded ceiling.

### LIVE-SPEND BOUNDARY

7. Purchasing USD $5.00 of prepaid credits does NOT authorize spending the full USD $5.00.

8. The maximum authorized spend for the current bounded live verification remains:

`USD $1.00`

as fixed by D-036.

9. The X Billing Cycle Spending Limit must remain set to:

`USD $1.00`

before any paid live API request.

10. The remaining unused prepaid credit balance is not authorized for further live spend without separate explicit approval.

11. Credit availability must never be interpreted as permission to spend beyond the currently approved live-access envelope.

### BILLING SAFETY

12. Auto-recharge must remain OFF.

13. Automatic credit purchase, automatic top-up and automatic budget increase remain prohibited.

14. D-036 request and billable-resource limits remain unchanged:

- maximum 20 paid API requests;
- maximum 10 Posts per Recent Search request;
- maximum 200 billable returned Posts / resources;
- all D-036 hard safe-stop conditions remain mandatory.

### ACTIVATION BOUNDARY

15. D-037 authorizes only the one-time USD $5.00 prepaid credit purchase.

16. D-037 does NOT by itself authorize:

- connecting the X App to the Pay Per Use Project;
- generating or exposing credentials;
- making a paid live API request;
- starting X Collector implementation;
- increasing the Billing Cycle Spending Limit above USD $1.00;
- spending unused credits beyond the D-036 live-verification envelope.

17. Project connection, credential handling and the first paid live request remain separate controlled development steps and require their own verification before execution.

### RELATION TO EXISTING DECISIONS

18. D-034 remains authoritative for the total personal-funded ceiling and future funding rules.

19. D-036 remains authoritative for the current bounded live-access spend, request, resource and safe-stop limits.

20. D-037 changes only the permitted prepaid credit purchase amount required by the verified X purchase interface.

21. D-037 does not change the approved architecture, roadmap, source list or module order.

22. Module 7 remains PRE-IMPLEMENTATION / ACCESS GATED. X Collector implementation has not started.

## D-038 — X DEVELOPMENT PROJECT ACCESS AUTHORIZATION

Status: FIXED / APPROVED

### PURPOSE

1. D-038 authorizes connecting the existing X App to the existing `Default Project — Pay Per Use` only in the `Development` environment.

2. The purpose of this connection is limited to controlled bounded live-verification readiness under D-036.

### APPROVED CONNECTION

3. The approved Project Access action is:

`Connect · Development`

4. `Connect · Staging` is not authorized.

5. `Connect · Production` is not authorized.

6. No new X Project is authorized or required by D-038.

### BOUNDARIES

7. D-038 authorizes only the Development Project Access connection.

8. D-038 does NOT by itself authorize:

- generating or exposing credentials;
- making any paid API request;
- starting X Collector implementation;
- production polling;
- increasing Billing Cycle Cap;
- enabling Auto Recharge;
- spending beyond the D-036 live-verification envelope.

9. The D-036 limits remain unchanged:

- maximum USD $1.00 live spend;
- maximum 20 paid API requests;
- maximum 10 Posts per Recent Search request;
- maximum 200 billable returned Posts / resources;
- all D-036 hard safe-stop conditions remain mandatory.

10. The D-037 prepaid credit purchase does not expand these live-use permissions.

### CURRENT BILLING SAFETY STATE

11. Before Development connection, the verified X Developer Console state is:

- Remaining Balance: USD $5.00;
- Billing Cycle Cap: USD $1.00;
- Auto Recharge: OFF;
- Current Spend: USD $0.00.

12. Those billing safety controls must remain unchanged by the Project Access connection.

### NEXT AUTHORIZATION BOUNDARY

13. After Development connection, Project Access state must be verified before any further action.

14. Credential handling and the first paid live API request remain separate controlled development steps requiring explicit verification and authorization.

15. X Collector implementation remains not started.

### RELATION TO EXISTING DECISIONS

16. D-032 remains authoritative for Module 7 scope and official X API access.

17. D-034 remains authoritative for total personal-funded budget and funding safety.

18. D-036 remains authoritative for bounded live-access spend, request, resource and safe-stop limits.

19. D-037 remains authoritative for the prepaid credit purchase authorization and unused-credit boundary.

20. D-038 does not change the approved architecture, roadmap, source list or module order.

21. Module 7 remains PRE-IMPLEMENTATION / ACCESS GATED.

## D-039 — X BEARER TOKEN GENERATION AND LOCAL SECRET HANDLING

Status: FIXED / APPROVED

Date: 2026-09-22

### PURPOSE

1. D-039 authorizes generation of the X App Bearer Token only for the controlled credential-readiness step of Module 7.

2. The approved environment variable name is:

`X_BEARER_TOKEN`

3. The Bearer Token is authorized only for local secret storage in the repository-root `.env` file.

### VERIFIED SECRET-STORAGE READINESS

4. The repository-root `.env` is ignored by Git.

5. `.env` is not tracked by Git.

6. `.env.example` is tracked and contains only the safe placeholder:

`X_BEARER_TOKEN=REPLACE_WITH_LOCAL_X_BEARER_TOKEN`

7. The local `.env` contains exactly one `X_BEARER_TOKEN` key and its value remains empty before token generation.

### SECRET HANDLING BOUNDARIES

8. The generated Bearer Token must not be:

- sent in ChatGPT or any other chat;
- committed to Git;
- added to tracked project files;
- written into project documentation;
- written into logs;
- exposed in screenshots;
- copied into command output submitted for verification.

9. After generation, the token may be copied only into the local `.env` value for `X_BEARER_TOKEN`.

10. The token value itself must never be used as verification evidence. Verification must use only non-secret state such as key presence / non-empty status.

### AUTHORIZATION BOUNDARY

11. D-039 authorizes only Bearer Token generation and local storage.

12. D-039 does NOT authorize:

- any X API request;
- any paid API request;
- any Recent Search request;
- starting X Collector implementation;
- production polling;
- generating Access Token credentials;
- configuring User Authentication;
- exposing or rotating Consumer Key / Consumer Secret;
- connecting Staging or Production;
- increasing Billing Cycle Cap;
- enabling Auto Recharge;
- spending any X API credits.

13. The first bounded paid live API request remains a separate step requiring separate explicit authorization.

14. X Collector implementation remains not started.

### RELATION TO EXISTING DECISIONS

15. D-032 remains authoritative for Module 7 scope and official X API access.

16. D-034 remains authoritative for the total personal-funded budget and funding safety.

17. D-036 remains authoritative for the bounded live-verification envelope and all hard safe-stop conditions.

18. D-037 remains authoritative for prepaid-credit authorization and unused-credit restrictions.

19. D-038 remains authoritative for Development-only Project Access.

20. D-039 does not change the approved architecture, roadmap, source list or module order.

21. Module 7 remains SCOPE APPROVED / PRE-IMPLEMENTATION / ACCESS GATED.

### EXECUTION CLARIFICATION — 2026-09-23

22. X Developer Console verification showed a UI inconsistency: the Bearer Token row displays `Generate`, but activating that control opens a `Regenerate Bearer Token` confirmation dialog.

23. The user explicitly approves, within D-039, regeneration of the existing X Bearer Token through the verified Console flow:

`Generate → Regenerate`

24. The previously existing Bearer Token may be invalidated by this regeneration.

25. The regenerated Bearer Token remains authorized only for local storage in the Git-ignored `.env` as `X_BEARER_TOKEN`.

26. This clarification does NOT authorize any X API request, paid API request, Recent Search request, X Collector implementation, Access Token generation, User Authentication configuration, Staging / Production connection, Billing Cycle Cap increase, Auto Recharge, or credit spend.

### EXECUTION RECORD — 2026-09-23

27. The authorized `Generate → Regenerate` Bearer Token action was executed successfully in X Developer Console.

28. The regenerated Bearer Token was stored only in the repository-root Git-ignored `.env` under the approved variable name `X_BEARER_TOKEN`.

29. Non-secret verification confirmed that the locally stored value exactly matched the copied regenerated token: `TOKEN_MATCH=True`.

30. The clipboard containing the regenerated token was cleared after successful local storage and verification.

31. Git verification after credential storage showed `## main...origin/main`, confirming that the local `.env` remained untracked and no credential-bearing file was added to Git.

32. No X API request, paid API request or Recent Search request was executed during D-039.

33. X Collector implementation remains not started. The first bounded live X API verification remains a separate step requiring separate explicit authorization under the existing D-036 envelope.

## D-040 — X FIRST BOUNDED LIVE API VERIFICATION AUTHORIZATION

Status: FIXED / APPROVED

Date: 2026-09-23

### PURPOSE

1. D-040 authorizes exactly one controlled live verification request to the official X API v2 Recent Search endpoint.

2. The sole authorized endpoint is:

`GET https://api.x.com/2/tweets/search/recent`

3. Authentication is authorized only through the locally stored Git-ignored `.env` value:

`X_BEARER_TOKEN`

### AUTHORIZED REQUEST ENVELOPE

4. Exactly one API request is authorized.

5. The request must use:

`max_results=10`

6. The approved deterministic query is:

`("paid testing" OR "user testing") lang:en has:links -is:retweet`

7. Pagination is prohibited. `next_token` must not be followed.

8. No expansions, User lookups, additional endpoints or unrelated API calls are authorized.

### DATA HANDLING

9. Returned X Post content must not be persisted to PostgreSQL, files or any other project storage during this verification.

10. Returned Post content must not be written to logs.

11. Verification output is restricted to non-content operational evidence only:

- HTTP status;
- `meta.result_count`;
- actual number of returned Posts.

### BILLING SAFETY

12. Before the authorized request is executed, the following X billing state must be separately verified:

- Remaining Balance: USD $5.00;
- Billing Cycle Cap: USD $1.00;
- Auto Recharge: OFF;
- Current Spend: USD $0.00.

13. After the authorized request, billing / usage state must be checked again before any further X action.

14. Any pricing mismatch, unexpected billable resource or charge, inability to bound exposure, unverifiable usage / billing state, or operation outside the authorized endpoint / resource scope requires immediate STOP.

### RELATION TO D-036

15. D-036 remains fully authoritative and unchanged:

- maximum live spend: USD $1.00;
- maximum paid API requests: 20;
- maximum `max_results` per Recent Search request: 10 Posts;
- maximum billable returned Posts / resources: 200.

16. D-040 is intentionally narrower than D-036 and authorizes only one request returning at most 10 Posts.

17. D-040 does not authorize a second request, pagination, use of unused prepaid credits beyond this verification, Billing Cycle Cap increase or Auto Recharge.

### IMPLEMENTATION BOUNDARY

18. D-040 does not start X Collector implementation.

19. D-040 does not authorize production polling, Staging / Production connection, Access Token generation or User Authentication configuration.

20. Any second live X API request or transition into X Collector implementation requires a separate explicit project step and authorization.

### EXECUTION RECORD — 2026-09-23

21. The required pre-request billing verification was completed successfully before the authorized request:

- Remaining Balance: USD $5.00;
- Billing Cycle Cap: USD $1.00;
- Auto Recharge: OFF;
- Current Spend: USD $0.00.

22. The single API request authorized by D-040 was executed exactly once against:

`GET https://api.x.com/2/tweets/search/recent`

23. The request used the approved controls:

- `max_results=10`;
- query: `("paid testing" OR "user testing") lang:en has:links -is:retweet`;
- no pagination;
- no expansions;
- no User lookup;
- no additional endpoint call.

24. The live verification result was:

- HTTP status: `200`;
- `meta.result_count=10`;
- actual returned Post count: `10`.

25. Returned X Post content was not persisted to PostgreSQL, files or project logs. Verification output was restricted to the approved non-content operational evidence.

26. Secret-bearing PowerShell variables used during the request were subsequently cleared and non-secret verification confirmed:

`SECRET_VARS_CLEARED=True`

27. Required post-request billing verification was completed successfully:

- Remaining Balance: USD $4.95;
- Billing Cycle Cap: USD $1.00;
- Auto Recharge: OFF;
- Current Spend: USD $0.05.

28. The observed spend attributable to this single bounded verification was USD $0.05. No broader X pricing or billing model is inferred from this one request.

29. The D-040 authorization is now exhausted. No second X API request is authorized under D-040.

30. X Collector implementation remains not started. Any further live X API request or transition toward collector implementation requires a separate explicit project step and authorization.

## D-041 — X CONTENT COMPLIANCE AND PERSISTENCE POLICY

Status: FIXED / APPROVED

Date: 2026-09-25

### SCOPE AND AUTHORITY

1. D-041 defines the mandatory content-compliance boundaries for persistent real X Content in Module 7.

2. D-032 remains authoritative for Module 7 scope and requires an approved X-specific content-compliance policy before the first persistent storage of real X Content.

### OFFICIAL-SOURCE BOUNDARY

3. X Content may be persistently processed or stored only when obtained through an officially permitted X API path and only for the approved Opportunity Scanner AI use case.

4. HTML/browser scraping, unofficial mirrors, credential workarounds and access-restriction bypasses remain prohibited.

### DATA-MINIMIZATION BOUNDARY

5. Module 7 is not a raw X archive.

6. Only the minimum X data actually required for the approved Opportunity Scanner processing may be persistently retained.

7. Bulk or speculative archival of X Content for possible future use is prohibited.

### PERSISTENCE ARCHITECTURE

8. PostgreSQL remains the single cross-cutting persistence layer under D-017.

9. D-041 does not authorize or introduce a second database or persistence layer.

10. The existing `rss_source_items` schema is not automatically approved or considered sufficient for X persistence.

11. Persistent live X Content must not be stored in `rss_source_items` or another schema until an X-specific PostgreSQL persistence design is separately approved as compliant with D-041.

### MUTABLE COMPLIANCE STATE

12. Retained X Content must remain technically capable of being modified or removed when the corresponding source state or applicable X requirement changes.

13. Compliance handling must support at minimum X Content that becomes:

- deleted;
- modified;
- private or protected;
- associated with a suspended account;
- withheld;
- removed;
- unavailable;
- otherwise subject to modification or removal under applicable X requirements.

14. Required modification or removal must occur as soon as reasonably possible and within any applicable deadline imposed by current X requirements, an applicable written removal request, or applicable law.

15. Protected and blocked status must be respected and must not be bypassed through persistence or downstream processing.

### GEO-DATA BOUNDARY

16. Module 7 does not collect or retain X geographic or location data as a standalone dataset.

17. Any future requirement to persist or aggregate X geographic data requires separate compliance review and explicit project approval.

### COMPLIANCE-REMOVAL INVARIANT

18. After compliance removal, an ordinary persisted source record must not retain removed X Content, including Post text, Post ID, profile or author data, or other data falling within the applicable definition of X Content.

19. Because the applicable X definition includes copies and derivative works, the project must not automatically retain after compliance removal any:

- hash;
- fingerprint;
- mapping;
- identifier;
- deterministic digest;
- reversible surrogate;
- linkable surrogate;
- other derivative based on the removed X Content;

unless the permissibility of that specific residual representation is separately confirmed by current official X terms or other official X authorization.

20. D-041 does not assume that a Post ID, hash, fingerprint, mapping or other source-derived identity is an acceptable compliance tombstone.

### INTERNAL PROCESSING HISTORY

21. Any internal processing history retained after compliance removal must be independent of the removed X Content.

22. Such retained history must not:

- contain X Content;
- contain a copy or derivative of removed X Content;
- allow reconstruction of removed X Content;
- identify the removed X source item;
- allow retained history to be linked to the specific removed X source item;
- preserve reversible or deterministic source-derived identity.

23. The permissibility and exact fields of any retained audit or processing history must be determined by the next separately approved schema decision before implementation.

### TOMBSTONE AND DATABASE DESIGN DEFERRED

24. D-041 does not define or invent a compliant tombstone representation.

25. Whether a tombstone is required at all, and which fields could lawfully and technically remain after removal, is deferred to the next separate schema decision.

26. D-041 does not approve database tables, columns, indexes, constraints, migrations, hashes, identifiers or deletion mechanics.

27. The exact X-specific PostgreSQL schema and migration design require a separate explicit project decision before implementation.

### CONFLICT RULE

28. If D-041 compliance requirements conflict with the current PostgreSQL persistence design, deduplication model, processing-history requirement or any other approved architecture, the conflict must be surfaced for a separate explicit decision.

29. Compliance conflicts must not be silently worked around.

### DEDUPLICATION IMPLICATION

30. D-035 stable-identity and deterministic-deduplication requirements do not authorize retention of source-derived identity after compliance removal in violation of D-041.

31. How deterministic deduplication semantics remain compliant after removal is deferred to the next schema decision.

### AUTHORIZATION BOUNDARIES

32. D-041 authorizes no new X API request.

33. D-040 is exhausted. Any further live X API request requires separate explicit authorization.

34. D-041 does not start X Collector implementation.

35. D-041 does not authorize persistent live X collection.

36. D-041 does not authorize any PostgreSQL schema change or creation of an X-specific table.

### RELATION TO EXISTING DECISIONS

37. D-032, D-034, D-035, D-036, D-037, D-038, D-039 and D-040 remain authoritative within their existing scopes.

38. D-041 does not change budget limits, Auto Recharge policy, Billing Cycle Cap, access boundaries, safe-stop rules, architecture, roadmap, module order or the approved V1 source list.

39. The next required Module 7 step is a separate explicit schema/persistence decision that implements D-041 without inventing an unapproved tombstone or retention mechanism.

## D-042 — X POSTGRESQL PERSISTENCE SCHEMA AND COMPLIANCE LIFECYCLE

Status: FIXED / APPROVED

Date: 2026-09-25

### PERSISTENCE ARCHITECTURE

1. PostgreSQL remains the single cross-cutting persistence layer under D-017.

2. D-042 does not introduce a second database, Redis, queue, microservice, new schema namespace, new runtime database role or new migration framework.

3. Module 7 uses a separate source-specific table named `x_source_items`.

4. The existing `rss_source_items` table is not modified or reused for X persistence.

5. X persistence continues the existing versioned SQL migration sequence. The next migration is `003_x_source_items.sql`.

6. D-042 does not itself authorize creation or application of migration `003_x_source_items.sql`. That requires a separate implementation step.

### DATABASE SECURITY BOUNDARY

7. The migration must use the existing approved PostgreSQL migration / security path established in Module 2. No new administrative mechanism or privileged runtime role is introduced.

8. Runtime X Collector code must not use `POSTGRES_USER`, administrative database credentials or perform DDL.

9. Runtime operations against `x_source_items` use the existing `opportunity_scanner_app` credentials and only the necessary `SELECT`, `INSERT`, `UPDATE` and `DELETE` operations.

10. D-042 grants no new DDL or administrative privileges to `opportunity_scanner_app`.

11. The existing Module 2 configuration already grants `CREATE` on schema `public` to `opportunity_scanner_app`. D-042 does not expand, rely on, revoke or silently redesign that existing privilege. Any future least-privilege hardening requires a separate explicit security decision.

### MINIMUM X RECORD

12. The approved logical schema for `x_source_items` is:

`id bigserial PRIMARY KEY`

`x_post_id text NOT NULL`

`x_edit_root_id text NOT NULL`

`content_text text NOT NULL`

`filter_state text NOT NULL DEFAULT 'PENDING' CHECK (filter_state IN ('PENDING', 'PASS', 'REJECT'))`

`collected_at timestamptz NOT NULL`

`created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP`

`updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP`

`UNIQUE (x_edit_root_id)`

`UNIQUE (x_post_id)`

13. `x_post_id` represents the current / latest retained revision ID of the logical Post.

14. `x_edit_root_id` represents the first ID in `edit_history_tweet_ids` and is the deterministic logical identity of the full edit chain.

15. For a never-edited Post, `x_edit_root_id == x_post_id`.

16. X API edit semantics assign a new Post ID to each revision. Therefore deduplication based only on current `x_post_id` is insufficient for logical-item identity.

17. If required `x_post_id`, `edit_history_tweet_ids[0]` or `content_text` is missing or structurally invalid, the collector must fail safely without creating a false persisted record.

### X CONTENT BOUNDARY

18. `x_post_id`, `x_edit_root_id` and `content_text` are retained X-derived data and may exist only while the corresponding record is permitted to be retained under D-041.

19. Module 7 does not persist without a separate future decision:

- author or profile data;
- public or non-public metrics;
- geographic data;
- conversation IDs;
- the full `edit_history_tweet_ids` array;
- historical revision IDs beyond the required current and root identities;
- media metadata;
- other additional X API fields.

20. `edit_history_tweet_ids` is used during normalization only to derive `x_edit_root_id` and the current revision relationship. The full array is not archived in PostgreSQL.

### COMMON FILTER INTEGRATION

21. No X-specific Filter Engine is introduced.

22. The existing Module 6 Filter Engine processes the current retained revision with `title=None` and `content_text=current_post_text`.

23. Persisted `filter_state` remains compatible with Module 6 and is limited to `PENDING`, `PASS` and `REJECT`.

### INITIAL PERSISTENCE

24. On first appearance of a new edit chain, exactly one `x_source_items` row is created with current `x_post_id`, `x_edit_root_id = edit_history_tweet_ids[0]`, current `content_text`, and `filter_state = 'PENDING'`.

25. After early persistence, the record is passed to the existing common Filter Engine.

26. After deterministic filtering, `filter_state` is updated to `PASS` or `REJECT`.

### DETERMINISTIC EDIT-CHAIN DEDUP

27. `UNIQUE(x_edit_root_id)` is the database-level logical deduplication boundary for the edit chain.

28. Normal repeated collection of the same revision in the same edit chain must not create a second logical source-item row.

29. Collection of another revision with the same `x_edit_root_id` must not create a second logical source-item row.

30. `UNIQUE(x_post_id)` additionally prevents the same current revision ID from being retained in multiple rows but does not replace logical deduplication through `x_edit_root_id`.

### EDIT LIFECYCLE

31. A new revision belongs to the same logical item when incoming `edit_history_tweet_ids[0]` equals persisted `x_edit_root_id`.

32. When incoming current `x_post_id` differs from persisted `x_post_id` for the same `x_edit_root_id`, the existing row is updated in place.

33. On such a revision update:

- `x_post_id` becomes the new current / latest Post ID;
- `content_text` becomes the new current / latest Post text;
- `filter_state` becomes `PENDING`;
- `updated_at` becomes `CURRENT_TIMESTAMP`.

34. Old Post text is not archived.

35. The previous current revision ID is not retained in a history or version table.

36. D-042 does not introduce an edit-version history table.

37. After revision update, the current revision is passed again through the existing common Filter Engine and `filter_state` is updated to `PASS` or `REJECT`.

38. A new revision must not inherit a filtering result based on the previous revision text.

### UPDATED_AT SEMANTICS

39. `DEFAULT CURRENT_TIMESTAMP` applies to INSERT only and does not automatically update `updated_at` on PostgreSQL UPDATE operations.

40. Application persistence operations must explicitly set `updated_at = CURRENT_TIMESTAMP` whenever current `x_post_id`, `content_text`, revision-related `filter_state`, or another separately approved mutable persistence field changes.

41. No new PostgreSQL trigger, ORM behavior or framework is introduced for `updated_at`. The project continues the existing explicit application-update approach.

### COMPLIANCE REMOVAL

42. When an applicable X compliance state requires cessation of X Content retention, the complete corresponding `x_source_items` row is hard-deleted.

43. This applies when the applicable compliance action requires removal because of deletion, protection/private state, deactivation, suspension, withholding, removal or another applicable removal condition.

44. No per-item X tombstone remains after hard DELETE.

45. After compliance removal the project does not retain `x_post_id`, `x_edit_root_id`, previous revision IDs, Post text, hash, fingerprint, mapping, deterministic digest, reversible or linkable surrogate, or another source-derived identifier or derivative unless that exact residual representation is separately confirmed permissible under D-041.

46. D-042 approves a NO-TOMBSTONE design for Module 7 v1.

47. Any future technical requirement for a tombstone or residual source-derived identity requires a new review of current official X requirements and a separate explicit project decision.

### PROCESSING HISTORY AFTER REMOVAL

48. No per-item processing history linked to the removed X record is retained after compliance hard DELETE.

49. This is the X-specific retention / deletion rule under D-011 and D-041.

50. While an X record is lawfully retained, its processing lifecycle may be represented by its current persisted state.

51. Compliance removal deletes the source record together with all source-specific identity or history that could reconstruct, identify or link the removed item.

52. D-042 introduces no separate audit or history table for removed X items.

53. Generic operational history may remain only when it is genuinely independent of the removed X Content and cannot reconstruct, identify or link the removed source item.

54. D-042 does not automatically approve any X-derived aggregate, audit key or identifier for retention after removal.

### DEDUP AFTER COMPLIANCE REMOVAL

55. D-035 deterministic deduplication applies to currently retained X logical records through `UNIQUE(x_edit_root_id)`.

56. Compliance removal destroys the retained logical identity of that edit chain.

57. No hidden dedup identity or tombstone is retained after removal.

58. If a previously fully removed logical Post later becomes lawfully available again through an officially permitted X API path, absence of the former source-derived identity means it may be created as a new retained source record.

59. This behavior is a consequence of the D-041 compliance-removal invariant and is not a bypass of D-035.

### SCRUB_GEO

60. Module 7 v1 does not persist geographic data.

61. Therefore Batch Compliance `scrub_geo` does not require removal of a geo field from `x_source_items` because no such field exists in the approved minimal schema.

62. Any future permission to retain geographic data requires a separate schema and compliance decision including `scrub_geo` behavior.

### COMPLIANCE-SYNCHRONIZATION GATE

63. A compliant persistence schema alone does not prove that the application can detect X compliance changes within the required time.

64. Official X API documentation provides Batch Compliance as a candidate mechanism for checking stored Post or User IDs, including compliance actions such as `delete`, `rehydrate` for `tweet_edited`, and `scrub_geo`.

65. A `rehydrate / tweet_edited` action is a potential mechanism for detecting an edit event, after which the current revision would need to be obtained through a separately approved officially permitted path and processed through the D-042 edit lifecycle. D-042 does not authorize that fetch.

66. Batch Compliance is only a candidate V1 compliance-synchronization mechanism.

67. The following have not yet been verified or approved for the current Opportunity Scanner X App:

- actual Batch Compliance availability;
- Pay Per Use eligibility;
- pricing or billing;
- request, job and resource cost boundaries;
- permitted job size;
- cadence;
- turnaround time;
- suitability for required compliance deadlines;
- required handling of current and root revision IDs;
- required additional Post lookup or rehydration requests.

68. Batch Compliance is therefore not yet an approved production compliance mechanism.

### COMPLIANCE STREAMS BOUNDARY

69. X also documents near-real-time Compliance Streams for delete, edit and account-state events.

70. Current official documentation identifies Compliance Streams as requiring Enterprise access.

71. Compliance Streams are therefore not automatically the Module 7 v1 solution, are outside the current Pay Per Use approval and are not assumed to be part of Module 7.

72. Any future Compliance Streams use requires separate access, cost and architecture approval.

### REMAINING LIFECYCLE GATE

73. Persistent live X collection remains prohibited after approval of D-042.

74. The next separate project step must verify current official availability, access, cost and operational suitability of Batch Compliance or another officially permitted compliance mechanism for the existing App.

75. That step must separately define deterministic compliance cadence and verify that the mechanism can satisfy D-041 removal obligations within the applicable required time.

76. No additional endpoint, Post lookup, compliance job, stream or paid request is authorized automatically.

### DOWNSTREAM BOUNDARY

77. `x_source_items` does not include Telegram delivery state because Module 7 does not implement Telegram delivery.

78. D-042 does not implement or move into Module 7:

- EXTRACT;
- AI Analyzer;
- Anti-Scam;
- Risk;
- Score;
- Telegram Sources;
- Discord;
- scheduler infrastructure.

79. D-042 does not modify `rss_source_items` or reopen Module 4 or COMPLETED / PASS Module 6.

### BACKUP / RECOVERY BOUNDARY

80. Hard DELETE defines removal from the active working persistence model.

81. D-042 does not authorize a separate X raw archive, revision archive or X-specific backup copy.

82. Production backup / WAL retention and guaranteed compliance removal from production backup or recovery paths must be separately verified before production 24/7 persistence. D-042 does not silently resolve that future requirement.

### AUTHORIZATION BOUNDARIES

83. D-042 does not by itself authorize:

- creation or application of `003_x_source_items.sql`;
- PostgreSQL modification;
- a new X API request;
- a Batch Compliance job;
- a Post Lookup request;
- a Compliance Stream connection;
- X Collector implementation;
- persistent live X collection;
- spending remaining prepaid balance;
- increasing Billing Cycle Cap;
- enabling Auto Recharge.

84. After approval, D-042 must first be synchronized into authoritative project documentation and Git.

85. Only afterward may a separate implementation step explicitly authorize creation and deterministic local testing of `003_x_source_items.sql` using synthetic fixtures and local PostgreSQL without live X Content.

### RELATION TO EXISTING DECISIONS

86. D-017 remains authoritative for the single PostgreSQL persistence layer.

87. D-030 and D-031 remain authoritative for the common Filter Engine and `PASS / REJECT` semantics.

88. D-032 remains authoritative for Module 7 scope and the official API boundary.

89. D-035 remains authoritative for stable logical identity and deterministic deduplication.

90. D-041 remains authoritative for X content compliance, hard-removal constraints and the prohibition on automatically retaining source-derived derivatives.

91. D-034 through D-040 retain their existing budget, access, credential and live-verification boundaries.

92. D-042 does not change the approved architecture, roadmap, source list or module order.

## D-043 — X BATCH COMPLIANCE ACCOUNT ACCESS VERIFICATION AUTHORIZATION

Status: FIXED / APPROVED / EXECUTED

Date: 2026-09-25

1. D-043 authorizes exactly one read-only request:

`GET https://api.x.com/2/compliance/jobs?type=tweets`

2. The sole purpose of this request is to verify whether the currently connected Development App has access to the X Batch Compliance endpoint.

3. The confirmed documented unit cost for this GET endpoint is USD $0.005 per request.

4. The request must use only the existing local Git-ignored `X_BEARER_TOKEN`.

5. The Bearer Token must not be printed, logged, copied into documentation or stored in Git.

6. D-043 does not authorize creation of a Compliance Job.

7. `POST /2/compliance/jobs` is not authorized.

8. D-043 does not authorize:

- Batch Compliance job creation;
- upload of compliance input data;
- download of compliance results;
- Post Lookup;
- rehydration;
- Recent Search;
- pagination;
- another X endpoint;
- another API request.

9. Safe verification output is limited to non-secret metadata sufficient to determine access status, including:

- HTTP status;
- presence or absence of a `data` result;
- `meta.result_count` if returned;
- sanitized error category if an error is returned.

10. Job IDs, upload URLs, download URLs or other unnecessary response details must not be persisted in Git or project documentation.

11. HTTP 200 confirms actual access to the GET Batch Compliance endpoint for the current App.

12. HTTP 200 does not by itself approve Batch Compliance as the production compliance-synchronization mechanism and does not authorize creation of a Compliance Job.

13. HTTP 403 means Batch Compliance access is not confirmed for the current App and may indicate missing endpoint enrollment or another access requirement.

14. No workaround, alternate credential path or access bypass may be attempted after HTTP 403.

15. HTTP 401, unexpected billing behavior, pricing mismatch, redirect to another endpoint, unexpected endpoint behavior or another unexpected result requires immediate STOP with no second request.

16. Before execution, the current Billing Cycle Cap, Auto Recharge state and Current Spend must be verified through the existing approved billing-check path.

17. After execution, billing state must be verified again without making an additional X API request.

18. D-043 does not authorize:

- X Collector implementation;
- migration `003_x_source_items.sql`;
- PostgreSQL schema changes;
- persistent live X collection;
- Compliance Streams;
- Staging or Production connection;
- Billing Cycle Cap increase;
- Auto Recharge activation;
- any additional prepaid-credit funding.

19. The authorization is exhausted after exactly one authorized GET request regardless of HTTP result.

20. D-042 remains authoritative for X PostgreSQL persistence and the compliance-synchronization gate.

21. D-034 through D-042 retain their existing budget, access, credential, persistence, compliance and live-request boundaries except for the single additional GET request explicitly authorized by D-043.

### EXECUTION RESULT

D-043 was executed on 2026-09-25.

Exactly one authorized read-only request was executed:

`GET /2/compliance/jobs?type=tweets`

Safe verification result:

- `HTTP_STATUS=200`
- `DATA_PRESENT=False`
- `META_RESULT_COUNT=0`
- `ACCESS_RESULT=PASS`

The result confirms that the current Development App has access to the GET Batch Compliance endpoint.

No Compliance Job was created. No POST request, Post Lookup, rehydration, Recent Search, pagination or other X API request was executed under D-043.

The D-043 authorization is exhausted. No second request is authorized.

Post-request billing verification showed:

- Remaining Balance: USD $4.95
- Billing Cycle Cap: USD $1.00
- Auto Recharge: OFF
- Current Spend: USD $0.05

The Console displays these values only at cent precision, so the exact USD $0.005 request charge was not independently visible in the displayed billing totals.

This execution result confirms endpoint access only. It does not approve Batch Compliance as the production compliance-synchronization mechanism and does not authorize persistent live X collection or X Collector implementation.

## D-044 — X BATCH COMPLIANCE SYNTHETIC LIFECYCLE VERIFICATION AUTHORIZATION

Status: FIXED / APPROVED

Date: 2026-09-25

### PURPOSE

1. D-044 authorizes one strictly bounded synthetic verification of the full Batch Compliance lifecycle solely to verify technical operability with the current Development App.

2. The test does not use a real Post ID, User ID, X Content or collector data.

3. The only input is:

`not_a_valid_id`

4. Official Batch Compliance documentation identifies malformed / non-numeric input as an `invalid_id` result case.

### EXACT REQUEST ENVELOPE

5. D-044 authorizes at most one:

`POST /2/compliance/jobs`

to create one `tweets` Compliance Job.

6. At most one PUT is authorized exclusively to the `upload_url` returned by that specific authorized job.

7. The upload body contains exactly one synthetic line:

`not_a_valid_id`

8. At most six:

`GET /2/compliance/jobs/{id}`

requests are authorized exclusively to check the state of that same job.

9. Polling begins only after successful upload.

10. Approximately 60 seconds is used between status checks.

11. If the job reaches terminal `complete` before the sixth status GET, polling stops immediately.

12. If the job is still not `complete` after the sixth status GET, verification stops. A seventh GET is not authorized.

13. If the job reaches `failed`, `expired` or another terminal / unexpected state, verification stops.

14. At most one GET is authorized exclusively to the `download_url` belonging to that same job, and only after confirmed `complete`.

15. The maximum D-044 network envelope is:

- 1 create POST;
- 1 signed upload PUT;
- 6 status GET;
- 1 signed download GET.

No more than 9 network operations total.

### NO RETRIES

16. D-044 authorizes no automatic retries.

17. A failed or interrupted upload is not repeated.

18. A failed or interrupted download is not repeated.

19. A failed status request is not retried beyond the already authorized request count.

20. If the `upload_url` expires, STOP.

21. D-044 does not authorize `DELETE /2/compliance/jobs/{id}`, cancel / recreate or creation of a second job.

### REDIRECT / ENDPOINT BOUNDARY

22. Automatic redirect following must be disabled for upload and download.

23. If `upload_url` or `download_url` returns a redirect requiring an additional request, STOP.

24. If an operation requires another endpoint, new URL flow, additional authentication operation or any request outside the D-044 envelope, STOP.

25. No endpoint may be substituted manually for the URL returned by the authorized Compliance Job.

### VERIFIED KNOWN PRICING

26. Confirmed pricing:

`POST /2/compliance/jobs` — USD $0.010 per request.

27. Confirmed pricing:

`GET /2/compliance/jobs/{id}` — USD $0.005 per request.

28. Therefore the maximum known API portion of D-044 is:

`1 × $0.010 + 6 × $0.005 = USD $0.040`

29. This is not the complete confirmed cost of D-044 because signed upload / download pricing has not been separately verified.

### SIGNED URL COST BOUNDARY

30. Official Batch Compliance documentation describes `upload_url` as a signed PUT and `download_url` as a signed GET on the Batch Compliance lifecycle, but does not publish a separate price for those operations in the reviewed documentation.

31. The reviewed official general pricing interface does not show a separate published pricing item for Batch Compliance signed upload / download operations.

32. Therefore:

`upload_url PUT cost: UNKNOWN / NOT SEPARATELY VERIFIED`

`download_url GET cost: UNKNOWN / NOT SEPARATELY VERIFIED`

33. D-044 does not assume these operations are USD $0, free or included.

34. The known USD $0.040 must not be documented as the complete lifecycle cost.

35. The full observed lifecycle billing delta must be checked after D-044 execution.

### BILLING SAFETY BOUNDARY

36. The existing Billing Cycle Cap remains USD $1.00 and is not increased.

37. Auto Recharge remains OFF.

38. No additional prepaid funding is authorized.

39. D-044 does not change the D-034 / D-036 budget safeguards.

40. Before the first D-044 request, verify:

- Remaining Balance;
- Billing Cycle Cap;
- Auto Recharge;
- Current Spend.

41. Before the upload PUT, billing state must be checked again through the existing approved Console path.

42. If an unexpected billing delta, pricing mismatch, Billing Cycle Cap change, Auto Recharge change or other unexpected billing behavior appears after job creation, upload must not be executed; STOP.

43. Before the download GET, billing state must be checked again.

44. If unexpected billing behavior appears after the create / upload / status phase, or the action no longer remains within the existing Billing Cycle Cap / approved budget boundary, download must not be executed; STOP.

45. Billing verification itself does not authorize another X API request; the existing Console billing-check path must be used.

46. Final billing verification is mandatory after D-044 ends.

47. Final verification records the observed billing delta as:

`post-D044 Current Spend - pre-D044 Current Spend`

48. If Console precision does not allow the exact amount to be determined, record it as not independently visible at Console display precision.

49. No unknown billing delta may be retrospectively attributed specifically to upload or download without official evidence.

50. Billing Cycle Cap USD $1.00 remains the absolute account-level safety ceiling. D-044 does not claim that the complete test will cost USD $0.040; USD $0.040 is only the maximum pre-verified cost of create plus six status GET requests.

### UPLOAD SAFETY

51. The signed `upload_url` is treated as secret.

52. It must not be printed, persisted in Git, documentation, screenshots or logs.

53. It may exist only transiently in process memory for the authorized upload.

54. Upload is performed with exactly one PUT.

55. Upload payload contains no real X IDs and no X Content.

### DOWNLOAD SAFETY

56. The signed `download_url` is also treated as secret.

57. It must not be printed or persisted.

58. Download is performed with exactly one GET after confirmed `complete`.

59. The response is processed transiently; the raw response body must not be stored in Git or documentation.

60. For the expected synthetic case, only the following may be recorded:

- result record count;
- sanitized error category.

The expected documented case is:

`ERROR_CATEGORY=invalid_id`

### SAFE EVIDENCE

61. After execution, only the following safe metadata may be documented:

- create HTTP status;
- upload HTTP status;
- number of status GET requests performed;
- final job status;
- download HTTP status;
- result-record count;
- sanitized result / error category;
- pre / post billing state;
- total observed billing delta if Console precision allows it to be determined.

62. The following must not be persisted:

- job ID;
- `upload_url`;
- `download_url`;
- signed tokens;
- Bearer Token;
- complete response bodies;
- transient authorization headers.

### CREDENTIAL BOUNDARY

63. Only the existing local Git-ignored `X_BEARER_TOKEN` may be used.

64. The Bearer Token must not be printed, logged, placed in clipboard evidence or stored in Git.

65. After execution, transient variables containing token, job ID and signed URLs must be cleared.

### STOP CONDITIONS

66. Immediate STOP with no additional API calls applies on:

- pricing mismatch;
- unexpected billing behavior;
- HTTP 401;
- HTTP 403;
- unexpected redirect;
- wrong-purpose or expired signed URL;
- unexpected endpoint;
- upload failure;
- unexpected status;
- job failure or expiry;
- more than 6 polls being required;
- download failure;
- need for retry;
- need for a second job;
- need for any request outside the D-044 envelope.

67. No workaround, alternative credentials or access bypass is authorized.

### WHAT D-044 DOES NOT AUTHORIZE

68. D-044 does not authorize:

- real Post IDs;
- real User IDs;
- X Content persistence;
- Post Lookup;
- `GET /2/tweets`;
- rehydration;
- Recent Search;
- production Batch Compliance cadence;
- recurring jobs;
- scheduler;
- Compliance Streams;
- migration `003_x_source_items.sql`;
- PostgreSQL changes;
- X Collector implementation;
- persistent live X collection;
- Staging;
- Production;
- Billing Cycle Cap increase;
- Auto Recharge;
- additional funding.

### RESULT INTERPRETATION

69. A successful synthetic lifecycle confirms only that the current Development App is technically capable of:

`create → upload → process/poll → download`

through Batch Compliance.

70. It does not automatically approve Batch Compliance as the production compliance-synchronization mechanism.

71. After successful D-044, separate decisions are still required for:

- production cadence;
- actual operating cost;
- behavior for real retained IDs;
- compliance deadline suitability;
- edit `rehydrate` lifecycle;
- Post Lookup authorization / cost envelope;
- reliability / retry policy;
- scheduling;
- backup / recovery interaction.

### AUTHORIZATION EXHAUSTION

72. D-044 is exhausted after the first synthetic lifecycle attempt regardless of whether it reaches download or stops earlier under a STOP condition.

73. Unused request slots under D-044 do not carry over to another test.

74. A second job or repetition of D-044 requires a new explicit project decision.

### D-044 EXECUTION RESULT

Execution date: 2026-09-25

Status: EXECUTED / EXHAUSTED

Verification result: FAIL — expected sanitized semantic result `invalid_id` was not verified.

Observed authorized lifecycle:

- pre-request billing checkpoint: Remaining Balance USD $4.95; Billing Cycle Cap USD $1.00; Auto Recharge OFF; Current Spend USD $0.05;
- exactly one authorized `POST /2/compliance/jobs`: HTTP 200; job status `created`; Job ID, upload URL and download URL were present;
- pre-upload billing checkpoint: Remaining Balance USD $4.95; Billing Cycle Cap USD $1.00; Auto Recharge OFF; Current Spend USD $0.05;
- exactly one authorized signed upload PUT using only `not_a_valid_id`: HTTP 200;
- exactly one authorized status GET: HTTP 200; job status `complete`; no further polling was performed;
- pre-download billing checkpoint: Remaining Balance USD $4.95; Billing Cycle Cap USD $1.00; Auto Recharge OFF; Current Spend USD $0.05;
- exactly one authorized signed download GET: HTTP 200;
- downloaded result contained exactly one record;
- safe parser result: `ERROR_CATEGORY=UNKNOWN_OR_NONE`;
- expected `invalid_id` semantic result was therefore not verified;
- raw response body was not retained;
- transient Job ID, signed upload URL, signed download URL and credential variables were cleared after execution;
- final billing checkpoint: Remaining Balance USD $4.95; Billing Cycle Cap USD $1.00; Auto Recharge OFF; Current Spend USD $0.05.

At Console cent-level display precision, the observed pre-to-post Current Spend delta is USD $0.00. This does not prove that the actual lifecycle cost was zero and does not prove that signed upload or download operations are free; exact sub-cent or delayed billing was not independently visible.

The transport lifecycle `create → upload → poll → download` was technically reached successfully, but D-044 does not receive PASS because the expected sanitized `invalid_id` result was not verified.

No retry, second job, second download, additional polling, Post Lookup, rehydration, Recent Search or other X API request was executed.

D-044 authorization is exhausted. Any further investigation requires a new explicit project decision and authorization.

Batch Compliance remains only a candidate and is not approved as the production compliance-synchronization mechanism. Persistent live X collection and X Collector implementation remain unauthorized.

## D-045 — X BATCH COMPLIANCE D-044 SEMANTIC RECONCILIATION

Status: FIXED / APPROVED

Date: 2026-09-25

### CONTEXT

D-044 — X Batch Compliance Synthetic Lifecycle Verification Authorization — was executed and exhausted.

The authorized transport lifecycle reached:

`create → upload → status complete → download`

with HTTP 200 at each executed transport step.

The downloaded result contained exactly one record.

The D-044 safe parser searched for the expected semantic result:

`ERROR_CATEGORY=invalid_id`

but returned:

`ERROR_CATEGORY=UNKNOWN_OR_NONE`

Therefore D-044 semantic verification was recorded as FAIL under its approved test oracle.

The raw download response body was intentionally not retained under the D-044 safety boundary.

### CURRENT OFFICIAL DOCUMENTATION RECONCILIATION

Current reviewed official X Batch Compliance documentation describes downloaded compliance results as newline-delimited JSON records based on fields including:

- `id`;
- `action`;
- relevant timestamps;
- `reason`.

Current reviewed documentation describes Post compliance reasons / events including values such as:

- `deleted`;
- `bounced`;
- `protected`;
- `suspended`;
- `scrub_geo`.

The current reviewed official documentation does not establish that malformed input `not_a_valid_id` must produce:

`"error":"invalid_id"`

and does not establish `invalid_id` as the deterministic result representation assumed by the D-044 parser.

Therefore the D-044 assumption that `not_a_valid_id` had an officially documented deterministic `invalid_id` result is:

`NOT SUPPORTED BY CURRENT OFFICIAL DOCUMENTATION`

### HISTORICAL INTEGRITY

The original approved D-044 text and execution result are not silently rewritten.

D-044 remains:

`FIXED / APPROVED / EXECUTED / EXHAUSTED`

Its approved semantic verification result remains:

`FAIL`

because the approved test oracle was not satisfied.

D-045 changes the interpretation of that FAIL based on the current documentation reconciliation; it does not erase or retroactively replace the D-044 result.

### INTERPRETATION

The D-044 transport verification is considered:

`PASS`

because the authorized create, upload, processing / status, and download transport lifecycle completed successfully.

The D-044 semantic verification remains:

`FAIL UNDER THE APPROVED D-044 TEST ORACLE`

However, that semantic FAIL must not be interpreted as evidence that X Batch Compliance semantic processing itself failed.

The D-044 `invalid_id` oracle was not supported by the current reviewed official documentation.

Because the raw response body was intentionally not retained, the actual semantic meaning of the single downloaded result record is:

`UNKNOWN / NOT RECOVERABLE FROM RETAINED EVIDENCE`

No claim may be made that the record was `bounced`, `deleted`, `protected`, `suspended`, `scrub_geo`, `invalid_id`, or any other specific semantic result.

### FUTURE TEST RULE

`not_a_valid_id` must not be reused as an assumed deterministic official Batch Compliance semantic test vector unless future official documentation explicitly establishes its behavior.

Any future Batch Compliance semantic verification must define its expected parser / oracle from the then-current official documented result schema before execution.

The expected fields, actions, reasons, and PASS / FAIL conditions must be documented and approved before any future live test.

### AUTHORIZATION BOUNDARY

D-045 authorizes no X API request.

D-045 does not authorize:

- creation of another Compliance Job;
- upload;
- polling;
- download;
- retry of D-044;
- Post Lookup;
- rehydration;
- Recent Search;
- Compliance Streams;
- real Post IDs;
- real User IDs;
- X Content persistence;
- migration `003_x_source_items.sql`;
- PostgreSQL changes;
- X Collector implementation;
- persistent live X collection;
- Staging;
- Production;
- Billing Cycle Cap changes;
- Auto Recharge changes;
- additional funding.

Any further X API verification requires a new explicit project decision and authorization.

### PROJECT STATUS EFFECT

Batch Compliance remains only a candidate for the production compliance-synchronization mechanism.

It is not approved for production use by D-045.

Module 7 remains:

`SCOPE APPROVED / PRE-IMPLEMENTATION / ACCESS GATED`

Formal X source status remains:

`UNKNOWN — REQUIRES APPROVAL`

Persistent live X collection and X Collector implementation remain unauthorized.
