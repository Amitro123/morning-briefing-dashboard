---
name: morning-briefing
description: >
  Generates a daily morning briefing as an interactive HTML kanban board (Todo / In Progress / Done).
  Auto-pulls from connected sources — Gmail, Google Calendar, Monday.com — and also accepts pasted
  content from any source: Outlook emails, Obsidian notes, a task list, anything. Use this skill
  whenever the user asks for a morning briefing, daily dashboard, "what's on my plate today",
  standup prep, daily task overview, or wants to organize their emails and tasks into a visual board.
  Even if the user just says "start my day", "תתחיל את היום שלי", or pastes a block of tasks/emails,
  use this skill. Trigger also for "kanban from my emails", "organize my tasks", "what should I focus on today".
---

# Morning Briefing — Daily Kanban Dashboard

Produces a self-contained HTML file: `morning_briefing_YYYY-MM-DD.html`

Features: drag-and-drop kanban (Todo / In Progress / Done), cards from live sources or pasted text,
`+` button per column for manual tasks, `✕` delete on hover, deep links to source items.

---

## Step 1 — Gather data

Pull from all available sources in parallel.

### MCP connectors (use if tools are available)

| Source | Tool | Query |
|--------|------|-------|
| Gmail | `search_threads` | `in:inbox newer_than:2d`, up to 20 threads |
| Google Calendar | `list_events` | today full day, user timezone |
| Monday.com | board item tools | open items assigned to user |

### Pasted input (no connector needed)

Accept any pasted content and parse it directly:

| Format | Signals to extract |
|--------|-------------------|
| Outlook emails | Sender, subject, urgency keywords (FWD:, RE:, URGENT, deadline) |
| Obsidian / markdown | `- [ ]` → Todo, `- [x]` → Done, headings as context |
| Any free text | Extract task-like or email-like items |

If nothing is available and nothing is pasted, ask:
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

Don't create a card for every email — use judgment. Max ~5 cards per column; group low-priority items.

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

### Layout

Three columns (CSS grid): 📋 Todo / 🔄 In progress / ✅ Done
Each column: header + live count badge + card list + `+` add button

### Card structure

```
┌────────────────────────────────────────┐
│ ⠿  [× on hover]                        │
│    Title (concise, ~50 chars max)      │
│    [Source badge] [Priority badge]     │
│    Link to original ↗ (if available)  │
└────────────────────────────────────────┘
```

### Add task form

`+` → inline form per column:
- Text input + tag selector (None / 🔴 Urgent / 🟡 Medium / 🔵 Project / 🟢 Event / ⚪ General)
- Enter confirms, Escape cancels, count updates on add

### Drag and drop — mouse events only (not HTML5 drag API)

```
mousedown → clone card as floating ghost (fixed pos), add .ghost to original
mousemove → move ghost with cursor, show 3px blue drop indicator between cards
mouseup   → insert original at indicator, remove ghost, update counts
```

Done-column drops: set card `opacity: 0.6`.

### Design tokens

```css
body:        background #f5f5f3
column:      background #ebebea, border-radius 12px
card:        background #fff, border 0.5px solid #e0e0dc, border-radius 10px
font:        -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif

/* Priority badges */
.badge-red    { background: #FCEBEB; color: #a32d2d; }
.badge-amber  { background: #FAEEDA; color: #854f0b; }
.badge-blue   { background: #E6F1FB; color: #185fa5; }
.badge-green  { background: #EAF3DE; color: #3b6d11; }
.badge-gray   { background: #f1efe8; color: #666;    }

/* Source badges */
Gmail / Outlook → blue    Monday  → amber
Calendar        → green   GitHub  → gray
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

## Edge cases

| Situation | Handling |
|-----------|---------|
| Nothing available | Ask user to paste or connect. Don't generate empty board. |
| Only newsletters | Group into one "Newsletters (skip)" card in Todo |
| 20+ items | Max ~5 per column, group low-priority |
| Mixed Hebrew/English | Cards stay in original language; UI is bilingual-friendly |
| User wants automation | Suggest `schedule` skill for daily runs |
