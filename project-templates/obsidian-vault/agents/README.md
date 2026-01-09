# Custom Claude Code Agents for Obsidian

This folder contains specialized sub-agents that help you work with your Obsidian vault in different modes.

## Available Agents

### 1. **thinking-partner**
For exploring ideas without generating content.

**Use when:**
- Starting a new project and need to think it through
- Brainstorming and making connections
- Working through complex problems
- You want questions, NOT answers

**How to invoke:**
```
Use the thinking-partner agent to help me explore [topic]
```

**What it does:**
- Asks probing questions
- Helps you think, doesn't write for you
- Identifies patterns in your existing notes
- Keeps running log of insights

---

### 2. **daily-summarizer**
For synthesizing your day's work into a progress note.

**Use when:**
- Ending a work session
- Want to capture what you learned
- Need to maintain continuity across sessions

**How to invoke:**
```
Use the daily-summarizer agent to summarize today's progress on [project]
```

**What it does:**
- Reviews notes created/modified today
- Extracts key insights and connections
- Creates dated progress note
- Suggests next steps

---

### 3. **research-assistant**
For finding and organizing materials from your vault.

**Use when:**
- Starting a new project
- Need to find all notes on a topic
- Want to see connections across your vault
- Setting up project research folders

**How to invoke:**
```
Use the research-assistant agent to find everything about [topic]
```

**What it does:**
- Searches across your entire vault
- Finds related materials you might have forgotten
- Organizes findings by relevance
- Sets up project folder structures

---

### 4. **interviewer**
For extracting and developing your ideas through conversation.

**Use when:**
- Have a fuzzy idea that needs clarification
- Want to stress-test your thinking
- Need to articulate something important
- Preparing for a talk or article

**How to invoke:**
```
Use the interviewer agent to interview me about [topic]
```

**What it does:**
- Asks structured questions to extract your thinking
- Challenges assumptions gently
- Documents insights as they emerge
- Helps you discover what you actually think

---

## Tips for Using Agents

1. **Be explicit about mode** - Tell the agent if you're in "thinking mode" vs "writing mode"

2. **Use front matter** - Add instructions to your notes:
   ```yaml
   ---
   mode: thinking
   agent-instruction: Do not create drafts, only ask questions
   ---
   ```

3. **Combine agents** - Start with interviewer, move to thinking-partner, end with daily-summarizer

4. **Create project structures** - Let research-assistant set up your folders first

5. **Review daily** - Use daily-summarizer regularly to maintain momentum

## Example Workflows

### Starting a New Project
1. Use **research-assistant** to find existing relevant materials
2. Use **thinking-partner** to explore the core idea
3. Use **interviewer** to clarify fuzzy aspects
4. Use **daily-summarizer** to capture the session

### Developing an Idea
1. Use **thinking-partner** to brainstorm
2. Use **interviewer** to stress-test the idea
3. Use **research-assistant** to find supporting materials
4. Use **daily-summarizer** to track progress

### Voice Chat Integration
1. Have voice conversation (ChatGPT, Grok, etc.)
2. Save transcript to project's `/chats` folder
3. Use **daily-summarizer** to synthesize the conversation
4. Use **thinking-partner** to explore threads that emerged

---

## Customization

You can edit any agent file to customize behavior for your needs. Each agent is just a markdown file with instructions.

**To create your own agent:**
1. Create a new .md file in this folder
2. Write clear instructions for what the agent should do
3. Invoke it in Claude Code using the filename (without .md)

---

Created based on Noah Brier's Obsidian + Claude Code workflow
Inspired by: https://every.to (Second Brain podcast episode)
