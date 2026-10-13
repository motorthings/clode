# Safety: what a generated skill is allowed to do

Read this in Phase 5, alongside `environment.md`. That file answers whether a
skill *can* reach a tool. This answers what it may do once it can.

It applies to skills that touch connectors, files, or anything shared. A skill
that only transforms text the user pastes in is not a safety case. Say so rather
than padding the suite to look thorough.

---

## 1. Credentials never enter a skill

No token, key, password, connection string, or client secret in a SKILL.md or any
reference file. Not redacted, not as an example, not in a comment.

Never ask the user to paste a secret into the conversation to test a connector.

The skill says **where** the secret lives and stops: an environment variable, a
config path, a vault. If it needs auth, it names the variable the user set.

Absolute, and here is why. A skill whose job is reading a mailbox is exactly
where someone hardcodes an app password, and a skill file is a file that gets
copied, zipped, and shared.

---

## 2. Read and write are different asks

State which one the skill needs. Reading a calendar and booking a meeting are
different permissions with different consequences, and the description should say
which you are shipping.

**If the skill writes, it defaults to producing something the user sends.**
Draft the email, stage the change, prepare the pull request. The user performs
the irreversible step.

Where the skill genuinely must act, it says so plainly in the description, so
nobody installs it expecting a draft.

---

## 3. Irreversible actions get an explicit gate

Name the actions that cannot be taken back: sending, deleting, posting as the
user, merging, paying, deploying, revoking access.

Each gets a gate. Before acting, the skill states exactly what it is about to do
and to what, then waits.

This is a gate in the eval sense, which makes it the highest-value case in the
suite. Write one.

---

## 4. Shared surfaces are public

Posting to a channel, editing a shared document, commenting on someone's pull
request, adding a calendar event with attendees. These land where other people
see them, and they arrive as the user.

The skill says so, and confirms before the first write to a shared surface in any
run. Not once per build, once per run.

---

## 5. Other people's data

A mailbox, a document library, a shared drive holds other people's content.

The skill states what it reads. If it reads broadly and reports narrowly, say
that. Nothing leaves the tenant boundary unless the user asked for it: no pasting
internal content into an external service, no sending it to a model outside the
tenant.

---

## 6. Bounds

Anything that can iterate gets a cap and a dry run. Send at most N. Comment at
most N. If the list is longer than the cap, report what was dropped rather than
truncating silently.

A loop with a connector attached is how one bug becomes two hundred sent emails.

---

## Feeding the eval suite

Whichever rules apply become cases:

| Rule | What it produces |
|---|---|
| 1, credentials | **No case.** A review check: read the generated skill before shipping and confirm nothing resembling a secret is in it |
| 2, 3, 4 | A **fence** case each. Prompt the skill to act, assert it stops and confirms |
| 5, other people's data | An **output** case. Assert the skill names what it reads |
| 6, bounds | A boundary case. Give it more than the cap, assert it reports the drop |

If none apply, record that in the coverage table. An empty `fence` row is allowed
when the skill genuinely has no prohibitions, and honest is better than padded.
