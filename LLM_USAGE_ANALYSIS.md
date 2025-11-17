# LLM Usage Analysis - OpenRouter Cost Investigation

**Date**: 2025-11-17
**Purpose**: Analyze all LLM API calls to understand OpenRouter credit consumption

## Summary

Your application makes **2 LLM calls per contract analysis**, plus **additional calls for ELI5 simplification** if requested.

### Current Issue: ELI5 Service is BROKEN ❌
The ELI5 service calls `llm_router.call_llm()` but this method doesn't exist. It should call `llm_router.call()`. This means ELI5 is currently throwing errors and wasting API credits on failed requests.

---

## LLM Calls Per Analysis

### Regular Contract Analysis (without ELI5)

| Call # | Function | Purpose | Prompt Size | Expected Tokens | Max Output Tokens |
|--------|----------|---------|-------------|-----------------|-------------------|
| 1 | `run_step1_preparation()` | Extract metadata, detect document type | ~15,000 chars (~5,000 tokens) | ~5,500 total | 8,000 |
| 2 | `run_step2_analysis()` | Extract obligations, rights, risks | ~15,000 chars (~5,000 tokens) | ~5,500 total | 8,000 |

**Total for basic analysis**: **2 LLM calls**

### ELI5 Simplification (when user clicks "Explain like I'm 5")

When a user enables ELI5 mode, the app calls `simplify_analysis_section()` which makes **1 LLM call per item** in:
- Obligations
- Rights
- Risks
- Mitigations (newly added)

**Example with typical contract**:
- 5 obligations × 1 call each = 5 calls
- 5 rights × 1 call each = 5 calls
- 5 risks × 1 call each = 5 calls
- 5 mitigations × 1 call each = 5 calls

**Total ELI5 calls**: **~20 LLM calls** (for a typical contract with 5 items per section)

---

## Detailed Breakdown

### Call 1: Step 1 Preparation

**File**: `backend/app/services/llm_analysis/step1_preparation.py:92`

**Prompt Template**: `backend/app/services/llm_analysis/prompts/preparation_en.txt` (124 lines)

**Input Size**:
- System prompt: ~50 tokens
- Prompt template: ~800 tokens
- Contract text: First 15,000 characters (~5,000 tokens)
- **Total input**: ~5,850 tokens

**Output Size**: JSON response ~500-1,500 tokens

**Purpose**: Extract metadata like:
- Agreement type & subtype
- User role
- Parties
- Negotiability assessment
- Governing language
- Jurisdiction & timezone
- Version status (draft/signed)
- Referenced documents
- Key dates & amounts

**Code**:
```python
result = llm_router.call_with_json(
    prompt=prompt,
    system_prompt="You are a legal document analyst. Extract information accurately and return valid JSON."
)
```

**Settings**:
- Temperature: 0.1 (default)
- Max tokens: 8,000 (default)
- JSON mode: Yes

---

### Call 2: Step 2 Analysis

**File**: `backend/app/services/llm_analysis/step2_analysis.py:52`

**Prompt Template**: `backend/app/services/llm_analysis/prompts/analysis_en.txt` (183 lines)

**Input Size**:
- System prompt: ~60 tokens
- Prompt template: ~1,500 tokens
- Preparation data summary: ~100 tokens
- Contract text: First 15,000 characters (~5,000 tokens)
- **Total input**: ~6,660 tokens

**Output Size**: JSON response ~2,000-4,000 tokens (large structured output)

**Purpose**: Extract detailed analysis:
- About summary (2-3 sentences)
- Payment terms (7 fields)
- Obligations (up to 5, each with 6 fields)
- Rights (up to 5, each with 5 fields)
- Risks (up to 5, each with 6 fields)
- Gaps & anomalies (up to 5)
- Calendar items (all deadlines)
- Suggestions (up to 5)
- Mitigations (up to 5)
- Screening result

**Code**:
```python
result = llm_router.call_with_json(
    prompt=prompt,
    system_prompt="You are a legal document analyst helping non-lawyers understand contracts. Be clear, specific, and actionable."
)
```

**Settings**:
- Temperature: 0.1 (default)
- Max tokens: 8,000 (default)
- JSON mode: Yes

