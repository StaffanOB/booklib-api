# BookLib API - Production Deployment Guide

## Overview

This guide covers deploying the BookLib API to a standalone server (192.168.1.175) using Jenkins CI/CD pipeline (192.168.1.173) with Docker containers and graceful database error handling.

## Features

- ✅ Standalone Docker deployment with PostgreSQL
- ✅ Graceful database error handling (API won't crash if DB is unavailable)
- ✅ Automated Jenkins CI/CD pipeline
- ✅ Health checks and automatic restarts
- ✅ Non-root container execution
- ✅ Production-ready configuration

## Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Jenkins Server │──────▶│  Deploy Server  │◀─────│   PostgreSQL    │
│  192.168.1.173  │      │  192.168.1.175  │      │   Container     │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                │
                                │
                         ┌──────▼──────┐
                         │  BookLib API │
                         │  Container   │
                         └─────────────┘
```

## Prerequisites

### On Deploy Server (192.168.1.175)

1. Docker and Docker Compose installed
2. Port 5000 available for API
3. Port 5432 available for PostgreSQL

### On Jenkins Server (192.168.1.173)

1. Jenkins installed and running
2. Docker installed
3. SSH credentials configured

## Setup Instructions

### Step 1: Prepare Deploy Server (192.168.1.175)

Run the setup script:

```bash
# Copy server-setup.sh to 192.168.1.175
scp server-setup.sh root@192.168.1.175:/tmp/

# SSH to server and run setup
ssh root@192.168.1.175
cd /tmp
chmod +x server-setup.sh
./server-setup.sh
```

### Step 2: Configure SSH Keys

On Jenkins server (192.168.1.173):

```bash
# Generate SSH key if not exists (as Jenkins user)
sudo -u jenkins ssh-keygen -t rsa -b 4096 -f /var/lib/jenkins/.ssh/id_rsa -N ""

# Copy public key to deploy server
sudo cat /var/lib/jenkins/.ssh/id_rsa.pub
```

On deploy server (192.168.1.175):

```bash
# Add Jenkins public key to deploy user
sudo -u deploy mkdir -p /home/deploy/.ssh
sudo -u deploy vi /home/deploy/.ssh/authorized_keys
# Paste the public key from Jenkins server

# Set correct permissions
sudo chmod 700 /home/deploy/.ssh
sudo chmod 600 /home/deploy/.ssh/authorized_keys
```

### Step 3: Configure Environment Variables

On deploy server (192.168.1.175):

```bash
cd /opt/booklib
sudo -u deploy cp .env.production.example .env.production
sudo -u deploy vi .env.production
```

Update with secure values:

```bash
POSTGRES_DB=booklib_prod
POSTGRES_USER=booklib_user
POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD_HERE
SECRET_KEY=YOUR_RANDOM_SECRET_KEY_HERE
JWT_SECRET_KEY=YOUR_RANDOM_JWT_SECRET_HERE
```

Generate secure keys:

```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# Generate JWT_SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Step 4: Configure Jenkins

1. **Add SSH Credentials in Jenkins:**

   - Go to: Jenkins → Manage Jenkins → Credentials
   - Add new SSH credential with ID: `deploy-key`
   - Username: `deploy`
   - Private Key: Paste Jenkins private key (`/var/lib/jenkins/.ssh/id_rsa`)

2. **Create Jenkins Pipeline:**
   - New Item → Pipeline
   - Name: `booklib-api-deploy`
   - Pipeline from SCM → Git
   - Repository URL: Your Git repository
   - Script Path: `Jenkinsfile`

### Step 5: Test Deployment

1. **Manual Test on Deploy Server:**

```bash
ssh deploy@192.168.1.175
cd /opt/booklib

# Build and start containers
docker-compose --env-file .env.production up -d

# Check container status
docker-compose ps

# Check logs
docker-compose logs -f api

# Test health endpoint
curl http://localhost:5000/health
```

Expected response:

```json
{
  "status": "healthy",
  "database": {
    "connected": true,
    "error": null
  },
  "timestamp": "2025-10-14T..."
}
```

2. **Trigger Jenkins Pipeline:**
   - Go to Jenkins dashboard
   - Click on `booklib-api-deploy` job
   - Click "Build Now"
   - Watch the pipeline stages execute

## Graceful Database Error Handling

The API now handles database unavailability gracefully:

### When Database is Unavailable:

```bash
# Response from any endpoint with DB dependency
curl http://192.168.1.175:5000/books
```

Response:

```json
{
  "error": "Database temporarily unavailable",
  "message": "The service is experiencing database connectivity issues. Please try again later.",
  "status": "service_degraded"
}
```

**HTTP Status: 503 Service Unavailable**

### Health Check with Database Down:

```bash
curl http://192.168.1.175:5000/health
```

Response:

```json
{
  "status": "degraded",
  "database": {
    "connected": false,
    "error": "connection refused..."
  },
  "timestamp": "2025-10-14T..."
}
```

### Benefits:

- ✅ API stays running even if database is down
- ✅ Returns meaningful error messages
- ✅ Automatic retry when database comes back
- ✅ Health endpoint shows database status

## Monitoring and Maintenance

### Check Application Status

```bash
# On deploy server
docker-compose ps
docker-compose logs -f api
```

### Check Database Status

```bash
docker-compose exec postgres psql -U booklib_user -d booklib_prod -c '\dt'
```

### Restart Services

```bash
# Restart API only
docker-compose restart api

# Restart all services
docker-compose restart

# Full restart (recreate containers)
docker-compose down && docker-compose up -d
```

### View Logs

```bash
# API logs
docker-compose logs -f api

# Database logs
docker-compose logs -f postgres

# All logs
docker-compose logs -f
```

### Database Backup

```bash
# Backup database
docker-compose exec postgres pg_dump -U booklib_user booklib_prod > backup_$(date +%Y%m%d).sql

# Restore database
docker-compose exec -T postgres psql -U booklib_user booklib_prod < backup_20251014.sql
```

## Troubleshooting

### Issue: API container keeps restarting

```bash
# Check logs
docker-compose logs api

# Check if database is accessible
docker-compose exec api ping postgres

# Verify environment variables
docker-compose exec api env | grep DATABASE_URL
```

### Issue: Database connection refused

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### Issue: Jenkins deployment fails

```bash
# Test SSH connection from Jenkins server
ssh -i /var/lib/jenkins/.ssh/id_rsa deploy@192.168.1.175

# Check Jenkins logs
# Jenkins → Build History → Console Output
```

### Issue: Port already in use

```bash
# Check what's using port 5000
sudo lsof -i :5000

# Or kill the process
sudo kill -9 $(sudo lsof -t -i:5000)
```

## Security Best Practices

1. **Change Default Passwords:**

   - Update all passwords in `.env.production`
   - Use strong, randomly generated passwords

2. **Firewall Configuration:**

```bash
# Allow only necessary ports
sudo ufw allow 5000/tcp  # API
sudo ufw enable
```

3. **Regular Updates:**

```bash
# Update Docker images
docker-compose pull
docker-compose up -d
```

4. **SSL/TLS (Recommended):**
   - Use nginx reverse proxy with Let's Encrypt
   - Or use a load balancer with SSL termination

## API Endpoints

Once deployed, API is available at: `http://192.168.1.175:5000`

### Key Endpoints:

- `GET /health` - Health check with database status
- `GET /books` - List all books
- `POST /users/register` - Register new user
- `POST /users/login` - User login
- `POST /books` - Add new book (requires JWT)

See full API documentation: `http://192.168.1.175:5000/swagger`

## Rollback Procedure

If deployment fails:

1. **Check previous image:**

```bash
docker images booklib-api
```

2. **Rollback to previous version:**

```bash
docker tag booklib-api:previous booklib-api:latest
docker-compose up -d
```

3. **Or use specific version:**

```bash
# Edit docker-compose.yml
image: booklib-api:123  # Use specific build number

docker-compose up -d
```

## Support

For issues or questions:

- Check logs: `docker-compose logs -f`
- Health check: `curl http://localhost:5000/health`
- Review Jenkins pipeline console output
