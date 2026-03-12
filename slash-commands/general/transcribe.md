You are helping transcribe a video from a URL using MacWhisper's watched folder.

The user will provide a URL to a video (YouTube or other supported platforms).

Your task:
1. Get video metadata (title, duration, date) using yt-dlp
2. Download audio to MacWhisper's watched folder (MacWhisper will auto-transcribe)
3. Wait for MacWhisper to complete transcription (check for .txt file)
4. Read the transcript and create a markdown note with metadata
5. Clean up audio files after processing

Important details:
- **Download audio to MacWhisper watched folder**: `/Users/motorthings/Documents/Obsidian Vault/Transcriptions/watched_folder/`
- Use yt-dlp: `cd "/Users/motorthings/Documents/Obsidian Vault/Transcriptions/watched_folder" && yt-dlp -x --audio-format wav -o "%(title)s.%(ext)s" [URL]`
- MacWhisper will automatically detect and transcribe the file
- Wait for transcription: Look for matching .txt or .srt file in the watched folder
- After MacWhisper creates the transcript (usually takes 1-3 minutes for a 30min video):
  - Read the .txt file MacWhisper created
  - Create formatted markdown note with metadata
- **Save final transcript to**: `/Users/motorthings/Documents/Obsidian Vault/Transcriptions/`
- Filename format: `Transcript_[video_title]_[date].md`
- **Clean up**: Delete both the audio file (.wav) and MacWhisper's .txt file from watched_folder after processing

Workflow:
1. Get metadata with: `yt-dlp --print "%(title)s|||%(duration)s|||%(upload_date)s" [URL]`
2. Download to watched folder
3. Tell user "Audio downloaded to watched folder. Waiting for MacWhisper to transcribe..."
4. Poll for .txt file (check every 10 seconds, timeout after 10 minutes)
5. Once found, read transcript and create markdown note
6. Clean up watched folder

After transcription, show the user:
- The transcript file path (in Transcriptions folder)
- Video title and duration
- Transcript word count

Note: Make sure MacWhisper is running and has the watched folder configured to monitor `/Users/motorthings/Documents/Obsidian Vault/Transcriptions/watched_folder/`
