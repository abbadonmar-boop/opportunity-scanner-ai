# SOURCE ACCESS PRECHECK

Status: COMPLETE / VERIFIED

Purpose: record the verified official-access state of every approved V1 source before collector implementation resumes.

Formal statuses are defined by D-033.

## Reddit

Verification date: 2026-09-16

Formal status: BLOCKED

Blocker: DATA ACCESS NOT APPROVED

Official access path:
Reddit official developer / Data API access only.

Developer account required:
YES

Application or external approval required:
YES

Credentials required:
YES, after approved official access.

Paid access / cost gate:
No paid access has been approved or activated for this project.

Technical / compliance limitations:
The project submitted an official Reddit Data Access request. The Reddit Data Team denied the request on 2026-09-12. Under D-028 and D-029, Reddit collector implementation must not proceed through scraping, unofficial mirrors, credential workarounds or any access-restriction bypass.

Persistence / retention / content-compliance:
No Reddit User Content may be collected or persisted while required official access remains unapproved.

Evidence:
- Official Reddit Data Team denial received on 2026-09-12 — supports the fact that required data access was not approved.
- D-029 — Reddit Access Denial Handling and Roadmap Continuation — records the verified denial and prohibits bypass.
- D-033 section SOURCE-SPECIFIC BASELINE — explicitly retains `BLOCKED — DATA ACCESS NOT APPROVED` unless new official evidence changes that state.

Collector implementation may proceed:
NO

Conclusion:
Reddit satisfies the D-033 criteria for BLOCKED. No new access attempt or repeated verification is required unless new official evidence changes the access state.

## X / Twitter

Verification date: 2026-09-16

Formal status: UNKNOWN — REQUIRES APPROVAL

Official access path:
Official X API through the X Developer Console and X API v2.

Developer account required:
YES

Current developer account state:
Developer onboarding was completed successfully on 2026-09-16 after review of the applicable X Developer Agreement, Developer Policy, API Restricted Use Rules, X Rules, Display Requirements, Automation Rules and Brand Guidelines.

Application or external approval required:
Developer onboarding is complete. An X App was created successfully during onboarding and is currently shown as `active`.

Current App access state:
The X App is active and its Project Access state is connected to `Default Project — Pay Per Use` in the authorized `Development` environment.

The Developer Console offers connection to:
`Default Project — Pay Per Use`

Available environment choices shown by the console:
- Development
- Staging
- Production

A confirmation dialog verified that connecting the App would connect it to `Default Project (Pay Per Use)` and that rate limits and endpoint access would follow that project's plan.

Under D-038, the `Development` connection was subsequently confirmed and executed successfully on 2026-09-22. `Staging` and `Production` remain unauthorized.

Credentials required:
YES.

The App interface exposes App-Only Authentication / Bearer Token and other credential controls. No new Bearer Token or Access Token was generated during this precheck and no secret value is recorded in this document.

Paid access / cost gate:
YES.

The currently verified post-connection billing state is:
- Remaining Balance: USD $5.00
- Billing Cycle Cap: USD $1.00
- Auto Recharge: OFF
- Current Spend: USD $0.00

The verified Project is `Default Project — Pay Per Use` and the App is connected only in the authorized `Development` environment.

The D-037 USD $5.00 prepaid credit purchase has been completed and credited.
No paid API request has been made.
No new Bearer Token or Access Token was generated during the D-038 connection step.

D-039 now separately authorizes Bearer Token credential execution and storage only in the local Git-ignored `.env` as `X_BEARER_TOKEN`. X Developer Console verification on 2026-09-23 showed that the Bearer Token row displays `Generate`, but activating that control opens a `Regenerate Bearer Token` confirmation. The user explicitly approved this verified `Generate → Regenerate` execution path; the previous Bearer Token may be invalidated. Regeneration has not yet been executed. D-039 does not authorize any X API request or X Collector implementation.

