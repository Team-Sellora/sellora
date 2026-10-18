# Testing

[Back to overview](../README.md)

<p align="center"><img src="../assets/chart-code-and-tests.svg" alt="Lines of code and automated tests per repository" width="100%"></p>

## Strategy

| Level | Tools | What it covers |
|---|---|---|
| Unit | xUnit | Domain rules with no framework: GPS distance, check-in policy, delivery transitions, retry timing, fulfilment decisions |
| API | xUnit, `WebApplicationFactory` | Full HTTP pipeline in memory: routing, auth policies, validation, status codes |
| Integration | Testcontainers, PostgreSQL 16 | Real SQL, real constraints, real migrations |
| Messaging | Kafka in CI | Consumers, producers and the outbox relay against a real broker |
| Email | Mailpit | Notification sends real SMTP and the test reads the inbox |
| Web | Vitest, Testing Library | API clients, hooks, formatters, route rules and key components |
| Acceptance | QA role each sprint | Every story's acceptance criteria tested on staging before it closes |

## Why real infrastructure

Several of the most important rules live in the database. Category names are unique regardless of letter case. Each consumer must store an event ID once. The audit role must not be able to update a row.

An in-memory fake would pass tests that PostgreSQL would fail. Every backend repository uses **Testcontainers** for these cases, so they run against the same engine as production.

## Examples of what is tested

| Area | Example cases |
|---|---|
| Tenant isolation | Company B cannot read or change Company A's records |
| GPS check-in | Exactly 300 m is accepted. 300.01 m is rejected. A fix older than 5 minutes is rejected |
| Payment | No check-in, expired check-in, another rep's check-in and wrong amount all fail |
| Fulfilment | Agency has everything. Agency short on one line. Company also short |
| Outbox | An event is never published before the one written ahead of it for the same order |
| Consumers | A duplicate event changes nothing. A broken message goes to the dead-letter topic |
| Email | A 4xx is retried. A hard bounce stops at once. Real messages are checked in Mailpit |
| Delivery | Transitions outside the allowed list are refused |

## Counts per repository

| Repository | Automated tests |
|---|---|
| sellora-web | 284 |
| sellora-delivery | 212 |
| sellora-organization | 199 |
| sellora-order | 194 |
| sellora-inventory | 97 |
| sellora-notification | 81 |
| sellora-catalog | 67 |
| **Total** | **1,134** |

.NET counts are `[Fact]` and `[Theory]` methods. A theory runs once per data row, so the number of executed cases is higher.

## Manual and performance testing

QA was a rotating role. Each sprint the QA member tested every story against its acceptance criteria on staging and attached the evidence to the Jira story. Load checks used JMeter through the gateway, and browser checks used Selenium.
