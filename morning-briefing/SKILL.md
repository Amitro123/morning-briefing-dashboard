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

## What this skill produces

A self-contained interactive HTML file saved to the outputs folder. It contains:
- A drag-and-drop kanban board (Todo / In Progress / Done)
- Cards auto-populated from the user's data sources
- Manual task addition via a + button in each column
- Delete-on-hover per card
- Direct links to source items (GitHub, Gmail threads, Monday tasks, etc.)
- Filename format: `morning_briefing_YYYY-MM-DD.html`

---

## Step 1 — Gather data

Pull from all available sources in parallel. More sources = better briefing.

### Connected MCP sources (use if tools are available)

| Source | Tool | Query |
|--------|------|-------|
| Gmail | `search_threads` | `in:inbox newer_than:2d` — up to 20 threads |
| Google Calendar | `list_events` | today's date range, user's timezone |
| Monday.com | `get_board_items_by_name` or similar | open items assigned to user |

Check which tools are actually available before trying — don't assume.

### Manual / pasted sources

If the user pastes content — Outlook emails, an Obsidian daily note, a task list, a standup doc, a Slack summary, anything — parse it directly. Treat any pasted text as a valid input. Accept mixed formats.

**Outlook emails**: Look for sender, subject, snippet. Infer urgency from subject line keywords (FWD:, RE:, URGENT, deadline, etc.)

**Obsidian / markdown notes**: Look for `- [ ]` checkboxes (→ Todo), `- [x]` (→ Done), headings as context.

**Free text / any format**: Extract any task-like or email-like items. Use context to infer priority.

If nothing is available and nothing is pasted, ask: "Want to paste your emails or tasks? You can copy from Outlook, Obsidian, or anywhere — I'll parse it."

---

## Step 2 — Classify items

Map every item to a kanban column and a priority level.

### Column logic

| Signal | Column |
|--------|--------|
| Requires a response, fix, or decision | **Todo** |
| Ongoing work, pending approval, event to prepare for | **In Progress** |
| Confirmations, order receipts, "FYI" items | **Done** (faded) |
| Newsletters, promotions, marketing | Group into one "skip" card in Todo or omit |

Don't create a card for every email. Use judgment — if something clearly requires no action, skip it or group it.

### Priority badges

| Badge | When to use |
|-------|------------|
| 🔴 Urgent | Deadline today, failure/error, escalation |
| 🟡 Medium | Action needed this week, pending reply |
| 🔵 Opportunity | Freelance lead, relevant event, interesting project |
| 🟢 Event | Calendar event, meetup, approved registration |
| ⚪ General | Everything else |

---

## Step 3 — Build the HTML file

Generate a single self-contained HTML file with no external dependencies.

### Kanban structure

Three columns side by side (CSS grid):
- 📋 **Todo** — items needing action
- 🔄 **In Progress** — ongoing or being watched
- ✅ **Done** — completed or FYI

Each column has:
- Header with title + live count badge
- Scrollable card list
- `+` Add task button at the bottom

### Card anatomy

```
┌─────────────────────────────────────────┐
│  [× delete on hover]                    │
│  Title of the item (concise, actional)  │
│  [Source badge] [Priority badge]        │
│  Link to original ↗ (if available)     │
└─────────────────────────────────────────┘
```

### Add task form (per column)

Clicking `+` opens an inline form:
- Text input: "כותרת המשימה..." / "Task title..."
- Tag selector: ללא תגית / 🔴 דחוף / 🟡 בינוני / 🔵 פרויקט / 🟢 אירוע / ⚪ כללי
- Confirm (Enter or button) / Cancel (Escape)
- On confirm: add card to column, update count, reset form

### Drag and drop

**Use mouse events, not HTML5 drag API** — more reliable across local file opens and different environments.

Implementation pattern:
1. `mousedown` on card → store offset, clone card as floating ghost (fixed position), add `.ghost` class to original
2. `mousemove` → move ghost with cursor, detect target column/position, show blue drop indicator line
3. `mouseup` → insert original card at indicator position, remove ghost, update counts

Key details:
- Ghost follows cursor precisely (offset from where the user clicked)
- Blue 3px indicator line shows drop position between cards
- Column highlights subtly when a card hovers over it
- Done column: dropped cards get 0.6 opacity

### Design guidelines

- Background: `#f5f5f3` (warm off-white)
- Columns: `#ebebea` with `border-radius: 12px`
- Cards: white `#fff`, `border: 0.5px solid #e0e0dc`, `border-radius: 10px`
- Font: system-sans (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`)
- RTL support: `dir="rtl"` on `<html>` — works for Hebrew content, visually consistent for mixed Hebrew/English
- No external CSS or JS libraries — fully self-contained

### Badge color reference

```css
.badge-red    { background: #FCEBEB; color: #a32d2d; }
.badge-amber  { background: #FAEEDA; color: #854f0b; }
.badge-blue   { background: #E6F1FB; color: #185fa5; }
.badge-green  { background: #EAF3DE; color: #3b6d11; }
.badge-gray   { background: #f1efe8; color: #666;    }
```

Source badges (smaller, use same color system):
- Gmail → blue
- Calendar → green
- Monday → amber
- GitHub → gray
- Manual → gray
- Outlook → blue
- Obsidian → purple (`background: #EEEDFE; color: #534AB7`)

---

## Step 4 — Save and present

1. Save the file as `morning_briefing_YYYY-MM-DD.html` in the outputs folder
2. Provide a `computer://` link so the user can open it directly
3. One-line note: "גרור כרטיסים בין עמודות, הוסף משימות עם + ומחק עם ✕ בזמן hover."

---

## Supported sources — quick reference

| Source | How | Notes |
|--------|-----|-------|
| Gmail | MCP connector (auto) | Searches inbox, last 2 days |
| Google Calendar | MCP connector (auto) | Today's events |
| Monday.com | MCP connector (auto) | Open items assigned to user |
| Outlook | Paste email list or body | Copy from Outlook → paste in chat |
| Obsidian | Paste daily note | Parses `- [ ]` tasks and headings |
| Any text | Paste anything | Free-form parsing |
| Manual | Type in the board | Via + button after file is open |

---

## Edge cases

- **No sources, nothing pasted**: Ask the user to connect a source or paste content. Don't generate an empty board.
- **Only newsletters**: Still generate the board, but group them all into one "Newsletters (skip)" card in Todo.
- **Mixed Hebrew/English**: Handle naturally — titles stay in their original language, UI can be bilingual.
- **Many items (20+)**: Prioritize ruthlessly. Show max ~5 items per column. Group low-priority items.
- **Scheduling / automation**: If the user asks to run this every morning, help them set up a scheduled task using the schedule skill.