Under D-034, official X Pay Per Use use is approved in principle. D-036 fixes the first bounded live-access envelope at maximum USD $1.00 spend, 20 paid API requests, 10 Posts per Recent Search request and 200 maximum billable returned Posts / resources, with deterministic hard safe-stop conditions. D-037 authorized and completed the verified minimum one-time prepaid credit purchase of USD $5.00 without increasing the D-036 live-spend limit. D-038 authorizes only Development Project Access to the existing `Default Project — Pay Per Use`; Staging and Production are not authorized, and the authorized Development connection has been executed and verified successfully. D-039 authorizes Bearer Token regeneration through the verified `Generate → Regenerate` flow and local storage as `X_BEARER_TOKEN` in the Git-ignored `.env`; regeneration has not yet been executed. Post-connection billing state remains Remaining Balance USD $5.00, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.00. No X API request has been made.

Technical limitations relevant to the approved use case:
- The approved initial collector path under D-032 remains the official X API v2 Recent Search path.
- Development Project Access is now connected, but no endpoint call has yet been authorized or executed.
- D-039 credential execution is separately authorized through the verified `Generate → Regenerate` flow, but regeneration has not yet been executed and no API use is authorized by D-039.
- Actual endpoint availability, rate limits and billable behavior remain unverified until a separately authorized bounded live API verification is performed.
- No polling frequency or live request budget is inferred from API limits.
- No live X Content may be permanently persisted before the X-specific content-compliance policy required by D-032 is approved.

Persistence / retention / content-compliance:
The reviewed X policies require stored X Content to remain synchronized with deletion, modification, protection or removal state as applicable.

The reviewed policy set also establishes restrictions covering redistribution, display / attribution, privacy, sensitive-user inference, off-X matching, rate-limit circumvention, unofficial access and model training / fine-tuning on X Content.

Under D-032, a dedicated X-specific content-compliance policy must be approved before the first persisted live X Content.

Evidence:
- X Developer onboarding form and acceptance flow verified on 2026-09-16.
- Successful transition from onboarding into the X Developer Console verified on 2026-09-16.
- Active X App state verified in the Developer Console on 2026-09-16.
- App Project Access state `Not connected` verified on 2026-09-16.
- Project Access dialog verified `Default Project — Pay Per Use` with Development / Staging / Production connection choices on 2026-09-16.
- Pay Per Use connection confirmation dialog verified that project limits and endpoint access would follow the selected project's plan.
- Account dashboard verified $0.00 balance, $0.00 credits, $0.00 free credits and zero billable usage.
- X Developer Agreement reviewed.
- X Developer Policy reviewed.
- API Restricted Use Rules reviewed.
- X Rules reviewed.
- Display Requirements reviewed.
- Automation Rules reviewed.
- X Brand Toolkit and Brand Guidelines reviewed.
- D-032 defines the project-specific official-access, cost-budget and pre-persistence compliance gates.
- D-033 defines the formal SOURCE ACCESS PRECHECK status criteria.
- D-038 authorized `Development` Project Access to `Default Project — Pay Per Use`; successful connection verified on 2026-09-22.
- Post-connection billing state verified on 2026-09-22: Remaining Balance USD $5.00, Billing Cycle Cap USD $1.00, Auto Recharge OFF and Current Spend USD $0.00.
- No new Bearer Token or Access Token generation and no paid live API request occurred during D-038 connection execution.
- D-039 — X Bearer Token Generation and Local Secret Handling — FIXED / APPROVED on 2026-09-22.
- Secret-storage readiness verified before generation: repository-root `.env` is ignored and untracked; tracked `.env.example` contains only the safe `X_BEARER_TOKEN` placeholder; local `.env` contains exactly one empty `X_BEARER_TOKEN` key.
- X Console `Generate` → `Regenerate Bearer Token` behavior verified on 2026-09-23.
- D-039 execution clarification explicitly authorizes regeneration of the existing Bearer Token; the previous token may be invalidated.
- Bearer Token regeneration has not yet been executed and no X API request has been made under D-039.

Collector implementation may proceed:
NO.

