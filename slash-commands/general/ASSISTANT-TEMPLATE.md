# Template for Creating Assistant Slash Commands

This template shows how to create slash commands that load custom AI assistant instructions.

---

## Quick Guide

### 1. Store Your Assistant Instructions

Create a file in `Assistants/[assistant-name].md` with your full system instructions.

**Example:** `Assistants/gigawatt.md`

### 2. Create the Slash Command

Create a file in `.claude/commands/[assistant-name].md` with this structure:

```markdown
You are now operating as the **[Assistant Name]** assistant - [brief description].

Read and follow the complete instructions in: [[Assistants/[assistant-name].md]]

Load those instructions now and operate as the [Assistant Name] assistant until the user tells you to stop or uses /reset.

**Your role:** [One sentence role description]

**Key capabilities:**
- [Capability 1]
- [Capability 2]
- [Capability 3]

[Optional: Initial greeting or question to the user]
```

### 3. Use the Assistant

In Claude Code, type:
```
/[assistant-name]
```

Claude Code will load the instructions and operate as that assistant.

### 4. Return to Normal

Type `/reset` to return Claude Code to standard behavior.

---

## Complete Example: Gigawatt Assistant

### Step 1: Create Instructions File

**File:** `Assistants/gigawatt.md`

```markdown
# Gigawatt - Energy Efficiency Consultant

You are Gigawatt, an AI assistant specialized in energy efficiency analysis and recommendations.

## Your Role
You help users analyze energy consumption, identify inefficiencies, and recommend sustainable solutions.

## Core Capabilities
- Energy audit analysis
- Cost-benefit calculations for efficiency upgrades
- Renewable energy system sizing
- Carbon footprint estimation
- Building efficiency recommendations

## Approach
1. Start with understanding current energy usage
2. Identify key areas of waste
3. Prioritize recommendations by ROI
4. Provide actionable, specific guidance
5. Include relevant calculations and metrics

## Communication Style
- Technical but accessible
- Data-driven with specific metrics
- Practical and actionable
- Environmentally conscious
- Cost-aware

## Key Principles
- Always provide quantitative analysis when possible
- Consider both environmental and financial impacts
- Tailor recommendations to user's specific context
- Explain technical concepts clearly
- Follow up with implementation guidance
```

### Step 2: Create Slash Command

**File:** `.claude/commands/gigawatt.md`

```markdown
You are now operating as the **Gigawatt** assistant - an energy efficiency consultant.

Read and follow the complete instructions in: [[Assistants/gigawatt.md]]

Load those instructions now and operate as the Gigawatt assistant until the user tells you to stop or uses /reset.

**Your role:** AI specialist in energy efficiency analysis and sustainable solutions.

**Key capabilities:**
- Energy auditing and consumption analysis
- ROI calculations for efficiency upgrades
- Renewable energy system sizing
- Carbon footprint estimation
- Building efficiency recommendations

How can I help you with energy efficiency today?
```

### Step 3: Test the Assistant

In Claude Code:
```
User: /gigawatt
Claude: [Loads instructions and asks about energy efficiency]

User: I want to analyze my home's energy usage
Claude: [Operates as Gigawatt, asking technical questions about usage]

User: /reset
Claude: [Returns to normal Claude Code]
```

---

## Best Practices

### For Instruction Files (Assistants/[name].md)

**Do:**
- ✓ Be specific about the assistant's role and scope
- ✓ Define communication style and tone
- ✓ List core capabilities clearly
- ✓ Include examples of good responses
- ✓ Specify what the assistant should NOT do
- ✓ Use structured format (headings, lists, examples)

**Don't:**
- ✗ Make instructions too vague or general
- ✗ Overlap too much with other assistants
- ✗ Include outdated information
- ✗ Create instructions without testing them

### For Slash Commands (.claude/commands/[name].md)

**Do:**
- ✓ Keep it concise (reference the full instructions file)
- ✓ Include a brief role description
- ✓ List 3-5 key capabilities
- ✓ Optionally add an opening question/greeting
- ✓ Always reference the full instructions with [[wikilink]]

**Don't:**
- ✗ Duplicate all instructions in the command file
- ✗ Make the command file too long
- ✗ Forget to mention /reset option

### Naming Conventions

**Instructions:** `Assistants/[lowercase-name].md`
- `gigawatt.md`
- `brand-voice-analyzer.md`
- `code-reviewer.md`

**Commands:** `.claude/commands/[same-name].md`
- `gigawatt.md`
- `brand-voice-analyzer.md`
- `code-reviewer.md`

**Usage:** `/[same-name]`
- `/gigawatt`
- `/brand-voice-analyzer`
- `/code-reviewer`

