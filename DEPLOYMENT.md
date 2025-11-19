# JobHack Deployment Guide

This guide covers deploying JobHack to production environments.

## Table of Contents

1. [Deployment Options](#deployment-options)
2. [Vercel + Railway (Recommended)](#vercel--railway)
3. [Docker Deployment](#docker-deployment)
4. [AWS Deployment](#aws-deployment)
5. [Environment Variables](#environment-variables)
6. [Post-Deployment](#post-deployment)

---

## Deployment Options

### Recommended Stack

- **Frontend**: Vercel (Next.js optimized)
- **Backend**: Railway or Render
- **Database**: Supabase or AWS RDS
- **Storage**: AWS S3 or Supabase Storage
- **Redis**: Upstash or Redis Cloud

---

## Vercel + Railway

### 1. Deploy Frontend to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd frontend
vercel

# Follow prompts to:
# - Link to Vercel project
# - Set environment variables
# - Deploy to production
```

**Environment Variables for Vercel:**

```env
NEXT_PUBLIC_APP_URL=https://your-domain.com
NEXT_PUBLIC_API_URL=https://your-api.railway.app
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_xxx
CLERK_SECRET_KEY=sk_live_xxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
```

### 2. Deploy Backend to Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Initialize project
cd backend
railway init

# Add PostgreSQL
railway add

# Deploy
railway up
```

**Environment Variables for Railway:**

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_ORIGINS=https://your-domain.com
ANTHROPIC_API_KEY=sk-ant-xxx
SENDGRID_API_KEY=SG.xxx
STRIPE_SECRET_KEY=sk_live_xxx
```

### 3. Configure Custom Domain

**Vercel:**
1. Go to project settings
2. Add custom domain
3. Update DNS records

**Railway:**
1. Go to service settings
2. Generate domain or add custom domain
3. Update NEXT_PUBLIC_API_URL in Vercel

---

## Docker Deployment

### 1. Build Images

```bash
# Build all services
docker-compose build

# Or build individually
docker build -t jobhack-frontend ./frontend
docker build -t jobhack-backend ./backend
```

### 2. Deploy with Docker Compose

```bash
# Production compose file
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend

  frontend:
    image: jobhack-frontend
    environment:
      NEXT_PUBLIC_API_URL: https://api.your-domain.com
    depends_on:
      - backend

  backend:
    image: jobhack-backend
    environment:
      DATABASE_URL: postgresql://user:pass@postgres:5432/db
      ENVIRONMENT: production
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

```bash
# Start production stack
docker-compose -f docker-compose.prod.yml up -d
```

### 3. SSL Configuration (Let's Encrypt)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d api.your-domain.com

# Auto-renewal is configured automatically
```

---

## AWS Deployment

### Architecture

```
Route 53 (DNS)
    ↓
CloudFront (CDN)
    ↓
S3 (Frontend Static Files)

API Gateway or ALB
    ↓
ECS Fargate (Backend)
    ↓
RDS PostgreSQL + ElastiCache Redis
```

### 1. Frontend to S3 + CloudFront

```bash
# Build frontend
cd frontend
npm run build
npm run export

# Upload to S3
aws s3 sync out/ s3://your-bucket-name --delete

# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name your-bucket.s3.amazonaws.com \
  --default-root-object index.html
```

### 2. Backend to ECS Fargate

```bash
# Build and push to ECR
aws ecr create-repository --repository-name jobhack-backend

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t jobhack-backend ./backend
docker tag jobhack-backend:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/jobhack-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/jobhack-backend:latest

# Create ECS task definition and service
# (Use AWS Console or CloudFormation)
```

### 3. Database (RDS)

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier jobhack-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password <password> \
  --allocated-storage 20
```

---

## Environment Variables

### Production Checklist

- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Configure production database URL
- [ ] Add production domain to `ALLOWED_ORIGINS`
- [ ] Use production API keys (Stripe, AI services, etc.)
- [ ] Configure error tracking (Sentry)
- [ ] Set up monitoring and logging
- [ ] Enable rate limiting
- [ ] Configure backup strategies

---

## Post-Deployment

### 1. Database Migrations

```bash
# Run migrations on production database
python manage.py migrate

# Or via Railway/Render CLI
railway run python manage.py migrate
```

### 2. Health Checks

```bash
# Test backend
curl https://api.your-domain.com/health

# Test frontend
curl https://your-domain.com

# Check database connection
psql $DATABASE_URL -c "SELECT 1"
```

### 3. Monitoring

**Setup Sentry:**

```env
SENTRY_DSN=https://xxx@sentry.io/xxx
```

**Setup PostHog:**

```env
NEXT_PUBLIC_POSTHOG_KEY=phc_xxx
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com
```

### 4. Backups

**Database Backups:**

```bash
# Setup automated backups (Railway/RDS handle this)
# Or manual backup:
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

**File Storage Backups:**

```bash
# S3 versioning
aws s3api put-bucket-versioning \
  --bucket your-bucket \
  --versioning-configuration Status=Enabled
```

### 5. Performance Optimization

1. **Enable Caching**
   - Redis for API responses
   - CloudFront for static assets

2. **Database Optimization**
   - Add indexes on frequently queried fields
   - Enable connection pooling

3. **Image Optimization**
   - Use Next.js Image component
   - Compress uploads

4. **Code Splitting**
   - Already handled by Next.js
   - Lazy load heavy components

### 6. Security Hardening

1. **SSL/TLS**: Enforce HTTPS
2. **CORS**: Restrict to known domains
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Sanitize all inputs
5. **Secrets Management**: Use environment variables, never commit secrets

---

## Scaling Considerations

### Horizontal Scaling

- Use load balancer (ALB/nginx)
- Run multiple backend instances
- Session management via Redis

### Database Scaling

- Read replicas for queries
- Connection pooling
- Indexing optimization

### Cost Optimization

**Free Tiers:**
- Vercel: Free for hobby projects
- Railway: $5/month credit
- Supabase: Free tier (500MB database)

**Production:**
- Vercel Pro: $20/month
- Railway: Pay per usage (~$20-50/month)
- Supabase Pro: $25/month

---

## Troubleshooting

### Common Issues

**Issue: CORS errors**
```env
# Add all production domains to ALLOWED_ORIGINS
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

**Issue: Database connection timeout**
```env
# Increase connection pool
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40
```

**Issue: File upload fails**
```env
# Increase max file size
MAX_UPLOAD_SIZE=10485760  # 10MB
```

---

## Rollback Strategy

```bash
# Vercel: Instant rollback to previous deployment
vercel rollback

# Railway: Rollback via dashboard or CLI
railway rollback

# Docker: Deploy previous image
docker-compose up -d frontend:previous-tag
```

---

**Successfully deployed? Don't forget to:**
- [ ] Update DNS records
- [ ] Configure monitoring
- [ ] Set up alerts
- [ ] Document custom configurations
- [ ] Train team on deployment process

**Good luck with your deployment! 🚀**
