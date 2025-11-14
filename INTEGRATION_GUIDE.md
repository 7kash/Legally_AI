# LLM Analysis Integration Guide

This guide explains how to integrate the LLM-based contract analysis from the `prototype/` directory into the main application.

## Current State

The application is fully functional with **placeholder analysis results**. The infrastructure for real-time analysis, text extraction, and results display is working perfectly.

**What needs integration**: The actual LLM-based contract analysis logic from `prototype/src/`.

## Integration Steps

### Step 1: Review Prototype Structure

First, examine the prototype code to understand the analysis pipeline:

```bash
ls -la prototype/src/
```

Expected structure:
```
prototype/src/
├── step1_preparation.py    # Document preparation & metadata extraction
├── step2_analysis.py        # Contract clause analysis
├── formatter.py             # Output formatting
├── llm_client.py           # GROQ API client
└── prompts/                # LLM prompts
```

### Step 2: Add Prototype to Python Path

Update `backend/app/tasks/analyze_contract.py` to import from prototype:

```python
import sys
from pathlib import Path

# Add prototype to Python path
prototype_path = Path(__file__).parent.parent.parent.parent / "prototype"
if str(prototype_path) not in sys.path:
    sys.path.insert(0, str(prototype_path))
```

### Step 3: Integrate Step 1 - Document Preparation

Replace the placeholder in `analyze_contract_task`:

**Before (placeholder):**
```python
preparation_result = {
    "agreement_type": "Unknown",
    "parties": [],
    "jurisdiction": contract.jurisdiction or "Unknown",
    "negotiability": "medium"
}
```

**After (real implementation):**
```python
from prototype.src.step1_preparation import run_preparation

try:
    preparation_result = run_preparation(
        contract_text=contract.extracted_text,
        output_language=output_language,
        jurisdiction=contract.jurisdiction
    )
except Exception as e:
    logger.error(f"Preparation step failed: {e}")
    # Fall back to placeholder if LLM fails
    preparation_result = {
        "agreement_type": "Error: Could not analyze",
        "parties": [],
        "jurisdiction": contract.jurisdiction or "Unknown",
        "error": str(e)
    }
```

### Step 4: Integrate Step 2 - Contract Analysis

Replace the analysis placeholder:

**Before:**
```python
analysis_result = {
    "obligations": [],
    "rights": [],
    "risks": [],
    "payment_terms": {},
    "key_dates": []
}
```

**After:**
```python
from prototype.src.step2_analysis import run_analysis

try:
    analysis_result = run_analysis(
        contract_text=contract.extracted_text,
        preparation_data=preparation_result,
        output_language=output_language
    )
except Exception as e:
    logger.error(f"Analysis step failed: {e}")
    analysis_result = {
        "obligations": [],
        "rights": [],
        "risks": [f"Error during analysis: {str(e)}"],
        "payment_terms": {},
        "key_dates": []
    }
```

### Step 5: Configure GROQ API Key

The prototype uses GROQ for LLM access. Configure the API key:

**1. Create/Update `.env` file in backend directory:**
```bash
cd backend
nano .env  # or use your preferred editor
```

**2. Add GROQ API key:**
```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/legally_ai
REDIS_URL=redis://redis:6379/0
```

**3. Verify it's passed to containers** (already configured in docker-compose.yml):
```yaml
environment:
  GROQ_API_KEY: ${GROQ_API_KEY}
```

### Step 6: Install Additional Dependencies

Check if prototype has additional requirements:

```bash
# Check prototype requirements
cat prototype/requirements.txt

# Add any missing dependencies to backend/requirements.txt
```

Common additions might include:
- `tiktoken` - for token counting
- `langchain` - if used in prototype
- Additional LLM libraries

### Step 7: Update Formatted Output

The prototype might return results in a different format. Update the formatting section:

```python
from prototype.src.formatter import format_analysis

formatted_output = format_analysis(
    preparation_result=preparation_result,
    analysis_result=analysis_result,
    output_language=output_language
)
```

