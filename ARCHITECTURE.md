# OPPORTUNITY SCANNER AI — ARCHITECTURE

## VERSION
Opportunity Scanner AI Architecture v1.0 — FIXED

## PRODUCT BOUNDARY
Opportunity Scanner AI v1 is a personal automated monitoring tool.

It is:
- personal, not SaaS;
- Telegram-first;
- designed for continuous automated monitoring;
- backed by PostgreSQL;
- rule-based filtered before AI analysis.

It is not:
- a manual Search Hub;
- a web application;
- a mobile application;
- an automatic task executor;
- an automatic wallet connector or transaction signer.

## APPROVED LOGICAL PIPELINE

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

## APPROVED V1 SOURCES
- X / Twitter
- Reddit
- Telegram channels
- Discord servers
- RSS / Atom

Decision reference: D-022

An explicitly configured RSS / Atom feed remains an RSS / Atom source even when published by an official company, project, organization or product website.

No separate Official Blogs source type or collector is introduced.

## CORE COMPONENTS
- Source Collectors
- Normalization
- Deduplication
- Rule-based Filter
- Data Extraction
- AI Analyzer
- Anti-Scam / Risk Engine
- Scoring Engine
- PostgreSQL
- Telegram interface

## FIXED PRODUCT RULES
- Supported publication languages: English, Russian, Ukrainian, German.
- User-facing explanations: Russian.
- Default minimum payout for the main Telegram flow: $5.
- KYC is allowed but must be explicitly flagged and risk-checked.
- Unknown project tokens are speculative rewards and receive lower priority.
- Category priority:
  1. AI / Data
  2. Testing
  3. Beginner-friendly Remote Work
  4. Web3

## POSTGRESQL PERSISTENCE BEHAVIOR

Decision reference: D-017

PostgreSQL is the single cross-cutting persistence layer.

Primary persistence occurs after collection / normalization as early as necessary for reliable recovery.

The same persisted record is progressively updated as it passes through:

DEDUPLICATE
→ FILTER
→ EXTRACT
→ AI
→ RISK
→ SCORE

No separate database or second persistence system is introduced.

This persistence behavior does not change or reorder the approved logical pipeline.
## SECURITY BOUNDARIES
The system must not automatically:
- perform third-party tasks for the user;
- connect wallets;
- sign transactions;
- send money;
- make deposits;
- expose secrets.

Secrets must not be stored in source code or committed configuration.

## EXCLUDED UNLESS EXPLICITLY APPROVED
- Kafka or another message broker
- Redis
- Microservice decomposition
- Kubernetes
- Web UI
- Mobile app

## KNOWN ARCHITECTURE ISSUES
1. RESOLVED — D-017 defines PostgreSQL as the single cross-cutting persistence layer. Early persistence is used for recovery and the same record is updated through later processing stages. The fixed logical pipeline and roadmap remain unchanged.
2. RESOLVED — D-021 defines Module 4 basic filtering as the minimum first implementation of the existing FILTER component required for RSS → Database → Filter → Telegram. The full Filter Engine remains in Module 6.

Issue 1 is resolved by D-017. Issue 2 is resolved by D-021. Neither resolution changes the fixed logical pipeline or roadmap.

## DEFERRED TECHNICAL DECISIONS
The following are not yet fixed and must not be invented prematurely:
- specific Python libraries and frameworks;
- ORM;
- migration framework;
- scheduler;
- AI provider and model;
- Telegram framework;
- detailed scoring weights and thresholds;
- detailed Anti-Scam providers and thresholds.

Changes to this architecture require a demonstrated technical reason and user approval.

