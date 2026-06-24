---
name: frontend-design
description: Design principles and Streamlit UI starter template guidelines for creating polished visual interfaces in the chatbot app.
---

# Frontend Design Skill — Langgraph Chatbot

Purpose
- Capture frontend requirements and produce a modern Streamlit-based frontend design and starter implementation for the Langgraph Chatbot.
- Encourage premium UI aesthetics, polished layout structure, and a professional design system using modern typography and color combinations.

Captured requirements (from user)
- Primary goal: Chat application with conversational UI.
- Pages: Single-page chat experience.
- Theme: Light + Dark mode toggle.
- Branding: Modern, professional appearance; good use of spacing, sections, and visual hierarchy.
- Typography: Use Jakarta Sans / premium sans font family with smooth readability.
- Interactivity: Real-time or streamed responses, clear send flow, and helpful status indicators.
- Layout: Header, chat content area, input footer, optional footer note.
- Color: Professional palette with one accent color, subtle gradients, and good contrast.
- Framework: Streamlit.
- Deliverables: Skill file + frontend implementation guidance.

Deliverables produced by this skill
- A written skill specification summarizing the UI requirements and design principles.
- A structured component list and wireframe for the chat page.
- Streamlit frontend template components, CSS layout guidance, and design tokens.
- Recommended implementation path for modern UI, fonts, buttons, headers, and footers.

Design principles
- Use a modern, clean layout with clear spacing and soft rounded panels.
- Prefer light backgrounds with subtle depth and muted shadows in light mode; clean dark surfaces in dark mode.
- Use Jakarta Sans or a premium geometric sans-serif font for headings and body text.
- Apply a professional color combination: neutral base + calm accent + subtle shadows.
- Make buttons, cards, and form controls feel tactile with polished hover/focus states.
- Align header, chat bubble, input, and footer areas in a balanced vertical layout.
- Use consistent spacing, line heights, and rounded corners for all panels.

Component list / Wireframe
- Header: app title, subtitle, small logo/icon, theme toggle, top-level description.
- Info strip: model status, connection status, prompt hint or usage tip.
- Chat window: scrollable message feed, user bubble vs bot bubble, time stamps, typing indicator.
- Input footer: large text input, primary send button, optional action buttons (clear, attach, voice).
- Footer: minimal legal/brand note, support link, small footer help text.
- Background: glassmorphism-style hero background or soft gradient behind content.

UI system / style guide
- Typography
  - Primary font: `Jakarta Sans`, fallback to `Inter`, `system-ui`, `sans-serif`.
  - Headings: bold, modern, spaced.
  - Body text: comfortable size, good line-height, subtle text color.
- Spacing
  - Use a 4px baseline grid; generous padding around content.
  - Keep main container width between 1000px and 1200px for desktop.
- Buttons
  - Primary button: vivid accent, rounded pill shape, strong contrast.
  - Secondary button: ghost or low-key background with border.
  - Hover states: soft background lift or brightness increase.
- Cards and panels
  - Use smooth corner radius (16px) and subtle shadows.
  - Differentiate user and bot messages with tone and background.
- Header/Footer
  - Header: crisp title, compact controls, horizontal division from content.
  - Footer: discrete text, small links, subtle divider line.
- Color tokens
  - Background: `#F7F8FC` / `#111827`.
  - Surface: `#FFFFFF` / `#1F2937`.
  - Accent: `#4F46E5` or `#2563EB`.
  - Text: `#111827` / `#F9FAFB`.
  - Secondary: `#6B7280` / `#9CA3AF`.

UX Details
- Streaming responses: render partial bot text progressively inside the current bubble.
- Theme toggle: store selection in session state and apply CSS variables.
- Message history: preserve across user input, with clear and reset actions.
- Input experience: send on `Enter`, show disabled state while waiting.
- Feedback: show retry / error indicator if the backend fails to produce an answer.

Implementation plan
1. Create `assets/styles.css` with modern layout CSS, theme variables, and Jakarta Sans import.
2. Enhance `streamlit_frontend.py` to load the CSS, render the header, chat area, input footer, and optional footer.
3. Add `frontend_ui.py` or `ui.py` helper module exposing reusable render functions for header, chat bubbles, status strip, and input.
4. Use Streamlit columns/containers for structured layout: top banner, main chat card, sticky footer input.
5. Add a professional palette and clear contrast rules for light/dark modes.
6. Keep the UI code modular so future frontend improvements can swap out styles or layout easily.

Files to create / update
- `.agents/skills/frontend-design/SKILL.md` (this file)
- `frontend_ui.py` — reusable Streamlit UI helper functions
- `assets/styles.css` — modern design tokens, layout, header/footer styles, button styles
- `streamlit_frontend.py` — main entrypoint updated with the new UI structure and CSS

How to run / test (developer)
```powershell
cd E:\Projects\Project1Demo\Langgraph-ChatBot
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_frontend.py
```

Notes and assumptions
- The existing backend should provide a message send/receive interface; otherwise the frontend can start with a stub mode.
- This skill encourages a polished desktop-first experience but should remain adaptable for future responsive support.
- Having an `assets/styles.css` file allows the UI to feel more modern than default Streamlit styling.

Next steps I can take now
- Generate `frontend_ui.py` and `assets/styles.css` with modern layout, header/footer, button styles, and Jakarta Sans.
- Update `streamlit_frontend.py` to use these styles and render the chat UI with polished components.
- Optionally create a small `README.md` snippet describing the design system and frontend structure.

Please confirm which next step you want me to take.