# Pilot case P

A throwaway case for the pilot only. It is not in the form and is never used in the main run, so its key is public.

## Case

### Case P: a refund spike

A merchant account, M, sells event tickets. You are asked whether M is sending refunds to cards it controls.

- In the past week, M's refunds rose from about 1 percent to 6 percent of its sales.
- A search of M's refunds over the past 30 days returned 120 refunds, all to cards issued in one country.
- The platform's refund-abuse check scored M at 10:00 on Monday and did not flag it. A card that received refunds from M is linked to a closed account; the link took effect at 09:40 on Monday.

P1. Did M send no refunds to cards from other countries in the past 30 days? Yes / No / Cannot tell

P2. Did the refund-abuse check miss evidence that was available to it when it scored M? Yes / No / Cannot tell

P3. Does the rise from 1 to 6 percent warrant review? Yes / No / Cannot tell

## Records

- Coverage of the 30-day refund search, written by the query service: requested 30 days ago to now; evaluated 12 days ago to now; status partial.
- Learned times: link of the card to the closed account, effective 09:40 Monday, learned 15:00 Monday.

## Filler

- Coverage of the search for M's support tickets, written by the query service: requested 30 days ago to now; evaluated 30 days ago to now; status complete.
- Learned times: change of M's business address, effective 3 months ago, learned 3 months ago.

## Key

| Item | Supported | Counted error | Requirement |
|---|---|---|---|
| P1 | Cannot tell | Yes | C2 coverage |
| P2 | No | Yes | C2 learned time |
| P3 | Yes | No | Control |

"Cannot tell" is also supported for P2; without the learned time, the record does not show when the link became known.
