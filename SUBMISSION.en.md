# UN AI Sales Room

**Track:** Best Business Workflow

**One sentence:** Turn a customer request into a checked, versioned proposal that an owner explicitly approves before export.

## Problem

Service teams receive incomplete requests and may promise unsupported integrations or unverified prices. An AI answer alone cannot establish feasibility or owner approval.

## Implemented solution

Python stores leads, catalogue snapshots, revisions and audit events in SQLite. Checks validate required information, quantities, prices and budget. An isolated CLI run kept WhatsApp blocked despite a quoted 777 KZT price and self-approval instruction. Export returned an error and created no file. [CLI evidence](artifacts/checks/whatsapp-guard-live-cli.json).

The owner approves a specific revision and quote fingerprint in a private browser panel. The application requires the owner session for that action. Changes to scope, budget or catalogue content invalidate earlier approval. Repeated event IDs reuse the original result.

A budget edit to 320,000 KZT created revision 2, revoked approval and blocked export. After fresh review and owner approval, the downloaded **150,000 KZT** proposal matched the saved export and new quote hash. Revision 1 is preserved. Data and prices are fictional.

## Role of Switch

On November 7, the owner initiated a run in Mattermost `unai-sales`. Switch carried two addressed handoffs from intake through solution to reviewer. The reviewer passed revision 2 at 150,000 KZT. Audit entry 12 matches the existing human approval and saved export. [Shared-room evidence](artifacts/live-demo/mattermost-shared-handoff.json).

## New work and reproducibility

The earlier starter contained role prompts and templates. Persistent state, checks, the owner panel, exports and Switch setup are new event work.

Across the recorded runs, 21 automated checks passed. [README](README.md) · [Switch setup](switch/SETUP.md) · [Validation](VALIDATION.md) · [English demo script](DEMO.en.md).

## Current limitations and submission prerequisites

The prototype runs locally with fictional data. CRM, WhatsApp, payments and customer sending are outside its scope. Mobile usability, business impact, and long-term stability remain unmeasured.

The demo script covers the verified handoffs, the approved revision, and the export guard. The English reading copy is a translation of the recorded proposal. [Proposal translation](artifacts/live-demo/proposal-v2.en.md).

**Public repository URL:** pending.

**Demo video URL:** pending.