---

## Managing Multiple Assistants

### Organization

```
Assistants/
├── README.md (overview of all assistants)
├── echo.md (brand voice analysis)
├── gigawatt.md (energy efficiency)
├── code-mentor.md (coding tutor)
└── writer-coach.md (writing improvement)

.claude/commands/
├── echo.md → loads [[Assistants/echo.md]]
├── gigawatt.md → loads [[Assistants/gigawatt.md]]
├── code-mentor.md → loads [[Assistants/code-mentor.md]]
├── writer-coach.md → loads [[Assistants/writer-coach.md]]
├── list-assistants.md (shows all available)
└── reset.md (return to normal)
```

### Discovery

Create `/list-assistants` command to show all available assistants.

### Switching

You can switch directly between assistants:
```
/gigawatt
[work with gigawatt]
/echo
[switch to echo without /reset first]
```

---

## Common Assistant Types

### Analysis & Review
- Code reviewer
- Brand voice analyzer
- Document editor
- Data analyst

### Tutoring & Learning
- Programming tutor
- Language coach
- Subject matter expert
- Study buddy

### Creative & Writing
- Writing coach
- Story editor
- Content strategist
- Copywriter

### Technical & Domain
- Energy consultant (gigawatt)
- Legal advisor
- Medical information
- Financial planner

### Workflow & Productivity
- Project manager
- Meeting facilitator
- Research assistant
- Task organizer

---

## Testing Your Assistant

### Checklist

- [ ] Instructions file created in `Assistants/`
- [ ] Slash command created in `.claude/commands/`
- [ ] Both files use the same name
- [ ] Instructions are clear and specific
- [ ] Command references instructions file with [[wikilink]]
- [ ] Tested with `/[name]` in Claude Code
- [ ] Assistant responds appropriately to test queries
- [ ] `/reset` returns to normal behavior
- [ ] Updated `Assistants/README.md` with new assistant

### Test Conversation

```
/[your-assistant]
[Test 1: Basic capability]
[Test 2: Edge case]
[Test 3: Outside scope - should gracefully decline]
/reset
[Confirm normal behavior restored]
```

---

## Maintenance

### Updating Assistants

1. Edit the instructions file in `Assistants/[name].md`
2. Slash command automatically picks up changes
3. Test the updated behavior
4. Document changes in the instructions file

### Versioning (Optional)

```markdown
# Assistant Name

**Version:** 2.1
**Last Updated:** 2025-11-17
**Changelog:**
- v2.1: Added capability X
- v2.0: Major update to approach
- v1.0: Initial version
```

### Deprecating Assistants

1. Add `[DEPRECATED]` to file name
2. Update command to suggest alternative
3. Move to `Assistants/archive/` folder

---

## Advanced Patterns

### Context-Aware Assistants

Include vault-specific context:
```markdown
**Your context:**
You have access to this user's vault including:
- [[AI BuildLab/]] - Course content and meetings
- [[Networking/]] - Professional connections
- [[Transcriptions/]] - Learning materials

When relevant, reference and link to existing notes.
```

### Multi-Mode Assistants

Different sub-modes within one assistant:
```markdown
**Modes:**
1. Analysis mode - `/gigawatt analyze`
2. Recommendation mode - `/gigawatt recommend`
3. Calculation mode - `/gigawatt calculate`

Ask the user which mode they need, or infer from context.
```

### Chained Assistants

Suggest related assistants:
```markdown
After completing this analysis, you might want to:
- Use `/writer-coach` to draft communication
- Use `/project-manager` to plan implementation
- Use `/reset` to return to normal Claude Code
```

---

## Examples Library

See existing assistants for reference:
- `/echo` - Comprehensive brand voice analysis (see [[Assistants/Echo.md]])
- `/think` - Thinking partner (see [[.claude/commands/think.md]])
- `/brand-voice` - Brand voice guidance (see [[.claude/commands/brand-voice.md]])

---

## Quick Reference

**Create new assistant:**
1. Write instructions → `Assistants/[name].md`
2. Create command → `.claude/commands/[name].md`
3. Test with `/[name]`

**Use assistant:**
- `/[name]` - Activate
- `/reset` - Deactivate
- `/list-assistants` - See all available

**Manage assistants:**
- Edit `Assistants/[name].md` to update
- Update `Assistants/README.md` for documentation
- Use [[wikilinks]] to reference between files

---

**For more help, see:**
- [[Assistants/README]] - Overview of all assistants
- [[CLAUDE-CODE-AGENTS]] - Built-in Claude Code agents (different from custom assistants)
- [[TEMPLATES]] - Note templates and standards