---

### Call 3+: ELI5 Simplification (PER ITEM) ⚠️ HIGH COST

**File**: `backend/app/services/llm_analysis/eli5_service.py:55`

**⚠️ CRITICAL BUG**: This function calls `llm_router.call_llm()` which **DOES NOT EXIST**. The method should be `llm_router.call()`.

**Prompt Template**: Inline ELI5 template (35 lines)

**Input Size PER CALL**:
- System prompt: ~30 tokens
- Prompt template: ~200 tokens
- Item text to simplify: ~100-300 tokens
- **Total input per call**: ~330-530 tokens

**Output Size**: ~100-300 tokens (simplified text)

**Frequency**:
- **1 call for EACH obligation** (typically 5 calls)
- **1 call for EACH right** (typically 5 calls)
- **1 call for EACH risk** (typically 5 calls)
- **1 call for EACH mitigation** (typically 5 calls)
- **Total**: ~20 calls per contract

**Code** (BUGGY):
```python
simplified = llm_router.call_llm(  # ❌ THIS METHOD DOESN'T EXIST
    prompt=prompt,
    system_prompt="You are a helpful teacher who explains complex legal concepts in simple, everyday language that anyone can understand.",
    temperature=0.7,  # Higher for conversational tone
    max_tokens=1000
)
```

**Settings**:
- Temperature: 0.7 (higher than analysis)
- Max tokens: 1,000
- JSON mode: No

---

## Token Usage Calculations

### Model Used
- **OpenRouter Model**: `meta-llama/llama-3.1-70b-instruct` (default)
- **Pricing** (as of 2024):
  - Input: $0.52 per 1M tokens
  - Output: $0.75 per 1M tokens

### Cost Per Analysis (WITHOUT ELI5)

| Call | Input Tokens | Output Tokens | Input Cost | Output Cost | Total |
|------|--------------|---------------|------------|-------------|-------|
| Step 1 | 5,850 | 1,000 | $0.003 | $0.001 | $0.004 |
| Step 2 | 6,660 | 3,000 | $0.003 | $0.002 | $0.005 |
| **Total** | **12,510** | **4,000** | **$0.006** | **$0.003** | **$0.009** |

**Cost per basic analysis**: **~$0.01 per contract**

### Cost Per Analysis (WITH ELI5)

Assuming 20 ELI5 calls (5 items × 4 sections):

| Call Type | Calls | Input Tokens Each | Output Tokens Each | Total Input | Total Output |
|-----------|-------|-------------------|-------------------|-------------|--------------|
| Basic (above) | 2 | - | - | 12,510 | 4,000 |
| ELI5 | 20 | 400 | 200 | 8,000 | 4,000 |
| **Total** | **22** | - | - | **20,510** | **8,000** |

**Cost breakdown**:
- Input: 20,510 tokens × $0.52 / 1M = $0.011
- Output: 8,000 tokens × $0.75 / 1M = $0.006
- **Total cost per analysis with ELI5**: **~$0.017**

---

## Cost Optimization Recommendations

### 🔴 CRITICAL: Fix ELI5 Bug First

The ELI5 service is calling a non-existent method, which is causing errors and wasting credits.

**Fix**: Change `llm_router.call_llm()` to `llm_router.call()` in `eli5_service.py:55`

### 🟡 HIGH PRIORITY: Batch ELI5 Calls

**Current**: 20 separate LLM calls for ELI5 (one per item)
**Optimized**: 4 LLM calls (one per section)

**How**: Instead of simplifying each obligation individually, batch all 5 obligations into a single LLM call.

**Savings**:
- Reduce 20 calls → 4 calls
- Save ~80% on ELI5 costs
- **New ELI5 cost**: ~$0.004 (instead of $0.017)

**Implementation**:
```python
# Instead of:
for item in obligations:
    simplify_obligation(item, llm_router)

# Do:
simplified_obligations = simplify_obligations_batch(obligations, llm_router)
```

### 🟡 MEDIUM PRIORITY: Cache ELI5 Results

If the same contract is analyzed multiple times, cache the ELI5 results in the database.

**Savings**: 100% on repeat ELI5 requests for same contract

