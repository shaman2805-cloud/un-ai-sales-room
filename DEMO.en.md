# UN AI Sales Room · Two-minute demo

Record this walkthrough once the English recheck appears in `unai-sales` with both addressed handoffs and a passing revision 2 review. Open the English owner panel on Alma Studio's approved revision 2, the English proposal translation and the saved budget-change evidence. Use the earlier approval already shown in the panel. Keep the launcher and its private access link outside the recording area.

## Recording script

### 0:00–0:15 · The problem

**Show.** The project title in the owner panel.

**Say.** “Service teams often start with a rough request. UN AI Sales Room turns it into a checked quote that the business owner can approve.”

### 0:15–1:00 · Switch handoffs

**Show.** Scroll through the English recheck in the private Mattermost channel `unai-sales`. Start with the owner's request to review the existing revision 2. Pause on the addressed handoff from `unai-intake` to `unai-solution`, the calculation of 120,000 plus 30,000 KZT, and the handoff to `unai-reviewer`. Stop on the reviewer’s passing result.

**Say.** “Here is the actual run in Mattermost. The intake agent passes the request to the solution agent. It checks the catalog and hands the quote to the reviewer. The reviewer confirms revision two and a passing total of one hundred and fifty thousand tenge. Switch keeps each handoff visible in the shared conversation.”

### 1:00–1:35 · Owner approval and proposal

**Show.** In the English owner panel, pause on **Approved**, **Revision 2**, the 320,000 KZT budget and the 150,000 KZT quote. Open the English translation of the saved revision 2 proposal. Keep its translation label visible. [English proposal](artifacts/live-demo/proposal-v2.en.md).

**Say.** “The owner approved this revision earlier in the private panel. The recheck keeps that approval and the same quote fingerprint. This is the English translation of the saved proposal. The total is one hundred and fifty thousand tenge, against a budget of three hundred and twenty thousand.”

### 1:35–1:55 · Budget change and version history

**Show.** Open the saved budget-change evidence. Highlight `approval_cleared: true`, `export_exit_code: 1`, and `historical_version_1_file_unchanged: true`.

**Say.** “Earlier, a budget change created revision two and cleared the previous approval. Export was blocked until the owner approved the new revision. The first proposal stayed in the history.”

### 1:55–2:00 · Closing frame

**Show.** Return to the English proposal translation.

**Say.** “All customer details and prices in this demo are fictional.”

## Fallback with English captions

If the English recheck is still pending when you record, use the verified November 7 history from 13:45–13:48 Almaty time. Keep the English narration, owner panel and proposal translation. Add these captions beside the relevant posts. [Verified earlier run](artifacts/live-demo/mattermost-shared-handoff.json).

- Owner request — **Review existing revision 2**
- Intake handoff — **Intake → Solution**
- Solution handoff — **Solution → Reviewer**
- Reviewer result — **Revision 2 · Review passed · 150,000 KZT**

The original export and earlier approval remain the source evidence for the translation. The separate WhatsApp guard check ran through the CLI and can stay in the written validation. [Owner approval and download](artifacts/live-demo/verification-v2.json) · [Original revision 2 proposal](artifacts/live-demo/proposal-v2.ru.md) · [Budget-change evidence](artifacts/live-demo/revocation-v2.json) · [CLI check](artifacts/checks/whatsapp-guard-live-cli.json).
