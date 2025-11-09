# 🚀 START HERE - Quick Commands

You have Docker 24.0.6 installed ✅

---

## 3 Commands to Get Running

### 1. Generate Your API Keys

```bash
cd backend
./setup-env.sh
```

This will:
- ✅ Auto-generate your SECRET_KEY
- ❓ Ask for your GROQ_API_KEY (get at https://console.groq.com/keys)
- ❓ Ask if you want SendGrid (optional - can skip)
- ✅ Create your .env file

**Takes 2 minutes!**

---

### 2. Start Everything

```bash
./quick-start.sh
```

This will:
- ✅ Check Docker is running
- ✅ Start PostgreSQL + Redis + Backend + Celery
- ✅ Run database migrations
- ✅ Show you the API URL

**Takes 3-5 minutes on first run**

---

### 3. Test It

Open browser: **http://localhost:8000/docs**

Or run automated tests:

```bash
./test_integration.sh
```

**Done!** 🎉

---

## What Each Key Does

**SECRET_KEY** (auto-generated)
- Signs JWT authentication tokens
- Keeps user sessions secure

**GROQ_API_KEY** (you need to get)
- Powers the AI contract analysis
- Get free key at: https://console.groq.com/keys
- Free tier is generous!

**SENDGRID_API_KEY** (optional)
- Sends password reset emails
- Sends email verification
- Can skip - emails print to console instead
- Get at: https://signup.sendgrid.com/

---

## Quick Reference

```bash
# Setup .env file (do once)
./setup-env.sh

# Start application
./quick-start.sh

# View logs
docker-compose logs -f

# Stop application
docker-compose down

# Run tests
./test_integration.sh

# Check status
docker-compose ps
```

---

## Detailed Guides

📖 **SETUP_API_KEYS.md** - Detailed key creation guide
📖 **QUICK_START_README.md** - Quick start overview
📖 **INTEGRATION_TESTING_GUIDE_BEGINNERS.md** - Full testing guide

---

## Help! Something's Wrong

**"Docker not running"**
```bash
# Make sure Docker Desktop is running
# You should see the whale icon
```

**"Port already in use"**
```bash
# Another PostgreSQL is running
# Stop it or change ports in docker-compose.yml
```

**"Can't generate SECRET_KEY"**
```bash
# Install Python or OpenSSL first
# Or use: https://generate-secret.vercel.app/32
```

**"Services won't start"**
```bash
# Check the logs
docker-compose logs backend
```

---

## You're All Set!

Just run these 3 commands:
1. `./setup-env.sh` - Create .env file
2. `./quick-start.sh` - Start application
3. Open http://localhost:8000/docs - Test it!

**Questions?** Check the detailed guides above.

**Ready?** Let's go! 🚀
