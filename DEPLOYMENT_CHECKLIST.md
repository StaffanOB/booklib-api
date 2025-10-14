# Deployment Checklist ✅

Use this checklist to ensure a smooth deployment to production.

## Prerequisites

### Deploy Server (192.168.1.175)

- [ ] Docker 20.10+ installed
- [ ] Docker Compose 2.0+ installed
- [ ] Ports 5000 and 5432 available
- [ ] Root or sudo access available

### Jenkins Server (192.168.1.173)

- [ ] Jenkins running and accessible
- [ ] Docker installed on Jenkins server
- [ ] Git repository accessible

## Step 1: Prepare Deploy Server

- [ ] Copy server-setup.sh to deploy server

  ```bash
  scp server-setup.sh root@192.168.1.175:/tmp/
  ```

- [ ] Run setup script on deploy server

  ```bash
  ssh root@192.168.1.175 "bash /tmp/server-setup.sh"
  ```

- [ ] Verify deploy user created

  ```bash
  ssh root@192.168.1.175 "id deploy"
  ```

- [ ] Verify directory created
  ```bash
  ssh root@192.168.1.175 "ls -la /opt/booklib"
  ```

## Step 2: Configure SSH Access

- [ ] Generate SSH key on Jenkins server (if needed)

  ```bash
  ssh jenkins@192.168.1.173
  sudo -u jenkins ssh-keygen -t rsa -b 4096 -N ""
  ```

- [ ] Copy Jenkins public key

  ```bash
  sudo cat /var/lib/jenkins/.ssh/id_rsa.pub
  ```

- [ ] Add Jenkins public key to deploy server

  ```bash
  ssh deploy@192.168.1.175
  mkdir -p ~/.ssh
  chmod 700 ~/.ssh
  vi ~/.ssh/authorized_keys  # Paste public key
  chmod 600 ~/.ssh/authorized_keys
  ```

- [ ] Test SSH connection from Jenkins
  ```bash
  ssh deploy@192.168.1.175 "echo 'Connection successful'"
  ```

## Step 3: Configure Production Environment

- [ ] SSH to deploy server

  ```bash
  ssh deploy@192.168.1.175
  ```

- [ ] Navigate to deployment directory

  ```bash
  cd /opt/booklib
  ```

- [ ] Copy environment template

  ```bash
  cp .env.production.example .env.production
  ```

- [ ] Generate secure keys

  ```bash
  # Generate SECRET_KEY
  python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"

  # Generate JWT_SECRET_KEY
  python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"

  # Generate database password
  python3 -c "import secrets; print('POSTGRES_PASSWORD=' + secrets.token_urlsafe(32))"
  ```

- [ ] Edit .env.production with generated values

  ```bash
  vi .env.production
  ```

- [ ] Verify environment file
  ```bash
  cat .env.production
  ```

## Step 4: Configure Jenkins

- [ ] Login to Jenkins web interface

- [ ] Add SSH credentials

  - Navigate to: Manage Jenkins → Credentials
  - Click: Add Credentials
  - Kind: SSH Username with private key
  - ID: `deploy-key`
  - Username: `deploy`
  - Private Key: Paste content of `/var/lib/jenkins/.ssh/id_rsa`
  - Click: OK

- [ ] Create new Pipeline job

  - Click: New Item
  - Name: `booklib-api-deploy`
  - Type: Pipeline
  - Click: OK

- [ ] Configure Pipeline
  - Pipeline section:
    - Definition: Pipeline script from SCM
    - SCM: Git
    - Repository URL: `<your-git-repo-url>`
    - Credentials: `<your-git-credentials>`
    - Branch: `*/main`
    - Script Path: `Jenkinsfile`
  - Click: Save

## Step 5: Deploy

- [ ] Trigger first deployment

  - Click: Build Now

- [ ] Monitor build console output

  - Click on build number
  - Click: Console Output
  - Watch for errors

- [ ] Wait for all stages to complete
  - [ ] Checkout
  - [ ] Run Tests
  - [ ] Build Docker Image
  - [ ] Save Docker Image
  - [ ] Deploy to Server
  - [ ] Health Check

