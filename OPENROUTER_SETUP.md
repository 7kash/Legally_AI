# OpenRouter Setup Guide

This guide will help you switch from Groq to OpenRouter for the LLM API.

## Why OpenRouter?

- **No rate limits** (with sufficient credits)
- **Multiple models** available (Claude, GPT-4, Llama, Gemini, etc.)
- **Pay-as-you-go** pricing
- **Unified API** for all models

## Step 1: Get OpenRouter API Key

1. Go to https://openrouter.ai/
2. Sign up or log in
3. Go to **Keys** page: https://openrouter.ai/keys
4. Click **Create Key**
5. Copy your API key (starts with `sk-or-v1-...`)

## Step 2: Add Credits (Optional but Recommended)

1. Go to https://openrouter.ai/credits
2. Click **Add Credits**
3. Add at least $5-10 to start
4. OpenRouter shows costs per request, so you can monitor spending

## Step 3: Configure Your .env File

1. Open `/home/user/Legally_AI/backend/.env` (create if doesn't exist)
2. Add these lines:

```bash
# Switch to OpenRouter
LLM_PROVIDER=openrouter

# Your OpenRouter API key
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here

# Choose a model (recommended: Llama 3.1 70B - fast & affordable)
OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct
```

## Step 4: Install OpenAI SDK

The OpenRouter API uses the OpenAI SDK:

```bash
cd /home/user/Legally_AI/backend
pip install openai>=1.0.0
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Step 5: Restart Backend Services

Stop and restart your backend:

```bash
# Stop Celery worker (Ctrl+C if running in terminal)
# Stop FastAPI (Ctrl+C if running in terminal)

# Restart Celery
celery -A app.celery_app worker --loglevel=info &

# Restart FastAPI
uvicorn app.main:app --reload
```

## Step 6: Test the Connection

You can test if OpenRouter is working:

```bash
cd /home/user/Legally_AI/backend
python -c "
from app.services.llm_analysis.llm_router import test_llm_connection
success = test_llm_connection(provider='openrouter')
print('✅ OpenRouter connected!' if success else '❌ Connection failed')
"
```

## Recommended Models

Here are good models to use on OpenRouter:

### Fast & Affordable (Recommended)
```bash
OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct
```
- **Cost**: ~$0.18 per 1M input tokens, ~$0.18 per 1M output tokens
- **Best for**: Contract analysis with high volume
- **Pros**: Very fast, extremely cheap, good quality, supports JSON mode

### Best Quality (Premium)
```bash
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```
- **Cost**: ~$3 per 1M input tokens, ~$15 per 1M output tokens
- **Best for**: Maximum quality analysis
- **Pros**: Excellent reasoning, best at structured output

### Long Context
```bash
OPENROUTER_MODEL=google/gemini-pro-1.5
```
- **Cost**: ~$0.35 per 1M input tokens, ~$1.05 per 1M output tokens
- **Best for**: Very long contracts (100+ pages)
- **Pros**: 1M+ token context window

### OpenAI GPT-4
```bash
OPENROUTER_MODEL=openai/gpt-4-turbo
```
- **Cost**: ~$10 per 1M input tokens, ~$30 per 1M output tokens
- **Best for**: Maximum quality
- **Pros**: Industry standard, reliable

## Estimated Costs

For a typical contract analysis (5-10 pages):
- **Input**: ~5,000 tokens
- **Output**: ~3,000 tokens

**Using Claude 3.5 Sonnet:**
- Input cost: 5,000 × $3/1M = $0.015
- Output cost: 3,000 × $15/1M = $0.045
- **Total per analysis: ~$0.06**

**Using Llama 3.1 70B:**
- Input cost: 5,000 × $0.18/1M = $0.0009
- Output cost: 3,000 × $0.18/1M = $0.00054
- **Total per analysis: ~$0.001**

## Switching Back to Groq

If you want to switch back to Groq later:

```bash
# In .env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_key_here
```

## Troubleshooting

### Error: "OPENROUTER_API_KEY not found"
- Make sure you added it to `/home/user/Legally_AI/backend/.env`
- Make sure the line doesn't have spaces around the `=`
- Restart the backend after changing `.env`

### Error: "OpenAI SDK not installed"
```bash
pip install openai>=1.0.0
```

### Error: "Insufficient credits"
- Go to https://openrouter.ai/credits and add credits
- Minimum $1 to start

### Rate limit errors
- OpenRouter has much higher limits than Groq
- If you still hit limits, consider upgrading your OpenRouter plan

## Monitoring Usage

Check your OpenRouter usage:
1. Go to https://openrouter.ai/activity
2. See all requests, costs, and models used
3. Monitor spending in real-time

## Support

- OpenRouter Discord: https://discord.gg/openrouter
- OpenRouter Docs: https://openrouter.ai/docs
