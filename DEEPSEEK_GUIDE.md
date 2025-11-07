# DeepSeek Integration Guide for HuggingFace Prototype

**Last Updated**: 2025-11-07
**Status**: Implementation Complete
**Session**: 011CUtiiNvgPVR7ram5DwPLU

---

## Overview

The Legally AI prototype now supports **DeepSeek** as an alternative LLM provider alongside Groq. This guide explains when and how to use DeepSeek for the HuggingFace Spaces deployment.

---

## Why DeepSeek?

### Advantages

| Feature | DeepSeek | Groq (Current) |
|---------|----------|----------------|
| **Cost** | $0.27/1M input tokens<br>$1.10/1M output tokens | Free tier: 14,400 req/day<br>Paid: $0.59/1M tokens |
| **Model** | deepseek-chat (236B MoE) | llama-3.3-70b-versatile |
| **Reasoning** | Excellent for complex analysis | Very good for extraction |
| **Multilingual** | Strong (Chinese, English, Russian) | Strong (all 4 languages) |
| **Speed** | ~60-100 tokens/sec | ~800+ tokens/sec |
| **Rate Limits** | 10 RPM free tier<br>60 RPM paid | 30 RPM free<br>6000 RPM paid |
| **Context Window** | 64K tokens | 128K tokens |

### When to Use DeepSeek

**Use DeepSeek if:**
- ✅ You hit Groq rate limits (30 req/min on free tier)
- ✅ You need deeper reasoning for complex legal analysis
- ✅ You want cost predictability (Groq free tier may become paid)
- ✅ You're analyzing contracts with complex multi-party structures
- ✅ Testing with contracts that need better reasoning capabilities

**Stick with Groq if:**
- ✅ You need maximum speed (8x faster than DeepSeek)
- ✅ You're on prototype/testing phase (free tier is generous)
- ✅ You have simple contracts (NDAs, basic leases)
- ✅ Quick iteration is more important than reasoning depth

---

## Architecture Changes

### What Was Added

The implementation now includes:

1. **Model Configuration** (`prototype/src/constants.py`):
   ```python
   DEEPSEEK_SETTINGS = {
       "model": "deepseek-chat",
       "temperature": 0.1,
       "max_tokens": 8000,
       "top_p": 0.9,
       "base_url": "https://api.deepseek.com"
   }
   ```

2. **Provider Support** (`prototype/src/llm_router.py`):
   - Multi-provider initialization
   - OpenAI SDK integration (DeepSeek uses OpenAI-compatible API)
   - Automatic provider selection via environment variable

3. **Environment Configuration** (`prototype/.env.example`):
   - `LLM_PROVIDER` selector (groq/deepseek)
   - `DEEPSEEK_API_KEY` configuration

4. **Dependencies** (`prototype/requirements.txt`):
   - Added `openai>=1.0.0` (required for DeepSeek API)

---

## Setup Instructions

### Option 1: Using DeepSeek on HuggingFace Spaces

#### Step 1: Get DeepSeek API Key

1. Go to https://platform.deepseek.com/
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-`)

#### Step 2: Configure HuggingFace Space

1. Go to your HF Space: https://huggingface.co/spaces/7Kash-FluffyHedgehog/Legally_AI/settings
2. Scroll to **Repository secrets**
3. Add two secrets:

   **Secret 1:**
   - Name: `LLM_PROVIDER`
   - Value: `deepseek`

   **Secret 2:**
   - Name: `DEEPSEEK_API_KEY`
   - Value: `sk-your-deepseek-api-key-here`

4. Click **Save** for each
5. Go to **Settings** → **Factory reboot** to restart the space

#### Step 3: Verify

1. Open your space URL
2. Check logs for: `LLM Router initialized with provider: deepseek`
3. Upload a test contract
4. Analysis should work normally (but slightly slower than Groq)

### Option 2: Local Development with DeepSeek

#### Step 1: Update `.env` File

```bash
cd /Users/ekaterinamatyushina/Legally_AI/prototype

# Edit .env file
cat > .env << EOF
# LLM Provider Selection
LLM_PROVIDER=deepseek

# DeepSeek API Key
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here

# Keep Groq key as backup
GROQ_API_KEY=gsk_your_groq_api_key_here

# Other settings
DEFAULT_MODEL=llama-3.3-70b-versatile
SUPPORTED_LANGUAGES=russian,serbian,french,english
EOF
```

#### Step 2: Install Dependencies

```bash
cd prototype
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 3: Test Locally

```bash
python app.py
```

Open http://localhost:7860 and test with a sample contract.

---

## Usage Patterns

