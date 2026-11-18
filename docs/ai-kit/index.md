# The WitFoo AI desktop kit

The jobs shown in the WitFoo Analytics 1.2.0 launch film, ready to use with the AI assistant you already have: Claude or ChatGPT, connected to your own WitFoo appliance. This page describes what they do on WitFoo Analytics 1.2.0.

## What is in it

1. **A connection guide** for Claude and ChatGPT: turning on the MCP connector, signing in, personal keys and approvals. See [Connect Your Assistant to WitFoo](connect.md).
2. **Morning brief**: what happened since a time you name, ordered by what needs someone first, with each line naming its work unit.
3. **Incident response with playbooks**: a summary of one work unit, a suggested playbook, and an instruction to your assistant to ask before every change.
4. **Audit questionnaire**: answers from WitFoo's compliance figures, framework by framework, with failed checks stated plainly and WitFoo's remediation where WitFoo gives one.
5. **Board briefing**: an eight-slide deck in a WitFoo template, built from figures WitFoo has already worked out, with the source of every number in the speaker notes.

Jobs 2 to 5 come as Claude skills and as instructions for a ChatGPT project, with the board template and a sample questionnaire.

## What you need

- WitFoo Analytics 1.2.0 or later with Analytics Pro, Analytics Max or Reporter Pro. The incident-response job's playbooks need Analytics Pro or Max.
- MCP turned on by your appliance operator and your WitFoo administrator. See [Turn it on](connect.md#turn-it-on).
- A WitFoo account that holds **Connect MCP** (`mcp:connect`). The built-in Admin and Platform Admin roles have it; anyone else needs a custom role that includes it. Connect MCP grants no tool by itself, so that role also needs each job's permissions. See [Before you start](connect.md#before-you-start).
- A Claude or ChatGPT plan that allows custom connectors. On a Claude Team plan, an owner adds the connector in the organization's settings, and each member then connects it. On analytics 1.2.1 or later with WFA 2.5.5 or later, and the relay and app sign-in turned on, you can also add WitFoo from [Claude's directory](https://claude.ai/directory/witfoo); this kit describes the custom connector at your appliance's own address, which is how you connect on 1.2.0.

## The four jobs

Each job is a Claude skill, in its own ZIP file. The same four jobs are in the ChatGPT files further down.

### Morning brief

Builds a shift handover from the work units created since a time you name, ordered by what needs a person first, with each unit named by its title and ID. It counts only what WitFoo returned, says how it ranked the units, and says that units created earlier and changed in the period are not included. The job only reads; on an app connection approved read-only, WitFoo refuses changes.

[:material-download: Morning brief skill (.zip)](downloads/witfoo-morning-brief-1.0.zip){ download="witfoo-morning-brief-1.0.zip" }

### Incident response with playbooks

Summarizes one work unit from its structured evidence, suggests one of your organization's playbooks, says what a run does on this release, and then stops and asks. The job tells your assistant to ask before every change (running a playbook, adding a note, assigning the unit or changing its status), and never to claim that anything was isolated, blocked, reset or quarantined. These are instructions to your assistant, not limits the appliance enforces; see [What the AI sees](#what-the-ai-sees). On 1.2.0 a playbook run opens response tasks; people do the rest.

[:material-download: Incident response skill (.zip)](downloads/witfoo-incident-response-1.0.zip){ download="witfoo-incident-response-1.0.zip" }

### Audit questionnaire

Fills in a security questionnaire you attach or paste, keeping its questions and order. For each question it gives an answer, the framework and WitFoo's figure for it, the evidence, and WitFoo's remediation where one of WitFoo's cloud-configuration checks gives one. It uses only the standings WitFoo reported, claims no control, certification or attestation WitFoo did not report, and marks a question it cannot answer as needing a person. The job only reads; on an app connection approved read-only, WitFoo refuses changes. Try it with the sample questionnaire below.

[:material-download: Audit questionnaire skill (.zip)](downloads/witfoo-audit-questionnaire-1.0.zip){ download="witfoo-audit-questionnaire-1.0.zip" }

### Board briefing

Builds an eight-slide deck in the WitFoo board template from WitFoo's latest executive figures, cost and savings, compliance standing and significant work units, with the source and report date of every number in the speaker notes. WitFoo reports its latest figures, not a period you choose, so the deck says the date its figures are as of. It is told to invent no figure, trend or comparison. The job only reads; on an app connection approved read-only, WitFoo refuses changes. The template is inside the ZIP.

[:material-download: Board briefing skill (.zip)](downloads/witfoo-board-briefing-1.0.zip){ download="witfoo-board-briefing-1.0.zip" }

!!! note "On a read-only connection"
    In 1.2.0, a work unit's response tasks, notes and assignments, and the list of playbooks, are read through tools that WitFoo marks as able to make changes. An app you approved read-only is refused them. The morning brief and the board briefing then say so in their answer. The incident-response job needs changes allowed. See [When the assistant wants to change something](connect.md#when-the-assistant-wants-to-change-something).

### Add a skill to Claude

1. In Claude, open **Customize** > **Skills**.
2. Click **+**, then **Create skill**, then **Upload a skill**, and choose the ZIP file. Do not unzip it.
3. Turn the skill on.

Skills need Claude's code execution and file creation turned on. On a Team or Enterprise plan, an owner can also provision a skill for everyone in the organization. Claude changes its menu names from time to time; these are as of November 2026.

### Use the jobs in ChatGPT

1. Create a project in ChatGPT.
2. Paste the text of the ChatGPT instructions file into the project's instructions.
3. Add the ChatGPT jobs file to the project's files. For the board briefing, add the board template too.
4. In a chat in the project, type `@`, choose WitFoo, and ask for the job you want.

[:material-download: ChatGPT instructions (.txt)](downloads/witfoo-chatgpt-instructions-1.0.txt){ download="witfoo-chatgpt-instructions-1.0.txt" } · [:material-download: ChatGPT jobs (.txt)](downloads/witfoo-chatgpt-jobs-1.0.txt){ download="witfoo-chatgpt-jobs-1.0.txt" }

## Downloads

| File | What it is | Size |
| --- | --- | --- |
| [witfoo-morning-brief-1.0.zip](downloads/witfoo-morning-brief-1.0.zip){ download="witfoo-morning-brief-1.0.zip" } | Claude skill: morning brief | 1.9 KB |
| [witfoo-incident-response-1.0.zip](downloads/witfoo-incident-response-1.0.zip){ download="witfoo-incident-response-1.0.zip" } | Claude skill: incident response with playbooks | 2.3 KB |
| [witfoo-audit-questionnaire-1.0.zip](downloads/witfoo-audit-questionnaire-1.0.zip){ download="witfoo-audit-questionnaire-1.0.zip" } | Claude skill: audit questionnaire | 1.5 KB |
| [witfoo-board-briefing-1.0.zip](downloads/witfoo-board-briefing-1.0.zip){ download="witfoo-board-briefing-1.0.zip" } | Claude skill: board briefing, with the board template | 46 KB |
| [witfoo-chatgpt-instructions-1.0.txt](downloads/witfoo-chatgpt-instructions-1.0.txt){ download="witfoo-chatgpt-instructions-1.0.txt" } | Instructions to paste into a ChatGPT project | 1.1 KB |
| [witfoo-chatgpt-jobs-1.0.txt](downloads/witfoo-chatgpt-jobs-1.0.txt){ download="witfoo-chatgpt-jobs-1.0.txt" } | The four jobs, as a file for a ChatGPT project | 14 KB |
| [WitFoo_Board_Briefing_Template-1.0.pptx](downloads/WitFoo_Board_Briefing_Template-1.0.pptx){ download="WitFoo_Board_Briefing_Template-1.0.pptx" } | The eight-slide board template (the same file is in the board briefing skill) | 54 KB |
| [WitFoo_Sample_Security_Questionnaire-1.0.xlsx](downloads/WitFoo_Sample_Security_Questionnaire-1.0.xlsx){ download="WitFoo_Sample_Security_Questionnaire-1.0.xlsx" } | A 25-question sample questionnaire, written by WitFoo for demonstration and not taken from any published standard | 6.6 KB |

The board template uses the IBM Plex Sans and Poppins fonts, which are not embedded. Where they are not installed, PowerPoint shows a substitute font.

## What the AI sees

- **Only what your WitFoo account can see.** Every connection acts as one WitFoo user, and that user's permissions are checked on every request.
- **An app that signs in through your appliance reads only**, unless you also let it make changes on your appliance's approval page, and your organization allows that. Once you allow changes, the appliance does not ask again for each change; the kit's jobs tell your assistant to ask you before every change.
- **A personal key acts with all of your permissions**, with no read-only limit.

## Where your data goes

- **Direct connection.** When you add WitFoo as a connector in Claude or ChatGPT, the AI provider's servers make the calls to your appliance. A client on your own computer that uses a personal key calls it from your computer. At your appliance's own address, nothing passes through WitFoo.
- **The optional relay.** If your AI provider cannot reach your appliance and you cannot open an inbound port, WitFoo Analytics 1.2.0 has an optional AI-connector relay. It is off by default for every organization and every appliance, and only an operator at the appliance can turn it on: with WFA 2.5.1 or later, run `wfa mcp-relay enable`, read WitFoo's relay notice, type `ENABLE`, then run `wfa restart`. The appliance keeps one outbound HTTPS connection to `mcp-relay.witfoo.com` and gets its own relay address, `https://mcp-relay.witfoo.com/h/<handle>/mcp`.
    - For Claude or ChatGPT to sign in through the relay, leave `mcp_public_url` empty before you run `wfa mcp-relay enable`; `enable` then sets it to the relay address, and that is the address you give the app. If `mcp_public_url` already holds another address, app sign-in stays on that address and is not offered through the relay. Set `mcp_oauth_ui_url` as usual: the approval page is not relayed, so your browser must reach the WitFoo web interface.
    - Relayed requests and answers pass through WitFoo's relay service, which reads each one in memory only while it passes it on, and writes none of the content, tokens or keys to its database or logs. Its logs record, for each request, a request identifier, the address's handle, the method, the path, the time, the status, the sizes, the duration and the outcome, and are kept for 30 days. Until the address is revoked, the relay also keeps your organization and appliance identifiers and the name your appliance gave as the person who turned it on. Backups of the relay's database are kept for 35 days. The notice lists everything the relay keeps.
    - The relay's address is served through Cloudflare, which ends the encrypted connection at its network edge and can see what passes through.
    - The relay is separate from WitFoo's licensing service.
    - An air-gapped or privacy-sensitive deployment should leave it off. ChatGPT has not yet been verified through the relay.
    - The full notice and the steps are in [AI-Connector Relay](../ai/mcp/relay.md).
- **Your AI provider.** Either way, the results of each question go to the AI assistant you connected, and that assistant's provider handles them under its own terms. Choose your assistant the way you would choose any vendor.

## Why it uses fewer tokens

WitFoo does the work before the AI does. Your assistant reads structured work units and finished figures instead of raw logs, so each question needs far fewer tokens than sending the raw evidence would. Read why in [The AI cost collision in cybersecurity](https://www.witfoo.com/research/ai-cost-collision/).

---

*Claude is a trademark of Anthropic, PBC. ChatGPT is a trademark of OpenAI. Other product names are trademarks of their owners, used here only to identify the products. No endorsement or partnership is implied.*
