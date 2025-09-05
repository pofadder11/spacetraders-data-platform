Session memory scaffold for Codex CLI

This directory provides simple, file-based memory so your CLI sessions can persist context across runs.

Layout:
- history/: JSONL transcripts per session ID (ignored by git)
- session/summary.md: working memory of key context/decisions/TODOs
- plan.json: optional lightweight plan snapshot

Typical usage (Python):
- Use services.memory.append_history(session_id, role, content[, meta]) to append chat/tool events
- Use services.memory.load_summary()/save_summary() to manage the working summary
- Use services.memory.load_plan()/save_plan() to persist a plan snapshot

MCP note:
If your client uses MCP, you can point a filesystem MCP server at this folder to expose these resources to the assistant.

