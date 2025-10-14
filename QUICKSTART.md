# Quick Start - Production Deployment

## 🚀 Fast Track Deployment

### On Deploy Server (192.168.1.175)

```bash
# 1. Run setup script
sudo bash server-setup.sh

# 2. Create environment file
cd /opt/booklib
sudo -u deploy vi .env.production
```

Add these values:

```bash
POSTGRES_PASSWORD=<generate-secure-password>
SECRET_KEY=<generate-with: python3 -c "import secrets; print(secrets.token_hex(32))">
JWT_SECRET_KEY=<generate-with: python3 -c "import secrets; print(secrets.token_hex(32))">
```

### On Jenkins Server (192.168.1.173)

```bash
# 1. Copy Jenkins SSH public key
sudo cat /var/lib/jenkins/.ssh/id_rsa.pub

# 2. Add key to deploy server
ssh deploy@192.168.1.175
echo "<paste-public-key>" >> ~/.ssh/authorized_keys

# 3. Test SSH connection
ssh deploy@192.168.1.175 "echo 'Connection successful'"
```

### In Jenkins UI

1. Manage Jenkins → Credentials → Add

   - Kind: SSH Username with private key
   - ID: `deploy-key`
   - Username: `deploy`
   - Private Key: Paste `/var/lib/jenkins/.ssh/id_rsa`

2. New Item → Pipeline

   - Name: `booklib-api-deploy`
   - Pipeline from SCM
   - Repository: Your Git repo
   - Script Path: `Jenkinsfile`

3. Click "Build Now"

### Verify Deployment

```bash
# Check health
curl http://192.168.1.175:5000/health

# Test graceful error handling
curl http://192.168.1.175:5000/books
```

## 🔥 Test Graceful Database Errors

```bash
# On deploy server
cd /opt/booklib

# Stop database
docker-compose stop postgres

# API should still respond (with 503)
curl http://localhost:5000/health
curl http://localhost:5000/books

# Restart database
docker-compose start postgres

# API should recover automatically
curl http://localhost:5000/health
```

## 📊 Monitoring

```bash
# View logs
docker-compose logs -f api

# Check status
docker-compose ps

# Restart if needed
docker-compose restart api
```

## ✅ Success Criteria

- [ ] Health endpoint returns database status
- [ ] API responds with 503 when DB is down (not crash)
- [ ] API automatically recovers when DB comes back
- [ ] Jenkins pipeline deploys successfully
- [ ] All containers are running

## 🆘 Quick Troubleshooting

**API won't start:**

```bash
docker-compose logs api
```

**Database connection errors:**

```bash
docker-compose restart postgres
```

**Jenkins can't connect:**

```bash
ssh deploy@192.168.1.175 "pwd"
```

**Port in use:**

```bash
sudo lsof -i :5000
sudo kill -9 $(sudo lsof -t -i:5000)
```