### Step 8: Test with Real Contracts

After integration:

1. **Restart services:**
```bash
cd backend
docker compose down
docker compose up -d --build
```

2. **Upload a test contract** at http://localhost:3000/upload

3. **Monitor Celery logs** to see LLM API calls:
```bash
docker compose logs celery -f
```

4. **Check for errors:**
   - GROQ API connectivity issues
   - Token limit exceeded
   - Rate limiting
   - Invalid prompt formatting

## Error Handling Best Practices

### 1. API Failures
```python
try:
    llm_response = call_groq_api(prompt)
except APIError as e:
    logger.error(f"GROQ API error: {e}")
    # Return graceful fallback
    return {
        "status": "partial",
        "error": "LLM service unavailable",
        "fallback_data": {...}
    }
```

### 2. Token Limits
```python
# Truncate very long contracts
if len(contract_text) > 50000:
    logger.warning("Contract too long, truncating")
    contract_text = contract_text[:50000] + "..."
```

### 3. Retry Logic
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def call_llm_with_retry(prompt):
    return groq_client.chat.completions.create(...)
```

## Testing Checklist

After integration, verify:

- [ ] Text extraction still works
- [ ] GROQ API key is correctly loaded
- [ ] LLM API calls succeed
- [ ] Real analysis results are returned
- [ ] Results are properly formatted as JSON
- [ ] Frontend displays results correctly
- [ ] Error cases are handled gracefully
- [ ] Different contract types work (PDF, DOCX)
- [ ] Multiple languages work (EN, RU, FR, SR)
- [ ] Analysis completes within reasonable time (<2 minutes)

## Monitoring & Debugging

### Check Celery Logs
```bash
docker compose logs celery -f | grep -i "groq\|llm\|analysis"
```

### Check API Logs
```bash
docker compose logs api -f | grep -i "error\|warning"
```

### Database Inspection
```bash
# Check latest analysis
docker compose exec postgres psql -U postgres -d legally_ai -c "
SELECT id, status, LENGTH(formatted_output::text) as result_length
FROM analyses
ORDER BY created_at DESC
LIMIT 5;
"
```

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'prototype'`
**Solution**: Ensure prototype is added to sys.path (Step 2)

**Issue**: `groq.AuthenticationError: Invalid API key`
**Solution**: Check GROQ_API_KEY in .env file

**Issue**: Analysis takes too long (>5 minutes)
**Solution**: Reduce contract length or use faster GROQ model

**Issue**: Results not displaying on frontend
**Solution**: Check that formatted_output matches expected JSON structure

## Performance Optimization

### 1. Cache LLM Responses
```python
from functools import lru_cache
import hashlib

def get_text_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

# Cache analysis for identical contracts
@lru_cache(maxsize=100)
def analyze_with_cache(text_hash, output_language):
    # ... perform analysis
```

### 2. Use Streaming Responses
```python
# Stream LLM responses for better UX
for chunk in groq_client.chat.completions.create(
    stream=True,
    ...
):
    # Send progress updates via SSE
    create_event(db, analysis_id, "progress", chunk)
```

### 3. Batch Similar Requests
If analyzing multiple contracts, batch LLM calls to reduce API overhead.

## Next Steps After Integration

1. **Add Confidence Scoring** - Rate the quality of LLM analysis
2. **Implement Feedback Loop** - Use user corrections to improve prompts
3. **Add Caching** - Avoid re-analyzing identical contracts
4. **Language Detection** - Auto-detect contract language
5. **Export Functionality** - PDF/DOCX export of analysis results
6. **Comparison View** - Compare multiple contract versions

## Resources

- **GROQ Docs**: https://console.groq.com/docs
- **LLM Prompting Guide**: Best practices for contract analysis
- **Error Handling**: Robust error handling patterns
- **Rate Limiting**: Handle API quota limits gracefully

---

**Status**: Ready for LLM integration
**Next Action**: Review prototype code and begin Step 1 integration
