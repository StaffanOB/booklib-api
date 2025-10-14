# Standalone API Deployment

## Overview

The BookLib API is configured as a **standalone service** that connects to an **external PostgreSQL database**. The database is managed separately (from another repository).

## Architecture

```
┌─────────────────────┐
│  Jenkins Server     │
│  192.168.1.173      │
└──────────┬──────────┘
           │ Deploy
           ▼
┌─────────────────────┐      ┌─────────────────────┐
│  API Server         │──────▶│  PostgreSQL Server  │
│  192.168.1.175      │      │  (External)         │
├─────────────────────┤      │  Managed separately │
│  ┌───────────────┐  │      └─────────────────────┘
│  │  BookLib API  │  │
│  │  Container    │  │
│  │  Port: 5000   │  │
│  └───────────────┘  │
└─────────────────────┘
```

## Configuration

### docker-compose.yml
- **Single service**: API only
- **No database**: Removed PostgreSQL service
- **External connection**: Uses DATABASE_URL environment variable

### .env.production
Create this file on the deploy server with:

```bash
# External PostgreSQL connection
DATABASE_URL=postgresql://username:password@db-host:port/database

# Example
DATABASE_URL=postgresql://booklib_user:mypassword@192.168.1.200:5432/booklib_prod

# Application secrets
SECRET_KEY=your-generated-secret-key
JWT_SECRET_KEY=your-generated-jwt-secret
```

## Prerequisites

### Database Requirements
1. PostgreSQL database must exist
2. Tables must be created (from your database repo)
3. Database must be accessible from 192.168.1.175
4. PostgreSQL configured to accept remote connections

### Network Requirements
- API server (192.168.1.175) can reach database server
- Port 5432 open between servers (or custom PostgreSQL port)
- Firewall rules configured

## Deployment Steps

### 1. Prepare Database
```bash
# Ensure database exists and tables are created
# This is done from your separate database repository
```

### 2. Test Database Connection
```bash
# From API server, test connection to database
psql -h your-db-host -U booklib_user -d booklib_prod -c "SELECT 1;"
```

### 3. Configure Environment
```bash
ssh deploy@192.168.1.175
cd /opt/booklib
cp .env.production.example .env.production

# Edit with correct DATABASE_URL
vi .env.production
```

### 4. Deploy
```bash
# Via Jenkins pipeline
# Or manually:
docker-compose up -d
```

### 5. Verify
```bash
# Check health endpoint
curl http://192.168.1.175:5000/health

# Expected response (if DB accessible):
{
  "status": "healthy",
  "database": {
    "connected": true,
    "error": null
  }
}
```

## Graceful Error Handling

Even with external database, the API handles connection issues gracefully:

### Scenario 1: Database Temporarily Unavailable
```bash
# API request when DB is down
curl http://192.168.1.175:5000/books

# Response: 503 Service Unavailable
{
  "error": "Database temporarily unavailable",
  "message": "The service is experiencing database connectivity issues...",
  "status": "service_degraded"
}
```

**✅ API continues running** - doesn't crash!

### Scenario 2: Database Recovers
```bash
# Once database is back online
curl http://192.168.1.175:5000/books

# Response: 200 OK
[]  # or list of books
```

**✅ Automatic recovery** - no restart needed!

## Troubleshooting

### API Can't Connect to Database

**Check 1: Network connectivity**
```bash
docker exec booklib-api ping your-db-host
```

**Check 2: PostgreSQL is listening**
```bash
# On database server
sudo netstat -tulpn | grep 5432
```

**Check 3: PostgreSQL allows remote connections**
```bash
# On database server, check postgresql.conf
listen_addresses = '*'  # or specific IP

# Check pg_hba.conf
host    booklib_prod    booklib_user    192.168.1.175/32    md5
```

**Check 4: Firewall rules**
```bash
# On database server
sudo ufw allow from 192.168.1.175 to any port 5432
```

**Check 5: Environment variable**
```bash
# Verify DATABASE_URL is correct
docker exec booklib-api env | grep DATABASE_URL
```

### Check API Logs
```bash
docker-compose logs -f api
```

### Check Health Status
```bash
curl http://192.168.1.175:5000/health
```

## Benefits of Standalone API

✅ **Separation of Concerns**
- API and database managed independently
- Different teams can manage each component
- Database can be shared across services

✅ **Flexible Deployment**
- API can be redeployed without affecting database
- Database can be upgraded independently
- Easier to scale API horizontally

✅ **Graceful Degradation**
- API remains operational during DB maintenance
- Returns meaningful errors instead of crashing
- Automatic recovery when DB returns

✅ **Simplified API Container**
- Smaller container (no database)
- Faster deployment
- Less resource usage

## Jenkins Pipeline

The Jenkinsfile automatically:
1. ✅ Runs tests
2. ✅ Builds Docker image
3. ✅ Deploys to 192.168.1.175
4. ✅ Verifies health endpoint
5. ✅ No database initialization (managed externally)

## Security Considerations

1. **Database Credentials**: Store in .env.production (not in repo)
2. **Network Security**: Use firewall rules to restrict database access
3. **SSL/TLS**: Consider using SSL for database connections
4. **Secrets Management**: Use environment variables, not hardcoded values

## Monitoring

### Health Check
```bash
# Regular health monitoring
curl http://192.168.1.175:5000/health

# Monitor database connectivity
watch -n 5 'curl -s http://192.168.1.175:5000/health | jq .database'
```

### Logs
```bash
# API logs
docker-compose logs -f api

# Look for database connection errors
docker-compose logs api | grep -i database
```

## Summary

Your BookLib API is now configured to:
- ✅ Run as standalone Docker container
- ✅ Connect to external PostgreSQL database
- ✅ Handle database errors gracefully (no crashes)
- ✅ Auto-recover when database returns
- ✅ Deploy via Jenkins CI/CD pipeline

**Next Step**: Configure DATABASE_URL and deploy!
