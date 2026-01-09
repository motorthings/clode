Transcribe an audio file and create a properly formatted Obsidian note.

Workflow:
1. Ask for the audio file path (or use the most recent file in Audio/)
2. Use ElevenLabs MCP to transcribe: `mcp__elevenlabs__speech_to_text`
3. Ask user for:
   - Note title
   - Source/context (meeting, podcast, video, voice memo)
   - Project to associate with (optional)
   - Tags to add
4. Create note with proper frontmatter:
   ```yaml
   ---
   created: [timestamp]
   source: [source type]
   audio_file: [path]
   tags: [tags]
   ---
   ```
5. Save to appropriate folder (Transcriptions/ or project folder)
6. Offer to create summary or extract key points

Use voice-to-notes.js script as fallback if MCP fails.
