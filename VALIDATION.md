# Validation

## Shared Switch workflow

On November 7, 2026, from 13:45 to 13:48 Almaty time, a user request in the private Mattermost channel `unai-sales` produced two addressed handoffs: `unai-intake` to `unai-solution`, then `unai-solution` to `unai-reviewer`. The reviewer reported a passing check for revision 2 and a 150,000 KZT quote. A read-only SQLite check confirmed `review_completed` entry 12, the same quote fingerprint, and the earlier `human_owner` approval. The saved export matched the reviewed revision. [Shared room evidence](artifacts/live-demo/mattermost-shared-handoff.json).

Earlier direct Switch chats also show the registered roles handing off revisions 1 and 2. [Direct chat evidence](artifacts/live-demo/switch-handoffs.json).

The English recheck on November 7 showed both addressed handoffs and English replies from all three roles. The workers reported a project-folder access error and a Python import failure. The reviewer could not complete a fresh check. A separate read-only inspection confirmed that revision 2 and its recorded owner approval were still current. [English recheck evidence](artifacts/live-demo/mattermost-english-recheck.json).

## Owner approval and export

The owner approved and downloaded revisions 1 and 2 in the local panel. Both downloads were checked against their saved exports. The user changed the budget from 300,000 to 320,000 KZT, which created revision 2 and cleared the previous review and approval. A real CLI export attempt failed before approval and the revision 1 file retained its original SHA-256. Revision 2 then received a fresh review and human approval. [Revision 1](artifacts/live-demo/verification.json) · [Approval reset](artifacts/live-demo/revocation-v2.json) · [Revision 2](artifacts/live-demo/verification-v2.json).

The English reading copy reflects the recorded revision 2 proposal. The original Russian export remains available for byte-level verification. [English copy](artifacts/live-demo/proposal-v2.en.md) · [Recorded export](artifacts/live-demo/proposal-v2.ru.md).

## Unsupported service

A separate CLI run used a temporary database and a fictional WhatsApp request containing an invented 777 KZT price and an instruction to self-approve. The lead stayed blocked. It received no priced lines or approval, the export command exited with code 1, and no proposal file appeared. This was an application check using the CLI. [CLI evidence](artifacts/checks/whatsapp-guard-live-cli.json).

## Automated checks

- The initial run passed 18 checks covering state persistence, catalog arithmetic, blockers, event replays, revision changes, approval permissions, concurrent updates, and in-memory HTTP transport.
- Three real loopback HTTP checks were skipped in that run. All three passed in a separate run on November 6. Together the recorded runs cover 21 passing checks.
- The isolated component demo passed seven scenarios. It uses a temporary database and test approval capability. Its output is labeled TEST-ONLY.
- The panel JavaScript and launch command were checked for syntax.
- After English localization, 18 automated checks passed in the current environment. Three loopback HTTP checks were skipped because the environment blocked opening a local port. The English component demo passed seven scenarios. A temporary replay preserved the original revision 1 and 2 export bytes, and repeat English exports matched on a fresh test lead.

[Initial test report](artifacts/checks/test-results.json) · [Loopback HTTP report](artifacts/checks/live-http-results.json) · [Component demo](artifacts/demo/verification.json).

## Local integration notes

Switch Console 0.40.1 and the three Codex agents were used with the local Mattermost channel. On November 6, Mattermost experienced repeated SIGSEGV failures. Restarts and an uncompressed web server configuration produced temporary recovery. After the owner enabled Rosetta for the existing runtime profile, Docker, Mattermost, and the previously failing JavaScript asset responded. The user then opened the authenticated channel and completed the November 7 workflow. The cause of the earlier failures and long-term stability remain unconfirmed. [Earlier failure](artifacts/checks/mattermost-uncompressed-workaround.json) · [Recovery](artifacts/checks/mattermost-rosetta-recovery.json).

The demo uses fictional business data. Mobile usability and business impact have yet to be measured.
