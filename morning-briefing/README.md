# Morning Briefing Skill

A Claude skill that generates a daily **interactive kanban dashboard** from your emails, calendar, and tasks — as a standalone HTML file you can open in any browser.

Built for AI architects, product people, and anyone juggling multiple tools and inboxes.

---

## What you get

Every morning, one command → one HTML file:

```
start my day
```

Claude pulls from your connected sources, classifies everything into **Todo / In Progress / Done**, and produces a board you can actually interact with:

- Drag cards between columns
- Add tasks manually with the `+` button
- Delete cards on hover with `✕`
- Click links directly to Gmail threads, GitHub issues, Monday tasks, etc.

---

## Requirements

- [Claude for Desktop](https://claude.ai/download) with **Cowork mode** enabled, or [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI

No other dependencies. The output HTML file is fully self-contained — no internet connection needed to open it.

---

## Installation

### Option A — Cowork (Desktop app)

1. Open Claude for Desktop → Cowork mode
2. Go to **Plugins → Install from file**
3. Select `morning-briefing.skill`
4. Done — the skill is now available in all Cowork sessions

### Option B — Claude Code (CLI)

1. Copy the `morning-briefing/` folder into your skills directory:

```bash
# macOS / Linux
cp -r morning-briefing/ ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse morning-briefing\ "$env:APPDATA\Claude\skills\"
```

2. Restart Claude Code or reload skills:

```bash
claude --reload-skills
```

3. Verify it's active:

```bash
claude skills list
```

You should see `morning-briefing` in the list.

---

## Connecting data sources

The skill works with any combination of sources. Connect what you have — the skill adapts.

### Gmail

1. In Cowork → **Plugins → Connectors → Gmail → Connect**
2. Authorize with your Google account
3. Claude will now auto-pull your inbox when generating the briefing

### Google Calendar

1. In Cowork → **Plugins → Connectors → Google Calendar → Connect**
2. Authorize with your Google account
3. Today's events will appear on the board automatically

### Monday.com

1. In Cowork → **Plugins → Connectors → Monday.com → Connect**
2. Enter your Monday API token when prompted
3. Your open tasks will be pulled automatically

---

## Using with Outlook (and other tools without a connector)

No connector needed — just paste.

**Outlook:**
1. Open your inbox
2. Select the emails you want to include, copy the subject lines (or the full preview)
3. Paste into Claude:

```
start my day — here are my emails:
[paste]
```

**Obsidian daily note:**
```
start my day — here's my daily note:
[paste your note]
```

**Any combination:**
```
start my day.

Outlook emails:
[paste]

Monday tasks:
[paste]

Notes from yesterday:
[paste]
```

Claude parses everything — free-form text, markdown checkboxes (`- [ ]`), email threads, whatever you give it.

---

## Example prompts

All of these trigger the skill:

```
start my day
```
```
תתחיל את היום שלי
```
```
what's on my plate today?
```
```
morning briefing
```
```
make me a kanban from my inbox
```
```
daily standup prep
```
```
organize my tasks for today — here's my Outlook: [paste]
```

---

## Scheduling (optional)

To run the briefing automatically every morning:

```
set up my morning briefing every day at 7:30am
```

Claude will configure a scheduled task that generates the HTML file each morning before you start work.

---

## Output

The skill saves a file named `morning_briefing_YYYY-MM-DD.html` to your outputs folder. Open it in any browser — Chrome, Firefox, Edge, Safari. No server needed.

---

## How it classifies items

| Signal | Column |
|--------|--------|
| Requires a reply, fix, or decision | **Todo** |
| Ongoing work, pending approval, event to prep for | **In Progress** |
| Confirmations, order receipts, FYI items | **Done** |
| Newsletters, promotions | Grouped into one card (or skipped) |

Priority badges:
- 🔴 **Urgent** — deadline today, error, escalation
- 🟡 **Medium** — needs attention this week
- 🔵 **Opportunity** — freelance lead, project, event
- 🟢 **Event** — calendar item, meetup
- ⚪ **General** — everything else

---

## Supported sources

| Source | Method |
|--------|--------|
| Gmail | Auto (MCP connector) |
| Google Calendar | Auto (MCP connector) |
| Monday.com | Auto (MCP connector) |
| Microsoft Outlook | Paste in chat |
| Obsidian | Paste daily note |
| Notion, Linear, Jira, etc. | Paste exported content |
| Any text / task list | Paste anything |

---

## Troubleshooting

**The skill doesn't trigger automatically**
→ Try being more explicit: "use the morning briefing skill" or "generate my daily kanban dashboard"

**Gmail / Calendar not pulling**
→ Check that the connector is authorized: Cowork → Connectors → verify status is "Connected"

**Drag and drop not working**
→ Open the file in a browser (not a preview pane). Chrome and Edge work best.

**The board is empty**
→ No connected sources were found. Paste your content directly in the chat.

---

## Customization

Want to tweak the skill for your team? Edit `SKILL.md`:

- **Change columns** — modify the column logic in Step 2
- **Add a source** — add a row to the "Supported sources" table and describe how to parse it
- **Change the design** — edit the badge colors or layout in Step 3
- **Add fields to cards** — describe what additional info to show (e.g., due date, assignee)

---

## License

Free to use, share, and adapt. Built with Claude — [claude.ai](https://claude.ai)
