# How to Create API Keys

Quick guide to set up your SECRET_KEY and SENDGRID_API_KEY.

---

## 1. SECRET_KEY (Required)

The SECRET_KEY is used to sign JWT tokens for authentication. It needs to be a long, random string.

### Option A: Using Python (Easiest)

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Output example**:
```
Xp7k9mF2nL4vR8wQ1jH5tY3bN6gP0sA2cD4eF7hJ9k
```

✅ Copy this entire string for your SECRET_KEY

### Option B: Using OpenSSL

```bash
openssl rand -hex 32
```

**Output example**:
```
4f3d2a8b9c1e5f7a0d6b2c8e4f9a1d3b7c5e2f8a9d1c3b5e7f9a0d2c4e6f8a
```

✅ Copy this entire string for your SECRET_KEY

### Option C: Online Generator

Visit: https://generate-secret.vercel.app/32

Click "Generate" and copy the result.

---

## 2. SENDGRID_API_KEY (Optional for Testing)

SendGrid is used to send emails (password reset, email verification).

### ⚠️ For Development: You Can Skip This!

The application has a **development fallback**. If you don't set SENDGRID_API_KEY, emails will be printed to the console instead of sent.

**What happens without SendGrid:**
- Password reset emails → Printed to logs (you'll see the reset link)
- Email verification → Printed to logs (you'll see the verification link)
- Everything else works normally!

**To skip**: Leave SENDGRID_API_KEY empty or commented out in .env

---

### If You Want Real Emails: Get SendGrid API Key

#### Step 1: Sign Up for SendGrid (Free)

1. Go to: https://signup.sendgrid.com/
2. Click "Create Account"
3. Fill in:
   - Email
   - Password
   - First/Last Name
   - Company: "Personal Project" or your name
   - Website: Can be anything (e.g., "localhost")
4. Click "Create Account"
5. **Verify your email** (check your inbox)

**Free Tier**: 100 emails/day forever (plenty for testing!)

#### Step 2: Create API Key

1. After login, go to: https://app.sendgrid.com/settings/api_keys
2. Click **"Create API Key"** (top right)
3. Give it a name: "Legally AI Development"
4. Choose **"Full Access"** (for simplicity)
5. Click **"Create & View"**
6. **COPY THE KEY NOW** - you won't see it again!

**Key looks like**:
```
SG.xxxxxxxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

#### Step 3: Verify Sender Email

Before SendGrid can send emails, you need to verify a sender:

1. Go to: https://app.sendgrid.com/settings/sender_auth/senders
2. Click **"Create New Sender"**
3. Fill in:
   - From Name: "Legally AI"
   - From Email: YOUR email address
   - Reply To: Same as From Email
   - Company: Your name
   - Address: Any address
4. Click **"Save"**
5. **Check your email** and click the verification link

Now SendGrid can send emails from this address!

---

## 3. GROQ_API_KEY (Required for Analysis)

Groq provides the AI model for contract analysis.

### Step 1: Sign Up for Groq

1. Go to: https://console.groq.com/
2. Click "Sign Up" or "Log In" (can use Google/GitHub)
3. Complete registration

**Free Tier**: Very generous - plenty for development!

### Step 2: Create API Key

1. After login, click on **"API Keys"** in left menu
2. Or go directly to: https://console.groq.com/keys
3. Click **"Create API Key"**
4. Give it a name: "Legally AI"
5. Click **"Create"**
6. **COPY THE KEY** - you won't see it again!

**Key looks like**:
```
gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 4. Setting Up Your .env File

Now let's put it all together!

### Step 1: Navigate to Backend Directory

```bash
cd /path/to/Legally_AI/backend
```

### Step 2: Copy Example File

```bash
cp .env.example .env
```

### Step 3: Edit .env File

Open the .env file in your favorite editor:

```bash
# macOS
nano .env

# Or use any text editor
code .env  # VS Code
open -a TextEdit .env  # TextEdit on macOS
```

### Step 4: Fill in the Keys

Replace the placeholder values:

```bash
# Database (auto-configured by Docker Compose - don't change)
DATABASE_URL=postgresql://legally_ai:password@postgres:5432/legally_ai
REDIS_URL=redis://redis:6379/0

# Security (REQUIRED - use your generated key)
SECRET_KEY=YOUR_SECRET_KEY_HERE_FROM_STEP_1

# LLM Provider (REQUIRED - use your Groq key)
LLM_PROVIDER=groq
GROQ_API_KEY=YOUR_GROQ_KEY_HERE_FROM_STEP_3

# Email (OPTIONAL - can skip for development)
SENDGRID_API_KEY=YOUR_SENDGRID_KEY_HERE_FROM_STEP_2
FROM_EMAIL=noreply@legally-ai.com

# Frontend URL (for email links)
FRONTEND_URL=http://localhost:3000

# Debug mode
DEBUG=True
```

### Example Filled In:

```bash
# Database
DATABASE_URL=postgresql://legally_ai:password@postgres:5432/legally_ai
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=Xp7k9mF2nL4vR8wQ1jH5tY3bN6gP0sA2cD4eF7hJ9k

# LLM Provider
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_abc123def456ghi789jkl012mno345pqr678stu901vwx234

# Email (optional - commented out for dev)
# SENDGRID_API_KEY=SG.your_key_here
FROM_EMAIL=noreply@legally-ai.com

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Debug
DEBUG=True
```

### Step 5: Save the File

- **nano**: Press `Ctrl+O`, then `Enter`, then `Ctrl+X`
- **VS Code**: `Cmd/Ctrl+S`
- **TextEdit**: `Cmd+S`

---

## 5. Verify Your Setup

Check that your .env file has the required keys:

```bash
# Check if SECRET_KEY is set
grep SECRET_KEY .env

# Check if GROQ_API_KEY is set
grep GROQ_API_KEY .env
```

You should see your keys (not the placeholder text).

---

## ✅ You're Ready!

Now you can start the application:

```bash
./quick-start.sh
```

---

## 🔒 Security Notes

### Keep Your Keys Secret!

- ❌ **NEVER** commit .env file to Git
- ❌ **NEVER** share your API keys publicly
- ❌ **NEVER** post keys in issues or forums
- ✅ The .env file is in .gitignore (safe)
- ✅ Generate new keys if you accidentally expose them

### Production vs Development

**Development** (.env):
```bash
DEBUG=True
FRONTEND_URL=http://localhost:3000
SENDGRID_API_KEY=  # Can be empty
```

**Production** (set via hosting platform):
```bash
DEBUG=False
FRONTEND_URL=https://your-domain.com
SENDGRID_API_KEY=SG.real_key_here  # Required
SECRET_KEY=super_long_random_string  # Different from dev
```

---

## 📝 Summary

### Required Keys:
1. ✅ **SECRET_KEY** - Generate with Python or OpenSSL
2. ✅ **GROQ_API_KEY** - Sign up at console.groq.com

### Optional Keys (for development):
3. ⚪ **SENDGRID_API_KEY** - Only needed for real emails

### What Happens Without SendGrid:
- Password reset links printed to console logs
- Email verification links printed to console logs
- You can still test all other features!

---

## ❓ Troubleshooting

### "Invalid SECRET_KEY"
- Make sure it's a long random string (32+ characters)
- No spaces or quotes around it in .env
- Regenerate with the Python command above

### "Groq API Error"
- Check your GROQ_API_KEY is correct
- Verify at: https://console.groq.com/keys
- Make sure you have credits/quota remaining

### "SendGrid Error" (if using)
- Verify your sender email at SendGrid
- Check API key has "Full Access" permissions
- Make sure you're not over the daily limit (100/day free)

### "Email not working" (if using SendGrid)
- Check Docker logs: `docker-compose logs backend`
- Verify FROM_EMAIL matches your verified sender
- Check SendGrid activity: https://app.sendgrid.com/activity

---

## 🎓 Understanding the Keys

**SECRET_KEY**:
- Used to sign JWT authentication tokens
- Must be the same across app restarts
- Keep it secret and secure
- Used by: Authentication system

**GROQ_API_KEY**:
- Connects to Groq's AI models
- Used for contract analysis
- Free tier is generous
- Used by: Analysis engine (Celery worker)

**SENDGRID_API_KEY**:
- Sends transactional emails
- 100 free emails/day
- Optional for development
- Used by: Password reset, email verification

---

**Need help?** Check the main guides:
- `QUICK_START_README.md` - Quick start
- `INTEGRATION_TESTING_GUIDE_BEGINNERS.md` - Full testing guide

**Ready to continue?** Run `./quick-start.sh` 🚀
