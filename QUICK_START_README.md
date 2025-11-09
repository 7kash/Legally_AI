# Quick Start - Integration Testing

**New to Docker?** No problem! Follow these simple steps.

---

## 🚀 Super Quick Start (3 Steps)

### Step 1: Install Docker Desktop

Download and install Docker Desktop for your operating system:

**macOS**: https://docs.docker.com/desktop/install/mac-install/
**Windows**: https://docs.docker.com/desktop/install/windows-install/
**Linux**: https://docs.docker.com/desktop/install/linux-install/

After installation, **launch Docker Desktop** and wait for it to start (you'll see a whale icon).

---

### Step 2: Start the Application

Open a terminal and run:

```bash
cd /path/to/Legally_AI/backend
./quick-start.sh
```

**What happens**:
- ✅ Checks if Docker is installed
- ✅ Creates .env file if needed
- ✅ Starts all services (database, Redis, backend, Celery)
- ✅ Runs database migrations
- ✅ Shows you the API URL

**Time**: ~3-5 minutes (first run downloads Docker images)

---

### Step 3: Test It

Open your browser:

```
http://localhost:8000/docs
```

You'll see **interactive API documentation** where you can test all endpoints!

Or run automated tests:

```bash
cd /path/to/Legally_AI/backend
./test_integration.sh
```

**Done!** 🎉

---

## 📖 Full Documentation

For detailed instructions, troubleshooting, and advanced testing:

👉 **See**: `INTEGRATION_TESTING_GUIDE_BEGINNERS.md`

This guide explains:
- What Docker Compose does
- How to monitor logs
- How to test each feature
- Common problems and solutions
- Database and Redis commands

---

## 🎯 What Gets Tested

The integration tests cover:

✅ **Authentication**
- User registration
- Login/logout
- Password reset
- Email verification
- JWT token validation

✅ **Contract Management**
- File upload
- List contracts
- Get contract details
- Delete contracts

✅ **Analysis**
- Create analysis
- Real-time progress (SSE)
- Get results
- Export as PDF/DOCX
- Submit feedback

✅ **Account Management**
- Get account details
- Update profile
- GDPR data export
- Account deletion

✅ **Security**
- Authorization checks
- Free tier limits
- SQL injection prevention
- Invalid token handling

---

## ❓ Troubleshooting

### "Docker command not found"

**Solution**: Install Docker Desktop (see Step 1 above)

### "Port already in use"

**Solution**: Another service is using port 5432, 6379, or 8000

```bash
# Stop the services
docker-compose down

# Find what's using the port
lsof -i :5432  # macOS/Linux
netstat -ano | findstr :5432  # Windows

# Kill it or change ports in docker-compose.yml
```

### "Services won't start"

**Solution**: Check the logs

```bash
docker-compose logs backend
docker-compose logs postgres
```

### "Tests failing"

**Solution**: Make sure services are running

```bash
# Check if running
docker-compose ps

# Should show all services as "Up"

# Restart if needed
docker-compose restart
```

---

## 🛑 How to Stop

```bash
# Stop services (keeps data)
docker-compose down

# Stop and delete all data (fresh start)
docker-compose down -v
```

---

## 📝 Need More Help?

1. **Full Guide**: See `INTEGRATION_TESTING_GUIDE_BEGINNERS.md`
2. **Deployment**: See `TESTING_DEPLOYMENT_GUIDE.md`
3. **Testing Report**: See `COMPREHENSIVE_TESTING_REPORT.md`

---

**Questions?** The guides above have detailed troubleshooting sections!

**Happy Testing!** 🚀