Developer onboarding and App creation are complete. D-034 approves the official Pay Per Use path in principle, D-036 approves the first bounded live-access envelope, D-037 authorized and completed the one-time USD $5.00 prepaid credit purchase, and D-038 authorizes only Development Project Access to the existing `Default Project — Pay Per Use`. The authorized Development connection has now been executed and verified successfully. Staging and Production remain unauthorized.

No collector implementation or live API collection is authorized by this precheck result. Development Project connection was separately authorized by D-038 and has been executed. D-039 separately authorizes only Bearer Token generation and local secret storage; it does not authorize live API collection. Staging and Production connection remain unauthorized.

Conclusion:
X / Twitter satisfies the D-033 criteria for `UNKNOWN — REQUIRES APPROVAL`.

The unresolved prerequisite is no longer developer onboarding, App creation, principle-level Pay Per Use approval, bounded-envelope definition, credit-purchase authorization, credit-purchase execution, Development Project Access authorization, Development connection execution or credential-storage preparation. The remaining prerequisites before any live X API verification are controlled Bearer Token regeneration through the verified `Generate → Regenerate` flow and local storage under D-039, followed by separate explicit authorization for the first bounded paid live API request.

The X source precheck is complete at the current authorization boundary.

## Discord

Verification date: 2026-09-18

Formal status: AVAILABLE WITH LIMITATIONS

Official access path:
Official Discord Developer Platform using a Discord Application, bot user, OAuth2 / guild installation, Gateway and documented Discord APIs.

Developer account required:
YES.

Current developer account / application state:
Discord Developer Portal access is available.
The developer account email was verified.
The `Opportunity Scanner AI` application was successfully created.
The application currently has 0 server installations and 0 authorized users.

Application or external approval required:
NO for the current personal controlled implementation scale.

The Discord verification page states that application verification is required before the application can be added to more than 100 servers.

Separate privileged-intent review requirements apply at larger scale. The Bot settings page states that listed Privileged Gateway Intents require review when the bot reaches 10,000 users.

Credentials required:
YES.

A bot token / Discord application credentials are required for implementation.
No bot token or secret value is recorded in this document.
Credentials must remain outside tracked Git files.

Paid access / cost gate:
No mandatory paid access gate was identified for the approved Discord Collector path during this precheck.

No paid Discord feature was activated or purchased.

Official installation path:
The application supports guild installation through Discord's official installation system.

The official guild-installation scope selector exposes the `bot` scope.

The application must be explicitly installed into a server / guild and receive the permissions required for the approved collector functionality.

Technical limitations relevant to the approved use case:
- Collection is limited to servers / guilds where the application is legitimately installed and authorized.
- The bot must have permission to view the relevant channels.
- Reading historical messages requires the applicable message-history permission.
- Access to the content of most messages requires `Message Content Intent`.
- `Message Content Intent` is available in the current application configuration without external review at the current scale.
- Discord API and Gateway rate limits must be respected and must not be bypassed.
- Administrator permission is not required for the approved collector and must not be requested merely for convenience.
- Only the minimum permissions necessary for collection should be requested.
- Application verification is required before scaling beyond Discord's verified threshold shown by the Developer Portal.
- Privileged-intent review becomes an additional gate at the scale shown by the Developer Portal.

Persistence / retention / content-compliance:
Discord Developer Terms require API-data handling to follow the declared application functionality, applicable privacy law and Discord policies.

Stored API data must be updated or deleted when required by Discord, by the applicable user, when no longer necessary for the approved functionality, or when the application terminates, subject to applicable law.

The application must use reasonable security measures for API data and protect developer credentials.

Discord Developer Policy prohibits using message content obtained through the API to train AI / ML models, including LLMs, without explicit Discord permission.

Opportunity Scanner AI may use Discord message content only within the approved application functionality. Any future AI integration must remain inference / analysis and must not use Discord message content as a training dataset unless Discord explicitly authorizes that use.