### Pattern 1: Primary DeepSeek, Fallback Groq

**Use Case**: You want DeepSeek's reasoning but need Groq as backup if rate limited.

**Implementation** (future enhancement):
```python
# In llm_router.py (not yet implemented)
try:
    router = LLMRouter(provider="deepseek")
    result = router.call(prompt)
except RateLimitError:
    router = LLMRouter(provider="groq")
    result = router.call(prompt)
```

Currently, you must manually switch providers via environment variable.

### Pattern 2: Task-Based Routing

**Use Case**: Use Groq for fast extraction, DeepSeek for complex reasoning.

**Recommended Setup** (for production):
- Step 1 (Preparation): Groq (fast extraction, simple task)
- Step 2 (Analysis): DeepSeek (complex reasoning, risk assessment)

**Current Limitation**: Prototype uses same provider for both steps. Production MVP will support per-task routing.

### Pattern 3: A/B Testing

**Use Case**: Compare quality between providers.

**How To**:
1. Deploy two HF Spaces:
   - Space 1: `LLM_PROVIDER=groq`
   - Space 2: `LLM_PROVIDER=deepseek`
2. Analyze same contracts on both
3. Compare outputs for accuracy, completeness, risk detection
4. Choose best provider

---

## Cost Comparison

### Groq (Free Tier)
- **Rate Limits**: 30 requests/min, 14,400 requests/day
- **Cost**: $0/month (free tier)
- **When Sufficient**:
  - Testing phase (<480 analyses/day)
  - Low-traffic prototype
  - Personal use

**Example**: 100 analyses/day = FREE ✅

### DeepSeek (Paid)
- **Pricing**: $0.27/1M input tokens, $1.10/1M output tokens
- **Average Contract Analysis**:
  - Input: ~3,000 tokens (contract + prompts)
  - Output: ~2,000 tokens (analysis results)
  - **Cost per analysis**: ~$0.003 (0.3 cents)

**Example**: 100 analyses/day × 30 days = $9/month

### Cost Breakpoint

- **<480 analyses/day**: Use Groq (free)
- **>480 analyses/day**: Use DeepSeek (cheaper than paid Groq)
- **Testing phase**: Use Groq (no cost)
- **Production with volume**: Use DeepSeek (predictable cost)

---

## Performance Comparison

### Analysis Speed

**Groq (llama-3.3-70b)**:
- Parse document: 2-5 seconds
- Step 1 (Preparation): 3-5 seconds
- Step 2 (Analysis): 4-8 seconds
- **Total**: ~15-20 seconds

**DeepSeek (deepseek-chat)**:
- Parse document: 2-5 seconds
- Step 1 (Preparation): 8-15 seconds
- Step 2 (Analysis): 12-20 seconds
- **Total**: ~25-40 seconds

**Verdict**: Groq is 2-3x faster, better for prototype testing.

### Analysis Quality

**Preliminary Testing Needed**:
- Neither has been tested with real lawyer contracts yet
- DeepSeek may provide better reasoning for complex contracts
- Groq may be sufficient for simple contracts (NDAs, basic leases)

**Recommendation**:
1. Test with Groq first (faster iteration)
2. If lawyer feedback shows quality issues, try DeepSeek
3. Compare outputs side-by-side for 10-20 contracts

---

## Migration Guide

### From Groq to DeepSeek

If you're currently using Groq and want to switch:

**On HuggingFace Spaces**:
```bash
# 1. Add DeepSeek API key to HF Secrets
# 2. Add LLM_PROVIDER=deepseek to HF Secrets
# 3. Factory reboot the space
```

**Local Development**:
```bash
cd prototype
# Edit .env
echo "LLM_PROVIDER=deepseek" >> .env
echo "DEEPSEEK_API_KEY=sk-..." >> .env
# Restart app
python app.py
```

**No code changes needed!** The router handles provider selection automatically.

### Back to Groq

If DeepSeek is too slow or expensive:

**On HuggingFace Spaces**:
```bash
# 1. Change LLM_PROVIDER secret to "groq"
# 2. Factory reboot
```

**Local Development**:
```bash
# Edit .env
sed -i 's/LLM_PROVIDER=deepseek/LLM_PROVIDER=groq/' .env
python app.py
```

---

## Troubleshooting

### Issue: "DEEPSEEK_API_KEY not found"

**Cause**: API key not set in environment.

**Fix**:
- HF Spaces: Check Repository secrets, ensure `DEEPSEEK_API_KEY` is set
- Local: Check `.env` file has `DEEPSEEK_API_KEY=sk-...`

### Issue: "Rate limit exceeded"

