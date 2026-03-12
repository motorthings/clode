Help me understand and use the Obsidian MCP server capabilities.

Display a comprehensive guide showing:

## 🔌 Obsidian MCP Server Status

Check the connection status of the obsidian-mcp server and confirm it's working properly.

## 🛠️ Available Capabilities

### 1. Vault Access & File Management
- Read and reference notes from the vault
- Create new notes with proper frontmatter and formatting
- Update existing notes
- Search files by name, path, or content
- Access note metadata (frontmatter, tags, etc.)

**Example Tasks:**
- "Read the note about [topic]"
- "Create a new meeting note for today"
- "Update my daily note with a summary of what I worked on"
- "Show me all notes tagged with #project"

### 2. Semantic Search
- Search based on meaning and context, not just keywords
- Find related notes by conceptual similarity
- Discover connections between ideas across the vault
- Requires Smart Connections plugin (if installed)

**Example Tasks:**
- "Find all notes related to AI workflows, even if they don't mention 'AI' explicitly"
- "What notes discuss similar concepts to [note name]?"
- "Search for notes about productivity systems"
- "Find related content about [topic]"

### 3. Template Integration
- Execute Obsidian templates with dynamic parameters
- Generate structured notes using templates
- Create content with AI-provided context
- Requires Templater plugin (if installed)

**Example Tasks:**
- "Create a new project note using the project template"
- "Generate a meeting summary using the meeting template"
- "Use the daily note template to create today's note"

## 🎯 Common Use Cases

### Content Organization
- Find and organize related notes
- Identify gaps in documentation
- Create index pages linking related content
- Tag and categorize notes systematically

### Research & Analysis
- Synthesize information across multiple notes
- Find connections between different topics
- Generate summaries of note collections
- Answer questions using vault knowledge

### Note Creation & Updates
- Create structured notes with templates
- Add consistent frontmatter to notes
- Update meeting notes with action items
- Generate summaries and add to daily notes

### Knowledge Discovery
- Explore what you've written about a topic
- Find forgotten or overlooked notes
- Discover unexpected connections
- Map out knowledge domains

## 📋 Current Configuration

- **Server:** obsidian-mcp
- **Location:** `.obsidian/plugins/mcp-tools/bin/mcp-server`
- **API:** Local REST API (port 27124)
- **Config:** `.mcp.json` (project-level)

## 💡 How to Get Started

1. **Ask about your notes:** "What have I written about [topic]?"
2. **Search semantically:** "Find notes related to [concept]"
3. **Create content:** "Create a new note about [topic] with proper frontmatter"
4. **Analyze connections:** "How are my notes about [topic A] and [topic B] related?"
5. **Organize:** "Help me organize my notes about [topic]"

## 🔒 Security Note

The MCP server accesses your vault through the Local REST API plugin. All access is:
- Authenticated with your API key
- Routed through Obsidian's official plugin API
- Never gives direct file system access
- Respects Obsidian's permission model

---

After displaying this guide, ask me: **"What would you like to do with your Obsidian vault?"**