## Step 6: Verify Deployment

- [ ] Check health endpoint

  ```bash
  curl http://192.168.1.175:5000/health
  ```

  Expected response:

  ```json
  {
    "status": "healthy",
    "database": {
      "connected": true,
      "error": null
    }
  }
  ```

- [ ] Test books endpoint

  ```bash
  curl http://192.168.1.175:5000/books
  ```

  Expected: `[]` or list of books

- [ ] Check containers are running

  ```bash
  ssh deploy@192.168.1.175 "cd /opt/booklib && docker-compose ps"
  ```

  Expected: Both `postgres` and `api` containers running

- [ ] Check container logs
  ```bash
  ssh deploy@192.168.1.175 "cd /opt/booklib && docker-compose logs --tail=50 api"
  ```

## Step 7: Test Graceful Error Handling

- [ ] Stop PostgreSQL database

  ```bash
  ssh deploy@192.168.1.175 "cd /opt/booklib && docker-compose stop postgres"
  ```

- [ ] Test API still responds (should return 503)

  ```bash
  curl http://192.168.1.175:5000/books
  ```

  Expected response (503):

  ```json
  {
    "error": "Database temporarily unavailable",
    "message": "The service is experiencing database connectivity issues...",
    "status": "service_degraded"
  }
  ```

- [ ] Start PostgreSQL database

  ```bash
  ssh deploy@192.168.1.175 "cd /opt/booklib && docker-compose start postgres"
  ```

- [ ] Verify API recovers automatically

  ```bash
  curl http://192.168.1.175:5000/books
  ```

  Expected: Normal response (200 OK)

- [ ] Check health status shows database connected
  ```bash
  curl http://192.168.1.175:5000/health
  ```

## Step 8: Register Test User

- [ ] Register a new user

  ```bash
  curl -X POST http://192.168.1.175:5000/users/register \
    -H "Content-Type: application/json" \
    -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'
  ```

- [ ] Login with test user

  ```bash
  curl -X POST http://192.168.1.175:5000/users/login \
    -H "Content-Type: application/json" \
    -d '{"username":"testuser","password":"testpass123"}'
  ```

  Expected: JWT token in response

## Post-Deployment Checklist

- [ ] Document production credentials in secure location
- [ ] Setup monitoring alerts (optional)
- [ ] Configure firewall rules (optional)
- [ ] Setup SSL/TLS certificate (recommended)
- [ ] Configure database backups
- [ ] Test rollback procedure
- [ ] Document any custom configurations

## Troubleshooting

If deployment fails, check:

1. **SSH Connection Issues**

   ```bash
   ssh -v deploy@192.168.1.175
   ```

2. **Container Issues**

   ```bash
   ssh deploy@192.168.1.175 "cd /opt/booklib && docker-compose logs"
   ```

3. **Port Conflicts**

   ```bash
   ssh deploy@192.168.1.175 "sudo lsof -i :5000 && sudo lsof -i :5432"
   ```

4. **Environment Variables**
   ```bash
   ssh deploy@192.168.1.175 "cd /opt/booklib && cat .env.production"
   ```

## Success Criteria

✅ All items should be checked:

- [ ] Jenkins pipeline completes successfully
- [ ] Health endpoint returns "healthy" status
- [ ] Database shows "connected": true
- [ ] API returns 200 for /books endpoint
- [ ] API returns 503 (not crash) when DB is stopped
- [ ] API recovers automatically when DB starts
- [ ] Both containers running and healthy
- [ ] Test user can register and login

## 🎉 Deployment Complete!

Once all items are checked, your BookLib API is successfully deployed and production-ready!

## Next Steps

- Review logs regularly: `docker-compose logs -f`
- Monitor health endpoint: `curl http://192.168.1.175:5000/health`
- Setup automated backups for PostgreSQL
- Consider adding SSL/TLS with nginx reverse proxy
- Configure monitoring tools (Prometheus, Grafana, etc.)

---

**Questions or issues?** Check the documentation:

- README_DEPLOYMENT.md - Main guide
- DEPLOYMENT.md - Detailed manual
- QUICKSTART.md - Quick reference