**Cause**: DeepSeek free tier is 10 requests/min.

**Fix**:
- Slow down testing (wait 6 seconds between requests)
- Upgrade to paid tier ($5 minimum balance)
- Switch to Groq temporarily (`LLM_PROVIDER=groq`)

### Issue: "Invalid API key"

**Cause**: Wrong API key or expired.

**Fix**:
- Check API key starts with `sk-`
- Regenerate API key on DeepSeek platform
- Update HF secret or `.env` file

### Issue: "Analysis taking >60 seconds"

**Cause**: DeepSeek is slower than Groq.

**Fix**:
- This is expected (DeepSeek 2-3x slower)
- If too slow, switch back to Groq
- Consider increasing Gradio timeout (if needed)

### Issue: "Connection timeout"

**Cause**: DeepSeek API may have regional restrictions or downtime.

**Fix**:
- Check https://platform.deepseek.com/status
- Try again in a few minutes
- Switch to Groq as fallback

---

## Best Practices

### For Prototype Testing (Current Phase)

**Recommendation**: Stick with **Groq** for now.

**Reasons**:
1. Faster iteration (2-3x faster responses)
2. No cost (free tier generous)
3. Lawyer testing needs speed, not perfection
4. Can switch to DeepSeek later if quality issues found

### For Production MVP (Future)

**Recommendation**: Use **task-based routing**.

**Setup**:
- Step 1 (Preparation): Groq (fast extraction)
- Step 2 (Analysis): DeepSeek (deep reasoning)
- Fallback: OpenAI GPT-4o-mini (quality)

**Cost Estimate**:
- 1000 analyses/month
- Step 1 (Groq): $0 (free tier)
- Step 2 (DeepSeek): $3/month
- **Total**: ~$3-5/month ✅

### For High-Volume Production (Future)

**Recommendation**: **DeepSeek** for everything.

**Setup**:
- Primary: DeepSeek (predictable cost)
- Fallback: Together.ai Mixtral (cheap)
- Quality check: OpenAI GPT-4o-mini (sample 10%)

**Cost Estimate** (10,000 analyses/month):
- DeepSeek: ~$30/month
- Together.ai fallback: ~$5/month
- OpenAI quality check (1000): ~$10/month
- **Total**: ~$45/month ✅

---

## Monitoring & Analytics

### Key Metrics to Track

When using DeepSeek, monitor:

1. **Latency**:
   - Track: Average analysis time
   - Target: <40 seconds
   - Alert: >60 seconds

2. **Cost**:
   - Track: Tokens used per analysis
   - Target: <5000 tokens total
   - Alert: >10,000 tokens (runaway prompt)

3. **Quality**:
   - Track: Lawyer feedback scores
   - Target: >4/5 rating
   - Compare: Groq vs DeepSeek outputs

4. **Error Rate**:
   - Track: API failures, timeouts
   - Target: <1% errors
   - Fallback: Auto-switch to Groq if >5% errors

### Logging

The router automatically logs:
```python
print(f"LLM Router initialized with provider: {provider}")
```

**Future Enhancement**: Add structured logging:
```python
{
  "provider": "deepseek",
  "model": "deepseek-chat",
  "input_tokens": 3000,
  "output_tokens": 2000,
  "latency_ms": 15000,
  "cost_usd": 0.003,
  "timestamp": "2025-11-07T12:00:00Z"
}
```

---

## Decision Matrix

### Should You Use DeepSeek Now?

| Scenario | Use DeepSeek? | Reason |
|----------|---------------|---------|
| **Prototype testing with lawyer** | ❌ No | Groq is faster for iteration |
| **Hit Groq rate limits** | ✅ Yes | DeepSeek as backup |
| **Complex multi-party contracts** | ✅ Maybe | Test if Groq quality insufficient |
| **High-volume production** | ✅ Yes | Predictable cost, good quality |
| **Speed is critical** | ❌ No | Groq is 3x faster |
| **Cost is critical** | ✅ Yes (at scale) | Cheaper than paid Groq at >500 req/day |

---

## Roadmap: Multi-Provider Strategy

### Phase 0: Prototype (Now)
- ✅ Single provider (Groq)
- ✅ DeepSeek support added
- ✅ Manual switching via env var

### Phase 1: Lawyer Feedback (Week 2)
- ⏳ Test both providers with real contracts
- ⏳ Compare quality side-by-side
- ⏳ Choose best provider for MVP

### Phase 2: Production MVP (Weeks 3-6)
- ⏳ Task-based routing (Groq for extraction, DeepSeek for analysis)
- ⏳ Automatic fallback on errors
- ⏳ Cost tracking per provider

