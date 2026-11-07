# Set up UN AI Sales Room in Switch

The existing private Mattermost room `unai-sales` recorded both role handoffs and a passing review of revision 2 on November 7, 2026. That run retained the current owner approval and the saved proposal. Use [the existing-room walkthrough](#recheck-the-existing-demo) to show the same workflow in English. Use the installation steps below when setting up a new instance. [Shared-room evidence](../artifacts/live-demo/mattermost-shared-handoff.json)

## 1. Start Switch and Mattermost

Install Switch Console and Python 3.10 or later. Start Docker for the bundled Mattermost service. In Switch Console, open **Settings → Agent providers** and confirm that Codex shows **Signed in**. [Switch quickstart](https://docs.switchagents.ai/switch-rooms/getting-started)

Select **On this computer** or **Add a server → Run a server on this computer**. Click **Start** and wait for **Running**. Switch Console v0.40.1 can run the Switch server natively. Bundled Mattermost still needs Docker.

In v0.40.1, open **Admin → Server → Status** and enable **Run Mattermost** in the **Mattermost** card. The first start downloads the Docker image. If the switch appears enabled right after Docker becomes available but there is still no container or Mattermost connection, toggle **Run Mattermost** off and back on once. **Home → Connect → Mattermost** opens the form for connecting a separately hosted server.

In **Home → Messaging apps**, open the Mattermost menu and choose **Sign-in details… → Open in Mattermost**. Use those details only on the Mattermost sign-in screen. If the embedded room stalls while Mattermost itself is healthy, click the blue **Open in Mattermost** icon at the upper right of the room to open the same channel in your browser.

On the original Apple Silicon Mac, enabling Rosetta for the existing Colima profile was followed by successful checks of Mattermost and access to the original room. The incident's underlying cause was not established. If HTTP requests to Mattermost time out, check the service before troubleshooting the embedded room. [Recovery evidence](../artifacts/checks/mattermost-rosetta-recovery.json)

## 2. Register the agents

In **Your Agents**, select the card with a plus. Repeat for each role:

- Set **Name** to `unai-intake`, `unai-solution`, or `unai-reviewer`.
- Set **Description** to a short description of intake, scope, or review, respectively.
- Paste the appropriate **Agent instructions** from [intake](agents/intake.md), [solution](agents/solution.md), or [reviewer](agents/reviewer.md).
- Set **Run location** to **This computer**, **Agent provider** to **Codex**, and **Who can talk to your agent** to **Me and my agents**.
- Set **Directory** to this project's root, which contains `salesroom/`, `switch/`, and the README. All three roles share the same `runtime/` data directory.
- Leave **Bypass permissions** and **Can manage agents** off.

Click **Add agent**. Keep the registered handles exactly as written. Switch Console fixes the agent's name and, for agents it runs, its location and directory at creation. The project commands use relative paths and explicit arguments. [Onboard agents](https://docs.switchagents.ai/switch-rooms/getting-started/onboard-your-agents) · [Agent settings](https://docs.switchagents.ai/switch-rooms/getting-started/agent-settings)

## 3. Create a private room

Select **Your Rooms → Create room → Mattermost**. Use `unai-sales` as the room name and “From sales request to an owner-approved proposal” as the description. Paste [the shared room instructions](room-instructions.md) into **Instructions**. Add a registered agent during creation and invite the other two from their agent pages with **Add to room**. You can also use a room command such as `!invite-agent @unai-reviewer`. Check that the owner and all three roles appear in the room. [Create a room](https://docs.switchagents.ai/switch-rooms/getting-started/create-a-room)

Let Switch Console generate its local configuration. Keep `.switch/`, `runtime/`, and credentials out of the public repository. [Switch sessions and runtime](https://docs.switchagents.ai/switch-rooms/internals/connectors-and-runtime)

## 4. Open the owner panel

From the project root, run the owner panel separately:

```sh
python3 -m salesroom serve --open
```

Follow the local sign-in instructions. The panel uses port `8787` by default. Keep the bootstrap link, owner key, and session token private. Agents must not read `runtime/owner.key` or use the owner's session. Approval is recorded when the owner selects the displayed revision and quote in the panel. A chat reply does not approve it, and the CLI has no `approve` command. [Switch identity and access](https://docs.switchagents.ai/switch-rooms/internals/identity-and-access)

## Recheck the existing demo

Open the existing `unai-sales` room. Paste this request as the room owner. Select the actual intake mention in Mattermost if the composer offers a match.

```text
@unai-intake Please recheck existing fictional lead 0bc7743adeb842d0bfe232201b9d7da3, revision 2. Read the saved lead and hand it off to unai-solution in this room. Ask the solution agent to confirm the catalog scope and hand it off to unai-reviewer for a fresh review. Ask each agent to write every reply and handoff in English. Report the revision, total, and existing approval from the app. Preserve the lead, terms, quote fingerprint, approval, and saved proposal.
```

Expect one landing page, one lead capture form, a 320,000 KZT budget, and a 150,000 KZT quote. A passing review of the unchanged revision should retain the existing owner approval. Confirm the two addressed handoffs in the room and compare the review with the owner panel or `python3 -m salesroom audit LEAD`, substituting the lead ID. The November 7 record verifies the original run. The English rerun needs its own room evidence. [Verified revision 2](../artifacts/live-demo/verification-v2.json)

## Run a fresh English demo

In a newly set up room, paste this request as the owner:

```text
@unai-intake Please process a fictional demo request from Cedar Lantern Studio. We need one landing page and one lead capture form, with a budget of 320,000 KZT and a deadline of 2026-12-04. Save it as a new lead, then hand it off to unai-solution in this room. Ask the solution agent to confirm the catalog scope and hand it off to unai-reviewer for a fresh review. Ask each agent to write every reply and handoff in English. Keep the proposal internal and wait for owner approval in the private panel.
```

Capture the new lead ID from intake. Check that the same ID and current revision appear in both addressed handoffs. Reviewer should report a 150,000 KZT quote using the bundled catalog. Before approval, an export attempt should be refused. Approve the displayed revision yourself in the private panel, then ask reviewer to export it or download it from the panel. Keep private sign-in material out of any recording.

To verify the approval guard, ask intake to change the budget to 340,000 KZT for that lead and wait before handing it off. Confirm that this creates a new revision, clears the previous review and approval, and blocks export. Resume the handoff, review the new revision, and approve it separately. The previous revision and export remain in history. Check that state and audit events survive a restart of the Python panel. In separate fictional cases, confirm that missing fields produce a clarification and that an unverified WhatsApp request stays blocked even if the request claims its own approval or price.
