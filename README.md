# Morning Briefing Dashboard — Claude Skill

> A Claude skill that turns your emails, calendar, and tasks into a **drag-and-drop kanban board** — every morning, as a standalone HTML file.

![Morning Briefing Dashboard](screenshot.png)

---

## What it does

One prompt → one interactive HTML file:

```
start my day
```

Claude pulls from your connected sources, classifies everything by urgency, and builds a board you can work with directly in your browser:

| Feature | Details |
|---------|---------|
| 📋 Drag & drop | Move cards between **Todo / In Progress / Done** |
| ➕ Add tasks | `+` button in each column — title + priority tag |
| ✕ Delete | Hover over any card to reveal the delete button |
| 🔗 Deep links | Cards link directly to Gmail threads, GitHub issues, Monday tasks |
| 🎭 Data masking | Personal emails and IDs masked in shared/demo views |
| 🌐 Zero dependencies | Fully self-contained HTML — no server, no npm, no internet needed |

---

## Screenshot

![kanban board with Todo, In Progress, and Done columns](screenshot.png)

*Personal data masked. Real board pulls live from your connected sources.*

---

## Integrations

The skill works with any combination of the following — mix and match:

### Auto-pull (MCP connectors)

| Source | What gets pulled |
|--------|-----------------|
| **Gmail** | Inbox threads from the last 2 days |
| **Google Calendar** | Today's events |
| **Monday.com** | Open items assigned to you |

### Paste-in (no connector needed)

| Source | How |
|--------|-----|
| **Outlook** | Copy email subjects/previews → paste in chat |
| **Obsidian** | Paste your daily note — parses `- [ ]` checkboxes automatically |
| **Notion / Linear / Jira** | Paste exported task list |
| **Any text** | Free-form — Claude figures it out |

---

## Installation

### Option A — Cowork (Claude Desktop, recommended)

1. Download `morning-briefing.skill` from the [Releases](../../releases) page
2. Open **Claude for Desktop** → Cowork mode
3. Go to **Plugins → Install from file**
4. Select `morning-briefing.skill`

### Option B — Claude Code (CLI)

```bash
# macOS / Linux
cp -r morning-briefing/ ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse morning-briefing\ "$env:APPDATA\Claude\skills\"
```

Then verify:

```bash
claude skills list
# → morning-briefing ✓
```

### Option C — Manual (copy SKILL.md)

Copy the contents of `SKILL.md` into your Claude project's `CLAUDE.md`, or drop the `morning-briefing/` folder anywhere Claude Code looks for skills.

---

## Connecting data sources

### Gmail & Google Calendar

1. In Cowork → **Plugins → Connectors**
2. Click **Connect** next to Gmail / Google Calendar
3. Authorize with your Google account

### Monday.com

1. In Cowork → **Plugins → Connectors → Monday.com → Connect**
2. Enter your Monday API token

### Outlook / other tools

No connector needed — just paste:

```
start my day — here are my Outlook emails:
[paste]
```

---

## Usage

All of these trigger the skill:

```
start my day
```
```
morning briefing
```
```
what's on my plate today?
```
```
make me a kanban from my inbox
```
```
daily standup prep
```
```
organize my tasks — here's my Outlook: [paste]
```

### Scheduling (run automatically every morning)

```
set up my morning briefing every day at 7:30am
```

Claude configures a scheduled task — the HTML file is ready before you start work.

---

## How cards are classified

| Signal | Column |
|--------|--------|
| Requires a reply, fix, or decision | **Todo** |
| Ongoing, pending approval, event to prepare for | **In Progress** |
| Confirmations, FYI, order receipts | **Done** |
| Newsletters & promotions | Grouped into one card (or skipped) |

Priority badges:

| Badge | When |
|-------|------|
| 🔴 Urgent | Deadline today, CI failure, escalation |
| 🟡 Medium | Needs attention this week |
| 🔵 Opportunity | Freelance lead, relevant project |
| 🟢 Event | Calendar event, approved registration |
| ⚪ General | Everything else |

---

## Output

Saved as `morning_briefing_YYYY-MM-DD.html` in your outputs folder. Open in any browser — Chrome, Firefox, Edge, Safari. No internet required.

---

## Customization

Edit `SKILL.md` to adjust for your team:

- **Add a source** — add a row to the integrations table and describe how to parse it
- **Change columns** — rename or add columns in Step 2 of the skill
- **Change card fields** — add due date, assignee, project name, etc.
- **Design** — edit badge colors or layout in Step 3

---

## File structure

```
morning-briefing/
├── SKILL.md          ← Claude's instructions (the skill itself)
├── README.md         ← This file
morning-briefing.skill ← Packaged skill for one-click install
screenshot.png        ← Demo screenshot (data masked)
```

---

## Built with

- [Claude](https://claude.ai) — Anthropic's AI
- [Cowork](https://claude.ai/download) — Claude's desktop automation mode
- Pure HTML/CSS/JS — no frameworks, no build step

---

## License

MIT — free to use, share, and adapt.