Evidence:
- Discord Developer Portal access verified on 2026-09-18.
- Developer account email verification requirement encountered and completed.
- `Opportunity Scanner AI` application creation verified on 2026-09-18.
- Application state verified with 0 server installations and 0 authorized users.
- Bot configuration page verified the bot user, credential controls and Privileged Gateway Intents.
- Bot configuration page verified `Message Content Intent` availability and the displayed 10,000-user review threshold.
- Official Installation page verified guild installation support.
- Guild installation scope selector verified availability of the official `bot` scope.
- Application Verification page verified that application verification is required before installation on more than 100 servers.
- Discord Developer Terms reviewed.
- Discord Developer Policy reviewed.
- D-033 defines the formal SOURCE ACCESS PRECHECK status criteria.

Collector implementation may proceed:
YES, subject to the documented limitations.

No Discord collector implementation is authorized to begin until the complete five-source SOURCE ACCESS PRECHECK is finished and verified under D-033.

Conclusion:
Discord satisfies the D-033 criteria for `AVAILABLE WITH LIMITATIONS`.

An official permitted access path exists and no current external approval gate blocks controlled personal-scale implementation. Material limitations include guild-specific installation and permissions, Message Content Intent, rate limits, data-handling obligations, credential security and future verification / privileged-intent review thresholds at larger scale.

## Telegram

Verification date: 2026-09-18

Formal status: BLOCKED

Blocker:
TELEGRAM CONTENT AI-USE TERMS CONFLICT WITH THE APPROVED OPPORTUNITY SCANNER AI PIPELINE

Official access path:
Official Telegram API / MTProto using an application created through `my.telegram.org` and its own `api_id` / `api_hash`.

Developer account required:
A Telegram account with access to `my.telegram.org` is required.

Current developer account / application state:
Access to `my.telegram.org` was successfully verified.
The official `API development tools` section is available.
The `Create new application` form is available.
No Telegram API application was created during this precheck.
No `api_id`, `api_hash` or other Telegram API credential was generated or recorded.

Application or external approval required:
The official application-creation path is available through `my.telegram.org`.

No additional external approval gate was identified before creating the application itself.

Credentials required:
YES.

A Telegram API application requires its own `api_id` and `api_hash`.
No credentials were generated during this precheck.
Secrets must remain outside tracked Git files.

Paid access / cost gate:
NO mandatory paid access gate was identified.

Telegram API Terms state that the API is offered free of charge.

Technical access state:
The official API path is technically available.

However, technical availability does not make the approved Opportunity Scanner AI use case compliant.

Persistence / retention / content-compliance:
Telegram API Terms make API use subject to the Telegram Terms of Service for Content Licensing.

The Telegram API Terms explicitly prohibit using, accessing or aggregating Telegram platform data to train, fine-tune or otherwise engage in the development, enhancement or deployment of artificial intelligence, machine-learning models or similar technologies.

The Terms of Service for Content Licensing further state that Telegram prohibits scraping, indexing, harvesting, aggregation or use of Telegram data to train, fine-tune, validate or otherwise engage in the development, enhancement, benchmarking or deployment of AI / ML systems and similar technologies.

The documented exception requires all relevant users to provide explicit, informed, affirmative and continued consent limited to the specific content and specific chat, channel or other non-global context for which consent was requested.

No such consent basis exists for the approved general Telegram-source scanning use case.

Approved-project conflict:
The fixed Opportunity Scanner AI pipeline includes:

SOURCE → COLLECT → NORMALIZE → DEDUPLICATE → FILTER → EXTRACT → AI → RISK → SCORE → DATABASE → TELEGRAM

Telegram is an approved V1 source and the approved architecture includes the downstream AI Analyzer.

Using Telegram-derived content in that AI stage would conflict with the verified Telegram AI-use restrictions unless an applicable compliant exception is established.

Silently bypassing AI for Telegram records, removing Telegram from the source list, changing the pipeline, or introducing a new consent architecture would change approved project decisions and is not authorized by D-033.

