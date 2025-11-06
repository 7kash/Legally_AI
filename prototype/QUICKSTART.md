# Legally AI Prototype - Quick Start Guide

## Setup (Local Development)

### 1. Install Dependencies

```bash
cd prototype
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy `.env.example` to `.env` and add your Groq API key:

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

Your `.env` should look like:
```
GROQ_API_KEY=gsk_your_api_key_here
DEFAULT_MODEL=llama-3.3-70b-versatile
SUPPORTED_LANGUAGES=russian,serbian,french,english
```

### 3. Run the App

```bash
python app.py
```

The app will launch at http://localhost:7860

## Deploy to Hugging Face Spaces

### 1. Create a New Space

1. Go to https://huggingface.co/new-space
2. Name: `Legally_AI` (or your choice)
3. SDK: Gradio
4. Hardware: CPU Basic (free)
5. Click "Create Space"

### 2. Add Your API Key as a Secret

1. In your Space settings, go to "Repository secrets"
2. Add a new secret:
   - Name: `GROQ_API_KEY`
   - Value: `gsk_your_api_key_here`
3. Save

### 3. Upload Files

Upload all files from the `prototype/` directory:

```
prototype/
├── app.py                  # Main application
├── requirements.txt        # Dependencies
├── README.md              # Space description
└── src/
    ├── __init__.py
    ├── constants.py
    ├── parsers.py
    ├── language.py
    ├── quality.py
    ├── llm_router.py
    ├── step1_preparation.py
    ├── step2_analysis.py
    ├── formatter.py
    └── prompts/
        ├── preparation_en.txt
        └── analysis_en.txt
```

### 4. Wait for Build

HF Spaces will automatically:
- Install dependencies from `requirements.txt`
- Load your API key from secrets
- Launch the Gradio app
- Provide a public URL

## Testing

### Test with Sample Contracts

For testing, you can use:
1. **Sample lease agreement** (any language)
2. **NDA** (any language)
3. **Employment contract** (any language)

### What to Check

- ✅ File upload works (PDF and DOCX)
- ✅ Language detection correct
- ✅ Analysis completes in ~20-30 seconds
- ✅ Output follows specification format
- ✅ All sections present
- ✅ Risk flags make sense
- ✅ Obligations/rights extracted correctly

### Known Limitations (Prototype)

- English prompts only (multilingual prompts coming)
- No user accounts (stateless)
- No history (each analysis is independent)
- No "More" button functionality yet
- Basic error handling
- Single file upload only

## Troubleshooting

### "LLM router not initialized"
- Check that `GROQ_API_KEY` is set in `.env` (local) or Secrets (HF Spaces)
- Verify API key is valid

### "Document appears to be empty"
- PDF might be scanned without OCR
- Try with a different file
- Check file isn't corrupted

### "Cannot reliably analyze"
- Document quality too low
- Try uploading a clearer copy

### Slow analysis (>60 seconds)
- Groq API might be rate-limited
- Try again in a few minutes

## Next Steps

1. **Test with lawyer** using real contracts
2. **Collect feedback** on accuracy
3. **Add multilingual prompts** (Russian, Serbian, French)
4. **Refine prompts** based on test results
5. **Add missing features** (More button, better formatting)

## Support

For issues or questions:
- Check the main documentation in `/docs/`
- Review `decisions.md` for architecture choices
- See `plan.md` for full development roadmap
