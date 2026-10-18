# Design decisions

[Back to overview](../README.md)

Each entry records a choice we made, the options we weighed and why we picked one. Short on purpose.

<br>

### 1. Microservices in separate repositories

**Context.** The module required independently deployable services. Four people rotated roles every sprint.

**Decision.** One repository per service, all cloned from a shared template. Same layers, same auth, same outbox, same pipeline.

**Why.** Each service deploys on its own. The template meant a member moving from QA to Dev could start in any repository on day one.

**Cost.** Shared fixes had to be copied to several repositories. We accepted that over a shared library that would couple deployments.

<br>

### 2. Kafka for events

**Context.** Services needed to react to orders, deliveries and stock changes without slowing each other down.

**Decision.** Apache Kafka. Self-hosted first, then Confluent Cloud.

**Why.** Kafka keeps messages after they are read. The Audit service, built last, could read earlier events from the start of each topic instead of starting empty. Partition keys also give per-order ordering for free.

<br>

### 3. PostgreSQL with EF Core

**Context.** The first plan used MySQL.

**Decision.** PostgreSQL 16, one database per service, with EF Core migrations. The switch was confirmed with the module lecturer.

**Why.** Better support for the constraints we needed, such as case-insensitive unique names and granular role grants for the audit log. Managed hosting on Azure Flexible Server.

<br>

### 4. Transactional outbox instead of publishing in the request

**Context.** Publishing to Kafka inside the request risks two failures. The database commits but Kafka fails, so the event is lost. Or Kafka succeeds but the database rolls back, so a false event exists.

**Decision.** Write the event to an outbox table in the same transaction. A background relay publishes it.

**Why.** The order and its event now succeed or fail together. Kafka being down only delays events. It never loses them.

<br>

### 5. Per-key ordering in the relay

**Context.** A cash sale writes `OrderConfirmed` and `PaymentRecorded` together. If the first failed to publish and the second succeeded, consumers would see a payment for an unconfirmed order.

**Decision.** The relay only picks a row when no earlier row for the same order is still unpublished. Rows are leased with a conditional update.

**Why.** Ordering holds across retries and across several relay instances.

<br>

### 6. All-or-nothing fulfilment

**Context.** An agency may hold some items of an order but not all.

**Decision.** If the agency can supply every line in full, it supplies the order. Otherwise the whole order comes from the company. Never split.

**Why.** A split order means two deliveries, two invoices and two sets of stock movements for one shop visit. The business preferred one clear source.

<br>

### 7. Scope from Organization, not from token claims

**Context.** Services needed the caller's rep, agency or province. At first these IDs were copied into WSO2 claims by hand.

**Decision.** Organization answers `GET /api/me/scope` from its own data. It also creates WSO2 logins itself over SCIM2.

**Why.** No manual console work. No chance of a mistyped ID giving someone the wrong data. One source of truth for the hierarchy.

<br>

### 8. REST between services, not gRPC

**Context.** The early design mentioned gRPC for internal calls.

**Decision.** Plain REST with typed `HttpClient`s. The caller's token is forwarded.

**Why.** Only Order makes synchronous calls, and only three of them. REST kept one protocol, one auth model and one set of tools through APIM and the browser.

<br>

### 9. Memory cache, not Redis

**Context.** Scope lookups and some reads benefit from caching.

**Decision.** `IMemoryCache` inside each service with short lifetimes.

**Why.** Adding a managed Redis in the last sprint would add cost and a new failure point for a small gain. A five minute per-instance cache was enough.

<br>

### 10. Haversine in code, not PostGIS

**Context.** The GPS gate needs the distance between two points.

**Decision.** A small Haversine function in the Domain layer, rounded to the centimetre.

**Why.** At 300 m the error is well under a metre. A database extension would add setup in every environment for no real gain. The rule also stays unit testable.

<br>

### 11. Read SMTP codes as SMTP, not as HTTP

**Context.** The backlog said "retry on 5xx". That rule comes from HTTP APIs, where 5xx means the provider is broken.

**Decision.** Over SMTP, 4xx is temporary and retried. 5xx at the recipient is a hard bounce and stops at once. Two configuration errors on our side stay retryable.

**Why.** Retrying a bad address five times wastes the budget and delays the admin seeing the real problem.

<br>

### 12. An audit log the application itself cannot change

**Context.** The audit log is the evidence in a dispute. Code-level rules are not enough if the code has a bug.

**Decision.** Two schemas. The `audit` schema is insert and read only for the runtime database role. Reporting projections live in a separate schema with full access. Migrations run from the pipeline with a separate owner credential.

**Why.** Even a compromised service cannot rewrite history. Entries are chained, so tampering with elevated access is still detected on verification.