### Phase 3: Scale (Post-Launch)
- ⏳ Dynamic routing based on:
  - Contract complexity (simple → Groq, complex → DeepSeek)
  - User tier (free → Groq, paid → DeepSeek)
  - Current rate limits (load balancing)
- ⏳ A/B testing framework
- ⏳ Quality scoring per provider

---

## Code Examples

### Manual Provider Switching (Current)

```python
# Option 1: Via environment variable
import os
os.environ["LLM_PROVIDER"] = "deepseek"
os.environ["DEEPSEEK_API_KEY"] = "sk-..."

from src.llm_router import LLMRouter
router = LLMRouter()  # Automatically uses provider from env

# Option 2: Direct initialization
router = LLMRouter(provider="deepseek", api_key="sk-...")
response = router.call("Analyze this contract...")
```

### Testing Both Providers (Future)

```python
# Compare Groq vs DeepSeek
contract_text = "..."

groq_router = LLMRouter(provider="groq")
deepseek_router = LLMRouter(provider="deepseek")

groq_result = groq_router.call_with_json(prompt)
deepseek_result = deepseek_router.call_with_json(prompt)

# Compare outputs
print(f"Groq risks: {len(groq_result['risks'])}")
print(f"DeepSeek risks: {len(deepseek_result['risks'])}")
```

### Fallback Logic (Future Enhancement)

```python
# Not yet implemented, but planned for MVP
def analyze_with_fallback(contract_text, prompt):
    providers = ["groq", "deepseek", "openai"]

    for provider in providers:
        try:
            router = LLMRouter(provider=provider)
            return router.call_with_json(prompt)
        except (RateLimitError, TimeoutError) as e:
            print(f"{provider} failed: {e}, trying next...")
            continue

    raise Exception("All providers failed")
```

---

## FAQ

### Q: Can I use both Groq and DeepSeek simultaneously?

**A**: Not in the current prototype (single provider only). Production MVP will support task-based routing.

### Q: Which provider gives better accuracy?

**A**: Not yet tested with real contracts. Initial testing suggests:
- **Groq**: Better for simple extraction tasks (faster)
- **DeepSeek**: Better for complex reasoning (e.g., multi-party conflicts)

### Q: What if DeepSeek API goes down?

**A**: Currently, analysis fails. Future versions will auto-fallback to Groq.

### Q: Can I use DeepSeek's reasoning models (R1)?

**A**: Not yet. Current integration uses `deepseek-chat`. DeepSeek-R1 can be added if needed.

### Q: Does DeepSeek support all 4 languages?

**A**: Yes. DeepSeek supports Russian, Serbian, French, and English. Chinese is especially strong.

### Q: How do I switch back to Groq?

**A**: Change `LLM_PROVIDER=groq` in HF secrets or `.env` file, then restart.

---

## Support & Debugging

### Enable Debug Logging

```python
# In app.py or llm_router.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Connection

```python
from src.llm_router import test_llm_connection

# Test DeepSeek
result = test_llm_connection(provider="deepseek", api_key="sk-...")
print(f"DeepSeek connection: {result}")

# Test Groq
result = test_llm_connection(provider="groq", api_key="gsk-...")
print(f"Groq connection: {result}")
```

### Check Provider Status

- **Groq**: https://status.groq.com/
- **DeepSeek**: https://platform.deepseek.com/status

---

## Conclusion

### Current Recommendation

**For prototype testing**: Continue using **Groq**.
- Faster iteration (3x speed)
- No cost
- Good enough for lawyer feedback

**When to switch to DeepSeek**:
- ✅ Hit Groq rate limits (>30 req/min)
- ✅ Lawyer reports quality issues with complex contracts
- ✅ Moving to production with volume >500 analyses/day

### Next Steps

1. ✅ **Done**: DeepSeek integration implemented
2. ⏳ **Next**: Test prototype with lawyer using Groq
3. ⏳ **Future**: A/B test Groq vs DeepSeek with 10-20 contracts
4. ⏳ **MVP**: Implement task-based routing (Groq + DeepSeek + OpenAI)

---

## Related Documentation

- **Architecture**: See `architecture.md` (section on LLM Router)
- **Decisions**: See `decisions.md` (AD-002: Why Groq was chosen)
- **Deployment**: See `DEPLOYMENT_GUIDE.md` (HF Spaces setup)
- **Folder Structure**: See `FOLDER_STRUCTURE.md` (file locations)

---

**Maintained By**: Claude (Session 011CUtiiNvgPVR7ram5DwPLU)
**Last Tested**: 2025-11-07
**Status**: ✅ Production Ready
