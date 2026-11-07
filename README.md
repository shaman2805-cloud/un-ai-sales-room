# UN AI Sales Room

UN AI Sales Room turns a service request into a priced proposal. Three Codex agents pass the work through a shared Switch room in Mattermost. The business owner approves a specific revision in a private local panel before export.

## Workflow

1. `unai-intake` records the request and asks for missing information.
2. `unai-solution` matches the scope to the catalog. The application calculates the price in KZT.
3. `unai-reviewer` runs the application checks and reports the revision, total, and blockers.
4. The owner approves the reviewed revision in the panel. The application saves a versioned proposal and an audit trail.

Changing the scope, budget, or catalog clears the previous review and approval. Approval requires the owner session and binds to a specific revision and quote fingerprint. Repeated deliveries with the same event ID reuse the previous result.

## Verified demo

On November 7, the owner asked the intake agent to recheck an existing fictional request in the private `unai-sales` Mattermost channel. Both addressed handoffs appeared in the channel. The reviewer confirmed revision 2 at **150,000 KZT**. The recorded review, earlier human approval, and saved export share the same quote fingerprint. [Shared room evidence](artifacts/live-demo/mattermost-shared-handoff.json).

In a separate owner run, a budget edit from 300,000 to 320,000 KZT created revision 2, revoked the earlier approval, and blocked export until fresh review and owner approval. A separate CLI check also blocked an unsupported WhatsApp request containing an invented price and an instruction to self-approve. [Approval reset](artifacts/live-demo/revocation-v2.json) · [WhatsApp check](artifacts/checks/whatsapp-guard-live-cli.json).

The examples and prices are fictional. The prototype runs locally and does not send customer messages or connect to CRM, payments, or WhatsApp.

[English demo script](DEMO.en.md) · [English proposal translation](artifacts/live-demo/proposal-v2.en.md) · [Validation](VALIDATION.md)

## Run locally

Requires Python 3.10 or later. The application uses the Python standard library.

```sh
python3 -m salesroom serve --open
```

The owner panel listens on `127.0.0.1:8787`. If needed, select another port with `--port 8788`. Open the owner panel before onboarding the agents so the application can bind its local approval key. Keep the bootstrap link and owner credentials private.

For the shared workflow, start Switch Console with Codex and Mattermost, register the three roles from `switch/agents/`, and add them to `unai-sales`. All three roles use the same project directory. [Switch setup](switch/SETUP.md).

## CLI and tests

```sh
python3 -m salesroom create --event-id example-intake-1 --input examples/lead.complete.json
python3 -m salesroom get LEAD_ID
python3 -m salesroom review LEAD_ID --event-id example-review-1
python3 -m salesroom audit LEAD_ID
python3 -m salesroom export LEAD_ID
```

Replace `LEAD_ID` with the ID returned by `create`. Export becomes available after approval in the owner panel. For edits, use `update LEAD_ID --event-id UNIQUE_ID --input changes.json`. A replay uses the same event ID and payload.

```sh
python3 -m unittest discover -s tests -v
python3 tools/run_demo.py
```

The component demo uses an isolated database and test approval capability. Its output is labeled TEST-ONLY. The recorded Mattermost run and human owner approval are documented separately.

Runtime data and credentials stay in `runtime/` and `.switch/`, outside the source package. The archived catalog and original exports retain their source text for fingerprint verification. The English proposal translation is a reading copy for judges. The local prototype assumes a trusted machine.

## Hackathon

Persistent state, approval checks, the owner panel, proposal export, and the Switch workflow were implemented during Flip the Switch. The earlier starter provided role prompts and templates. [Official schedule](https://www.wemakedevs.org/hackathons/switch/schedule) · [Official rules](https://www.wemakedevs.org/hackathons/switch/rules).
