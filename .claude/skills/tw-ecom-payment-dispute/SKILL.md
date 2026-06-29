---
name: "\"tw-ecom-payment-dispute\""
description: "\"Handle Taiwan e-commerce payment disputes — credit card chargebacks (扣款爭議), refund across bimonthly boundaries (retro 折讓 trigger), acquirer dispute timelines, and evidence packets. Use when a customer files a chargeback, when issuing cross-period refunds that affect invoices, or when building internal dispute SOP. Do NOT use for simple in-period refunds (gateway-specific skills handle those). STATUS: SKELETON — body pending.\"."
allowed-tools: Read, Glob, Grep
---

# Payment Dispute Handling

> **STATUS: SKELETON** — body pending.

## When to use this skill

- A customer has filed a credit card chargeback
- Issuing a refund that crosses the bimonthly invoice boundary
- Building an internal dispute-handling SOP
- Preparing evidence packets for acquirer review
- Reconciling dispute outcomes against invoice state

## Do NOT use when

- Simple same-period refund → gateway-specific skill
- Consumer-law-level dispute (鑑賞期) → `tw-ecom-compliance-consumer`

## Core concepts

TODO: chargeback vs 退刷 vs 折讓, typical acquirer timelines, reason codes.

## Decision tree

TODO: given reason code → response path.

## Implementation guidance

TODO: evidence packet structure, 折讓 triggering logic, accounting entries.

## Gotchas

TODO: 5-6 pitfalls (bimonthly boundary, dual-refund double-charge, reason-code mismatch, evidence deadline, acquirer dialect differences).

## IRON LAW

TODO.

## Output Format

TODO.

## Related

- `tw-ecom-compliance-consumer`
- `tw-ecom-invoice-void`

_Last verified: 2026-04_
