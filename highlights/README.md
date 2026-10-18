# Code highlights

[Back to overview](../README.md)

Short excerpts from the Sellora code base. They are copied from the `dev` branches without changes, apart from trimming. Each file starts with the repository and path it came from.

| File | Service | What to look for |
|---|---|---|
| [01-gps-check-in.cs](01-gps-check-in.cs) | Order | Haversine distance rounded to the centimetre so the 300 m boundary is exact. The check-in limits as one configurable record |
| [02-transactional-outbox.cs](02-transactional-outbox.cs) | Order | The query that never publishes an event while an earlier one for the same order waits. Leasing with a conditional update so two relay instances never clash |
| [03-tenant-from-token.cs](03-tenant-from-token.cs) | Organization | The company comes only from the signed token. An invalid claim returns `null`, so filtered queries return nothing |
| [04-all-or-nothing-fulfilment.cs](04-all-or-nothing-fulfilment.cs) | Inventory | Reserve the whole basket from the agency. Only a stock shortage allows trying the whole basket at the company |
| [05-delivery-state-machine.cs](05-delivery-state-machine.cs) | Delivery | Allowed status changes kept as data. Anything not listed is refused |
| [06-email-retry-policy.cs](06-email-retry-policy.cs) | Notification | Reading SMTP replies correctly. Exponential backoff with jitter so retries after an outage do not all fire together |
| [07-route-access.ts](07-route-access.ts) | Web console | The console mirrors the server's role rules so users only see what they can use |

These files are for reading. They do not compile on their own.