Evidence:
- Official `my.telegram.org` access verified on 2026-09-18.
- Official `API development tools` / `Create new application` form verified on 2026-09-18.
- Telegram API Terms of Service reviewed on 2026-09-18.
- Telegram API Terms section 1.5 explicitly applies the Content Licensing / AI-use restrictions to Telegram API data.
- Official Telegram Terms of Service for Content Licensing reviewed on 2026-09-18.
- The Content Licensing terms explicitly prohibit AI / ML development, enhancement, benchmarking and deployment using Telegram-derived data except under the narrowly defined explicit-consent exception.
- D-033 requires BLOCKED status when mandatory compliance conditions make the approved collector implementation impossible without changing project decisions.

Collector implementation may proceed:
NO under the currently approved end-to-end Opportunity Scanner AI architecture.

Creating Telegram API credentials would not resolve the compliance conflict and is therefore not required for this precheck.

Conclusion:
Telegram satisfies the D-033 criteria for `BLOCKED`.

The blocker is not lack of technical API access. The blocker is the verified conflict between Telegram's current AI-use terms and the approved Opportunity Scanner AI pipeline in which collected source content proceeds to an AI Analyzer.

Telegram remains in the approved V1 source list and roadmap. Any future resolution requires a separate explicit project decision supported by compliant technical and policy evidence.

## RSS / Atom

Verification date: 2026-09-18

Formal status: AVAILABLE WITH LIMITATIONS

Official access path:
Explicitly configured official RSS / Atom feeds published by the source website.

Developer account required:
NO for the verified official RSS feed.

Application or external approval required:
NO for the verified official RSS feed.

Credentials required:
NO for the verified official RSS feed.

Paid access / cost gate:
NO mandatory paid access gate was encountered for the verified official RSS feed.

Current access verification:
A bounded direct HTTP request was performed against the already configured official feed:

`https://openai.com/news/rss.xml`

Verified result:
- HTTP status: 200
- Content-Type: `text/xml; charset=utf-8`
- XML root element: `rss`

No collector execution, PostgreSQL persistence or Telegram delivery was performed during this access precheck.

Technical limitations relevant to the approved use case:
- Only explicitly configured official RSS / Atom feeds are within the approved access path.
- HTML scraping is not an approved fallback.
- Browser scraping is not an approved fallback.
- Automatic HTML feed discovery is not part of the approved access path.
- Individual feeds may change URL, format, availability or publication behavior.
- A feed that becomes unavailable must fail safely and must not be silently replaced with an unapproved access method.
- Publisher-specific terms may impose additional content-use restrictions and must be respected where applicable.

Persistence / retention / content-compliance:
RSS / Atom transport itself does not remove publisher-specific rights or content-use obligations.

For each configured feed, only content made available through the official feed may be collected under the approved RSS access path.

Any source-specific retention, redistribution or downstream-use restriction discovered for a particular feed must be honored and surfaced rather than bypassed.

Evidence:
- Deterministic local verification performed on 2026-09-18 against the configured official OpenAI RSS endpoint.
- The request returned HTTP 200.
- The response Content-Type was `text/xml; charset=utf-8`.
- The parsed XML root element was `rss`.
- No authentication, developer approval or paid activation was required for this verified feed.
- Existing project decision D-022 limits RSS collection to configured official RSS / Atom feeds and prohibits substituting HTML scraping or automatic discovery.
- D-033 defines the formal SOURCE ACCESS PRECHECK status criteria.

Collector implementation may proceed:
YES, subject to the documented limitations.

The existing RSS collector remains limited to explicitly configured official feeds and source-specific compliance requirements.

No additional collector implementation resumes until the complete five-source SOURCE ACCESS PRECHECK is verified under D-033.

Conclusion:
RSS / Atom satisfies the D-033 criteria for `AVAILABLE WITH LIMITATIONS`.

An official permitted access path is available without credentials, external approval or a paid-access gate for the verified feed. The material limitations are explicit-feed configuration, no scraping fallback, feed-specific availability and publisher-specific content-use obligations.
