---
title: Legally AI - Contract Analysis
emoji: 📜
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# Legally AI - Contract Analysis Prototype

AI-powered contract analysis in **Russian, Serbian, French, and English**.

## What it does

Upload your contract (PDF or DOCX) and get:
- ✅ Clear summary of what you're agreeing to
- ✅ List of your obligations and rights
- ✅ Risk flags and recommendations
- ✅ Confidence assessment

## How to use

1. Upload your contract (PDF or DOCX)
2. Select the output language
3. Click "Analyze Contract"
4. Review the analysis

## Important Disclaimer

⚠️ **This is a prototype for testing purposes only.**

This is an AI-powered informational screening — **not legal advice**, not a law-firm review, and it does not create an attorney–client relationship. We looked only at the text you provided and did not verify facts, identities, authority to sign, ownership, required formalities, or compliance with local law.

For important contracts, always consult a qualified lawyer.

## Languages Supported

- 🇷🇺 Russian (Русский)
- 🇷🇸 Serbian (Српски)
- 🇫🇷 French (Français)
- 🇬🇧 English

## Technology

- **LLM**: Groq (llama-3.3-70b-versatile)
- **Parsers**: pdfplumber, python-docx
- **Language Detection**: langdetect
- **UI**: Gradio

## Feedback

This is a prototype being tested with legal professionals. If you find issues:
- Accuracy problems
- Missing information
- Confusing output
- Language/translation issues

Please provide feedback to help us improve!

---

**Developed with ❤️ for making contracts understandable**
