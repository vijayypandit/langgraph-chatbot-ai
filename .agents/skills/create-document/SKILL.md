---
name: create-document
description: Guidelines, formatting rules, and structural templates for creating and updating project documentation (like READMEs, guides, or instruction files).
---

# Documentation Creation Skill — Langgraph Chatbot 📝✨

## Purpose
- Define the standards, principles, and templates for creating or updating any project documentation (such as `README.md`, instructions files, developer guides, and onboarding checklists).
- Ensure all documents are clear, visually engaging, rich in explanation, and interactive with direct file links and professional diagrams.

---

## 📋 General Documentation Requirements

1. **Mandatory Project Code Scan**: You MUST scan and read all active codebase files BEFORE starting to create or update any README or documentation. This guarantees all documented functions, parameters, flows, and setups correspond exactly to the current code.
2. **Mandatory Emojis**: Always use expressive and relevant emojis at the start of headers, list items, and status indicators to keep the documents engaging and easy to read.
3. **Explicit Section Separators**: Use horizontal rule separators (`---`) between all major sections to organize content cleanly and professionally.
4. **Interactive File Links**: Always link to files using absolute file URI links (`file:///absolute/path/to/file`) instead of plain backticks or relative paths, so that they are directly clickable in the IDE.
5. **Mermaid Flowcharts**: Include clean Mermaid diagram flowcharts for any architectural description, sequence diagram, state machine, or process routing to keep descriptions visually clear and professional.
6. **No Placeholders**: Provide concrete examples, real configuration variables, and executable commands. Avoid boilerplate text like `insert_here` or `lorem ipsum`.
7. **Technical Precision**: Explicitly explain core system components, state designs, state reducers, edge transitions, checkpointers, and stream execution flows.

---

## 🎨 Design & Formatting Principles

- **Headers**: Maintain a clear vertical hierarchy with clean divider lines (`---`) between major sections.
- **Alert Boxes**: Use GitHub-style markdown alerts (e.g., `> [!NOTE]`, `> [!IMPORTANT]`, `> [!WARNING]`) to highlight important advice, caveats, or prerequisite instructions.
- **Code Blocks**: Always specify the code language (e.g., `python`, `bash`, `mermaid`) for syntax highlighting, and keep code segments complete and illustrative.
- **Tables & Lists**: Use structured tables when comparing options (e.g., streaming vs. blocking, checkpointer backends) and clean lists for chronological steps.

---

## 📁 Standard Documentation Templates

### 1️⃣ Project `README.md` Template
A standard project README must follow this logical order:
*   **Header**: Emoji-labeled main title, short sub-title, and summary of value.
*   **Key Features**: Bullet list describing the core functional pillars (e.g., streaming, state management).
*   **Architecture & Flow**: System interaction Mermaid diagram + backend graph flowchart.
*   **Backend Deep Dive**: Structural breakdown of states, nodes, edges, checkpointers, and code clips.
*   **Concept Deep Dives**: Detailed explanation of concepts (e.g., `thread_id` generation, state-switching, live generator streaming).
*   **Project Structure**: Directory layout listing key files as clickable links.
*   **Run Instructions**: Steps to install dependencies, set up environment files, and launch the application.
*   **Roadmap/Future Improvements**: Recommended persistent storage extensions or feature backlogs.

### 2️⃣ Developer Instructions & Guides Template
Any onboarding or environment setup instruction file must include:
*   **Prerequisites**: Software, API keys, and SDK version boundaries.
*   **Quick Start**: Clear terminal commands with absolute paths inside the workspace.
*   **Configuration Schema**: Complete lists of `.env` environment variables with default fallback options.
*   **Local Testing**: Commands to run unit tests, validation scripts, or linting checkouts.

---

## 🛠️ How to Apply This Skill
When tasked with writing or updating documentation:
1. View this skill file as a guide using `view_file` with `IsSkillFile=true`.
2. Analyze the target documentation request and identify the appropriate template to use.
3. Construct the markdown content matching the emojis, diagram, and link requirements outlined here.
4. Write or replace the file using the code edit tools.

---

## 📂 Files Created / Managed by This Skill
- `.agents/skills/create-document/SKILL.md` (this file)
- `README.md` — main repository entrypoint documentation
- `.instructions.md` — developer onboarding and project commands
- Any other helper `.md` documentation in the workspace
