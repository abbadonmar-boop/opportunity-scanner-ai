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
