You are selecting and summarizing the most relevant article from the user's reading list based on recent work context.

**Your task:**

## Step 1: Initialize Article Index

- Check if `/Users/motorthings/Documents/Obsidian Vault/articles/.article-index.md` exists
- If not, create it with header:
  ```markdown
  # Article Index

  Auto-generated index of saved articles. Updated by /read-now command.

  ---
  ```

## Step 2: Scan for New Articles

- Use Glob to find all files in `/Users/motorthings/Documents/Obsidian Vault/articles/`
- Look for: `*.md` and `*.pdf` files
- Read the article index to see which articles are already indexed
- Identify any new articles not in the index

## Step 3: Index New Articles

For each new article found:
- Read the content (first 500-1000 characters if long)
- Extract or infer: title, main topic
- Generate 1-sentence description of what the article is about
- Add entry to index:
  ```markdown
  ### [Title]
  - **Path:** [relative path from vault root]
  - **Summary:** [Will be added after selection]
  - **Added:** [today's date]
  - **Topic:** [1-sentence description]

  ---
  ```

Note: The summary link will be added in Step 7 when an article is selected and summarized.

## Step 4: Understand Recent Work Context

- Read `/Users/motorthings/Documents/Obsidian Vault/recent-activity.md`
- Extract key themes from last 2-3 days:
  - What topics are we working on?
  - What problems are we solving?
  - What areas of focus?

## Step 5: Match Article to Context

- Review all indexed articles
- Compare article topics to recent work themes
- Consider:
  - Relevance to current projects
  - Timeliness (newer articles slightly preferred)
  - Complementary knowledge (fills gaps in recent work)
- Select the MOST relevant article

## Step 6: Read and Summarize Selected Article

- Read the full article content (PDF or markdown)
- Generate exactly 2 paragraphs:
  - **Paragraph 1:** Core thesis and main points (3-4 sentences)
  - **Paragraph 2:** Key takeaways and how it relates to our recent work (2-3 sentences)
- Keep total summary under 150 words

## Step 7: Save Summary and Update Daily Note

**Create dedicated summary file:**
- Summary location: `/Users/motorthings/Documents/Obsidian Vault/Articles/Summaries/[Article Title].md`
- Create folder if it doesn't exist: `Articles/Summaries/`
- Format:
  ```markdown
  # [Article Title]

  **Author:** [If known]
  **Source:** [Link to original PDF/file]
  **Read:** [YYYY-MM-DD]
  **Relevance:** [How it relates to recent work]

  ---

  ## Summary

  [2-paragraph summary from Step 6]

  ---

  ## Key Takeaways

  [3-5 bullet points of main insights]

  ---

  ## Application to Current Work

  [How this applies to recent activity/projects]
  ```

**Update daily note:**
- Daily note location: `/Users/motorthings/Documents/Obsidian Vault/YYYY-MM-DD.md`
- If daily note doesn't exist, create it with header `# [Day of week], [Month] [Day], [Year]`
- Append link under section `## 📚 Article Read`
- Format:
  ```markdown
  ## 📚 Article Read

  **[Article Title](Articles/Summaries/[Article Title].md)** | [Time] | [Original file link]

  [1-sentence description]

  ---
  ```

**Update article index:**
- Add summary link to the article's entry in `.article-index.md`
- Add line: `- **Summary:** [Article Title](Summaries/[Article Title].md)`

## Step 8: Report Completion

Tell the user:
- Which article was selected and why (how it relates to recent work)
- Where the summary was saved (Articles/Summaries/[Article Title].md)
- That a link was added to today's daily note
- How many new articles were added to the index (if any)

**Important Notes:**
- If no `recent-activity.md` exists, select based on recency and general interest
- If `/articles` folder is empty, tell user to add articles first
- Always include clickable file link to original article
- Keep summaries concise and actionable
- Focus on relevance to user's current work context
