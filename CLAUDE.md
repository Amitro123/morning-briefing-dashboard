# Morning Briefing — Claude Skill Instructions

This file is the source of truth for the `morning-briefing` Claude skill.
It is automatically loaded when the skill is active.

---

## Skill identity

**Name:** `morning-briefing`

**Triggers on:** "start my day", "morning briefing", "what's on my plate today", "daily dashboard", "standup prep", "kanban from my emails", "organize my tasks", any pasted block of emails or tasks. Trigger even if the user doesn't name the skill explicitly.

---

## What this skill produces

A self-contained interactive HTML file saved to the outputs folder:
- Drag-and-drop kanban board (Todo / In Progress / Done) using mouse events
- Cards auto-populated from connected sources or pasted content
- `+` button per column to add tasks manually (title + priority tag)
- `✕` delete on hover
- Direct links to source items where available
- Filename: `morning_briefing_YYYY-MM-DD.html`

---

## Step 1 — Gather data

Pull from all available sources in parallel.

### Connected MCP sources (use if tools are available)

| Source | Tool | Query |
|--------|------|-------|
| Gmail | `search_threads` | `in:inbox newer_than:2d`, up to 20 threads |
| Google Calendar | `list_events` | today's full day, user timezone |
| Monday.com | board item tools | open items assigned to user |

### Manual / pasted input

Accept any pasted content — Outlook emails, Obsidian notes, task lists, standup docs, Slack summaries, or plain text. Parse it directly.

- **Outlook**: Extract sender, subject, urgency signals (FWD:, RE:, URGENT, deadline)
- **Obsidian / markdown**: `- [ ]` → Todo, `- [x]` → Done, headings as context
- **Free text**: Extract any task-like or email-like items

If nothing is available and nothing is pasted:
> "Want to paste your emails or tasks? Copy from Outlook, Obsidian, or anywhere — I'll parse it."

---

## Step 2 — Classify items

### Column mapping

| Signal | Column |
|--------|--------|
| Requires reply, fix, or decision | **Todo** |
| Ongoing, pending approval, event to prepare for | **In Progress** |
| Confirmations, FYI, order receipts | **Done** (0.6 opacity) |
| Newsletters / promotions | One grouped card, or skip |

Don't create a card for every email — use judgment. Skip clearly non-actionable items.

### Priority badges

| Badge | When |
|-------|------|
| 🔴 Urgent | Deadline today, CI failure, escalation |
| 🟡 Medium | Action needed this week |
| 🔵 Opportunity | Freelance lead, interesting project |
| 🟢 Event | Calendar item, confirmed meetup |
| ⚪ General | Everything else |

---

## Step 3 — Build the HTML file

Single self-contained file, no external dependencies.

### Kanban layout

Three columns side by side (CSS grid):
- 📋 Todo / 🔄 In progress / ✅ Done
- Each column: header + count badge + card list + `+` button

### Card structure

```
┌────────────────────────────────────────┐
│ ⠿  [× on hover]                        │
│    Title (concise, max ~50 chars)      │
│    [Source badge] [Priority badge]     │
│    Link to original ↗ (if available)  │
└────────────────────────────────────────┘
```

### Add task form (per column)

`+` button → inline form:
- Text input: "Task title..."
- Tag selector: None / 🔴 Urgent / 🟡 Medium / 🔵 Project / 🟢 Event / ⚪ General
- Enter confirms, Escape cancels
- New card added to column, count updates

### Drag and drop — use mouse events (not HTML5 drag API)

```
mousedown → clone card as floating ghost (fixed pos), add .ghost to original
mousemove → move ghost with cursor, show blue 3px drop indicator between cards
mouseup   → insert original at indicator position, remove ghost, update counts
```

Done column: dropped cards set to `opacity: 0.6`.

### Design tokens

```css
body bg:      #f5f5f3
column bg:    #ebebea  border-radius: 12px
card:         #fff     border: 0.5px solid #e0e0dc  border-radius: 10px
font:         -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif

/* Badge colors */
.badge-red    { background: #FCEBEB; color: #a32d2d; }
.badge-amber  { background: #FAEEDA; color: #854f0b; }
.badge-blue   { background: #E6F1FB; color: #185fa5; }
.badge-green  { background: #EAF3DE; color: #3b6d11; }
.badge-gray   { background: #f1efe8; color: #666;    }

/* Source badge mapping */
Gmail / Outlook → blue   Monday → amber
Calendar        → green  GitHub → gray
Obsidian        → purple (#EEEDFE / #534AB7)
Manual          → gray
```

RTL support: `<html dir="rtl">` — works for Hebrew, consistent with mixed content.

---

## Step 4 — Save and present

1. Save as `morning_briefing_YYYY-MM-DD.html` in the outputs folder
2. Provide a `computer://` link
3. Add one line: "Drag cards between columns, add tasks with `+`, delete on hover with `✕`."

---

## Supported sources

| Source | Method |
|--------|--------|
| Gmail | Auto (MCP) |
| Google Calendar | Auto (MCP) |
| Monday.com | Auto (MCP) |
| Outlook | Paste in chat |
| Obsidian | Paste daily note |
| Notion / Linear / Jira / etc. | Paste exported content |
| Any text | Free-form paste |
| Manual | Via `+` button after file opens |

---

## Edge cases

- **Nothing available**: Ask user to paste or connect a source. Don't generate an empty board.
- **Only newsletters**: Group into one "Newsletters (skip)" card in Todo.
- **20+ items**: Show max ~5 per column. Group low-priority items.
- **Mixed Hebrew/English**: Cards stay in their original language. UI is bilingual-friendly.
- **Scheduling**: If user asks to run every morning, use the `schedule` skill.
