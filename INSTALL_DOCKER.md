# ⚠️ DOCKER NOT INSTALLED

Docker is required to run this system. Here's how to install it:

## 🪟 Windows Installation

### Option 1: Docker Desktop (Recommended)

**Download & Install:**
1. Go to: https://www.docker.com/products/docker-desktop
2. Click "Download for Windows"
3. Run the installer
4. Follow the installation wizard
5. **Restart your computer when prompted**
6. Verify installation:
   ```powershell
   docker --version
   docker compose version
   ```

**System Requirements:**
- Windows 10 or later
- 4GB RAM minimum (8GB recommended)
- WSL 2 enabled (installer handles this)

**Installation Time:** 5-10 minutes

---

### Option 2: Docker via Chocolatey (Fast)

If you have Chocolatey installed:

```powershell
# Run PowerShell as Administrator
choco install docker-desktop -y
```

**Then restart your computer.**

---

### Option 3: Docker via WSL 2 (Advanced)

For advanced users who want CLI-only Docker:

```powershell
# Run PowerShell as Administrator
wsl --install
wsl --install -d Ubuntu
```

Then install Docker in WSL:
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
```

---

## ✅ Verify Installation

After restarting, run:

```powershell
# Check Docker version
docker --version

# Should output: Docker version 24.x.x or later

# Check Docker Compose
docker compose version

# Should output: Docker Compose version 2.x.x or later

# Test Docker daemon
docker run hello-world

# Should output: "Hello from Docker!"
```

---

## 🚨 Troubleshooting Installation

### PowerShell Says "docker: The term not recognized"

**Solution 1:** Restart PowerShell
```powershell
# Close all PowerShell windows
# Open a new PowerShell window
docker --version
```

**Solution 2:** Add Docker to PATH
```powershell
# Run as Administrator
$env:Path += ";C:\Program Files\Docker\Docker\resources\bin"
docker --version
```

**Solution 3:** Restart Computer
```powershell
# If still not working
Restart-Computer
# After restart, try again
docker --version
```

### Error: "Docker daemon is not running"

**Solution:**
1. Open "Docker Desktop" application
2. Wait for it to start (watch the taskbar icon)
3. When you see "Docker Desktop is running", try again:
   ```powershell
   docker run hello-world
   ```

### Error: "WSL 2 installation incomplete"

**Solution:**
1. Install WSL 2:
   ```powershell
   # Run as Administrator
   wsl --install
   ```
2. Restart computer
3. Open Docker Desktop again

---

## 📋 Quick Checklist

Before running the system, verify:

- [ ] Docker is installed: `docker --version`
- [ ] Docker Compose works: `docker compose version`
- [ ] Docker daemon is running: `docker ps`
- [ ] You're in the project folder: `cd "D:\Desktop\Assignment"`

---

## 🎯 Once Docker is Installed

Run these commands:

```powershell
# 1. Start all services
docker compose up -d

# 2. Wait 60 seconds
Start-Sleep -Seconds 60

# 3. Download the LLM model
docker exec ollama ollama pull mistral

# 4. Check health
docker compose ps

# 5. Access the system
Start-Process http://localhost:8000/docs
```

---

## 📞 Need Help?

- **Docker Installation Issues:** https://docs.docker.com/desktop/install/windows-install/
- **Docker Compose Issues:** https://docs.docker.com/compose/install/
- **WSL 2 Setup:** https://docs.microsoft.com/windows/wsl/install

---

## ⏱️ Expected Timeline

1. **Download Docker Desktop:** 2-3 minutes (500MB)
2. **Run Installer:** 5 minutes
3. **Restart Computer:** 2-3 minutes
4. **Verify Installation:** 1 minute
5. **Run System:** 1-2 minutes

**Total: ~15-20 minutes**

---

## 🚀 Ready to Continue?

Once Docker is installed and working:

1. Verify: `docker --version`
2. Run: `docker compose up -d`
3. Access: http://localhost:8000/docs

---

**Status:** ⏳ Waiting for Docker installation
**Next Step:** Install Docker Desktop, then run `docker compose up -d`

Last Updated: January 19, 2026
