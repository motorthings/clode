# Environment: what the skills you build may assume

**Edit this file freely.** It describes the tools available *where the skill will
run*, which is not necessarily the machine you are building on. Replace the
default list with your stack, or add to it. The builder reads this before
designing a solution around any connector.

---

## The rule

**A skill may only assume tools that appear in this file.**

A skill built against a connector nobody has is worthless, and it fails quietly:
the skill reads correctly, the user installs it, and it has nothing to call. So
when a solution leans on a tool, check it against this list first. If it is here,
build against it. If it is not, you have two honest options:

- **Name it as a prerequisite.** Write the skill so its first step confirms the
  tool is connected and stops with a clear message if it is not. That is a gate,
  and gates are the highest-value cases in the eval suite.
- **Find an approach that needs nothing.** Often the real answer: a process that
  depends on a connector may have a version that works from pasted text.

What you must not do is design around a tool you have not confirmed exists.

---

## Default surface: Microsoft 365

This is the starting list. It assumes a standard work tenant.

| Surface | What a skill can do with it |
|---|---|
| **Outlook** | Read and draft mail, search a mailbox, read and create calendar events, check availability |
| **Teams** | Read and post in channels and chats, pull meeting transcripts and recordings, find people |
| **SharePoint** | Read and write documents in site libraries, list sites, follow document links |
| **OneDrive** | Read and write personal files, share links |
| **Excel** | Read and write workbooks, work with named tables, append rows |
| **Word / PowerPoint** | Read and generate documents and decks |
| **Planner / To Do** | Read and create tasks, assign, check status |
| **Power Automate** | Trigger an existing flow, read flow run history |

Two cautions about this list:

- **Read versus write.** Many tenants grant read broadly and write narrowly. A
  skill that drafts into your own drafts folder is a different ask than one that
  sends mail as you. When a solution needs write access, say so, and make the
  skill confirm before acting.
- **Not every tenant grants every surface.** The list says what *can* be
  available. The generated skill's gate should confirm what actually is.

---

## Adding your own

Copy the table shape and add a section. Anything a skill could call belongs here:
other connectors, local CLIs, internal APIs, a database, a shared drive.

```markdown
## Our stack

| Tool | What a skill can do with it |
|---|---|
| **ClickUp** | Read and create tasks in a list, update status |
| **GitHub** | Read and open PRs, list review requests, read CI status |
| **Linear** | Read issues, update state |
```

Keep the entries at the level of *what a skill could do*, not how. The how
belongs in the generated skill.

---

## When someone names a tool that isn't here

Ask whether they have it. If they do, this file is out of date and editing it is
the fix. If they do not, the solution has to change, and that is worth saying out
loud rather than designing around a gap.

The question that settles it: **where will this skill run?** Not where you are
building it. A skill written on a laptop with no corporate mailbox is headed
somewhere that has one, and the environment that matters is the destination.
