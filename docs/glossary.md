# Glossary

[Back to overview](../README.md)

Plain-language meaning of the terms used in this repository.

## Business terms

| Term | Meaning |
|---|---|
| **FMCG** | Fast-moving consumer goods. Everyday products like soap, biscuits and drinks that sell quickly and cheaply |
| **Company** | A business using Sellora. Also called a tenant |
| **Province** | A region the company sells in |
| **Area Manager** | Manages one or more provinces for the company |
| **Agency** | A local distributor that holds stock and serves shops in its territories |
| **Territory** | An area of shops served by exactly one sales rep |
| **Sales rep** | The person who visits shops, takes orders and collects cash |
| **Van stock** | Goods a rep carries to sell on the spot |
| **Cash sale** | An order paid at the counter, from the rep's van |
| **Scheduled delivery** | An order the agency approves and delivers later |
| **Van return** | Unsold stock a rep brings back to the agency at the end of the day |
| **Fulfilment** | Deciding where an order's stock comes from: the agency or the company |

## Technical terms

| Term | Meaning |
|---|---|
| **Microservice** | A small service that owns one part of the business and its own data, and is deployed on its own |
| **Multi-tenant** | One deployment serving many companies, each seeing only its own data |
| **API gateway** | The single entry point that checks every request before passing it to a service |
| **OAuth2 / OIDC** | Standards for signing in and issuing access tokens |
| **PKCE** | A way for a browser app to sign in safely without storing a secret |
| **JWT** | A signed token that carries who the user is, their role and their company |
| **SCIM2** | A standard API for creating and managing user accounts |
| **Event** | A message saying something happened, such as `PaymentRecorded` |
| **Kafka topic** | A named stream of events. Services publish to it and read from it |
| **Consumer** | A service that reads events from a topic and reacts |
| **Transactional outbox** | Saving an event in the same database transaction as the change, then publishing it afterwards |
| **Idempotent** | Doing the same thing twice has the same effect as doing it once |
| **Dead-letter topic** | Where messages that cannot be processed are parked for inspection |
| **Haversine** | A formula for the distance between two GPS points on a sphere |
| **Staging slot** | A copy of production used to test a release before it goes live |
| **Testcontainers** | A library that starts real databases in Docker for tests |