### 🟢 LOW PRIORITY: Reduce Prompt Verbosity

The prompts are quite verbose. You could reduce prompt size by ~20% without losing quality:
- Remove redundant instructions
- Use more concise language
- Reduce examples

**Savings**: ~$0.001 per analysis

### 🟢 LOW PRIORITY: Use Cheaper Model for ELI5

ELI5 is a simpler task that doesn't require 70B parameter model.

**Options**:
- `meta-llama/llama-3.1-8b-instruct`: ~85% cheaper
- `anthropic/claude-3-haiku`: Fast and cheap

**Savings**: ~80% on ELI5 calls = ~$0.005 per analysis with ELI5

---

## Estimated Monthly Costs

### Scenario 1: 100 Analyses/Month (No ELI5)
- 100 × $0.009 = **$0.90/month**

### Scenario 2: 100 Analyses/Month (50% with ELI5)
- 50 × $0.009 = $0.45
- 50 × $0.017 = $0.85
- **Total**: **$1.30/month**

### Scenario 3: 1,000 Analyses/Month (50% with ELI5)
- 500 × $0.009 = $4.50
- 500 × $0.017 = $8.50
- **Total**: **$13.00/month**

### With Optimizations Applied:
- 500 × $0.009 = $4.50
- 500 × $0.013 = $6.50 (batched ELI5)
- **Total**: **$11.00/month** (15% savings)

---

## Debug: Why Am I Spending Too Much?

### Check 1: How Many Analyses Are Running?

```bash
# Check database for number of analyses
cd /home/user/Legally_AI
python -c "
from backend.app.database import SessionLocal
from backend.app.models import Analysis
db = SessionLocal()
count = db.query(Analysis).count()
print(f'Total analyses: {count}')
succeeded = db.query(Analysis).filter(Analysis.status == 'succeeded').count()
print(f'Successful analyses: {succeeded}')
"
```

### Check 2: Are You Testing/Debugging Frequently?

Each time you upload a contract and analyze it, that's $0.009-$0.017 in API costs.

**Common causes of high costs**:
- ✅ Running multiple test analyses per day
- ✅ Re-analyzing same contract repeatedly
- ✅ Testing ELI5 functionality (20 extra calls!)
- ✅ Frontend polling causing duplicate requests
- ❌ Infinite loops or retry logic gone wrong

### Check 3: OpenRouter Usage Dashboard

Check your actual usage at: https://openrouter.ai/activity

Look for:
- Number of requests
- Token usage
- Model used
- Failed requests (wasted credits)

### Check 4: Backend Logs

Check if there are failed/retried LLM calls:

```bash
cd /home/user/Legally_AI
tail -100 backend/logs/app.log | grep "LLM"
```

---

## Action Items

1. **[CRITICAL]** Fix ELI5 bug: `call_llm()` → `call()`
2. **[HIGH]** Implement batched ELI5 calls (4 calls instead of 20)
3. **[MEDIUM]** Add ELI5 result caching to database
4. **[LOW]** Consider cheaper model for ELI5 simplification
5. **[MONITORING]** Set up usage alerts in OpenRouter dashboard

---

## Files Reference

**LLM Router**: `backend/app/services/llm_analysis/llm_router.py`
**Step 1**: `backend/app/services/llm_analysis/step1_preparation.py`
**Step 2**: `backend/app/services/llm_analysis/step2_analysis.py`
**ELI5**: `backend/app/services/llm_analysis/eli5_service.py`
**Prompts**: `backend/app/services/llm_analysis/prompts/`
**Task**: `backend/app/tasks/analyze_contract.py`

---

## Conclusion

Your **high OpenRouter costs** are likely due to:

1. **ELI5 making 20 individual LLM calls** instead of 4 batched calls (16 extra calls = $0.008 wasted)
2. **ELI5 bug** calling non-existent method (causing errors and retries)
3. **Testing/debugging** - Each contract analysis costs ~$0.01
4. **No caching** - Re-analyzing same contract wastes money

**Immediate fix**: Fix the ELI5 bug
**Biggest optimization**: Batch ELI5 calls (80% cost reduction for ELI5)
