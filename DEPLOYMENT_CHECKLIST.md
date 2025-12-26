# 📋 Deployment Checklist

Use this checklist to track your deployment progress. Check off items as you complete them.

## Phase 1: Preparation (5 min)

### Accounts & Tools
- [ ] GitHub account with your repo cloned
- [ ] Vercel account (vercel.com)
- [ ] Railway.app account (railway.app) 
- [ ] Supabase account (supabase.com)
- [ ] Git installed on your machine
- [ ] Terminal/Command prompt ready

### Repository
- [ ] Git repository initialized
- [ ] All code committed locally
- [ ] Ready to push to GitHub

## Phase 2: API Deployment to Vercel (5 min)

### Deploy
- [ ] Open terminal in project root
- [ ] Run: `npm i -g vercel` (if not installed)
- [ ] Run: `vercel` and follow prompts
- [ ] Project auto-detects as FastAPI
- [ ] Deployment completes successfully
- [ ] Note the deployment URL (e.g., https://your-app.vercel.app)

### Verify API
- [ ] Visit https://your-app.vercel.app in browser
- [ ] Dashboard page loads
- [ ] Status shows "Disconnected" (expected, no DB yet)
- [ ] /docs endpoint works at https://your-app.vercel.app/docs
- [ ] /health endpoint responds

## Phase 3: Database Setup (5 min)

### Create Supabase Project
- [ ] Go to supabase.com
- [ ] Click "New Project"
- [ ] Create project in nearest region
- [ ] Wait for database creation (1-2 min)
- [ ] Database is now running

### Get Credentials
- [ ] Click "Project Settings" → "API"
- [ ] Copy "Project URL" (starts with https://xxxxx.supabase.co)
- [ ] Copy "anon public" API key
- [ ] Save both securely (will use in next step)

### Create Database Schema
- [ ] Go to "SQL Editor"
- [ ] Copy schema from SUPABASE_SETUP.md (starting with CREATE TABLE)
- [ ] Paste into SQL editor
- [ ] Click "Run"
- [ ] All tables created successfully
- [ ] Check "Tables" tab shows: logs, alerts, metrics

## Phase 4: Connect Database to API (3 min)

### Vercel Environment Variables
- [ ] Go to vercel.com dashboard
- [ ] Select your project
- [ ] Settings → Environment Variables
- [ ] Add variable:
  - Name: `SUPABASE_URL`
  - Value: (paste from Phase 3)
- [ ] Add variable:
  - Name: `SUPABASE_KEY`
  - Value: (paste from Phase 3)
- [ ] Save variables

### Redeploy API
- [ ] Run: `vercel --prod` in project root
- [ ] Wait for deployment to complete
- [ ] Visit API URL again
- [ ] Status should now show "Connected" ✓

### Test Database Connection
- [ ] Go to https://your-app.vercel.app/docs
- [ ] Try POST /logs/ingest with test data
- [ ] Response shows successful insert
- [ ] Log appears in dashboard
- [ ] Verify in Supabase console

## Phase 5: Deploy Log Watcher Agent (3 min)

### Railway Setup
- [ ] Go to railway.app
- [ ] Click "New Project"
- [ ] Select "GitHub Repo"
- [ ] Authorize GitHub (if first time)
- [ ] Select your distributed-log-analytics repo
- [ ] Select "Deploy Now"
- [ ] Wait for initial deployment

### Configure Log Watcher
- [ ] Click "Variables" tab
- [ ] Add environment variables:
  - `API_URL`: https://your-app.vercel.app
  - `LOG_FILE`: /var/log/syslog
  - `POLL_INTERVAL`: 10
  - `BATCH_SIZE`: 100
- [ ] Save variables

### Set Start Command
- [ ] Click "Settings"
- [ ] Find "Start Command"
- [ ] Replace with: `python agent/log_watcher_enhanced.py`
- [ ] Save and redeploy
- [ ] Check logs section for "Starting Log Watcher" message
- [ ] No errors in logs

### Verify Running
- [ ] Status shows "Running" (green)
- [ ] Dashboard shows logs appearing
- [ ] Timestamps are current

## Phase 6: Deploy Metrics Collector Agent (3 min)

### Create New Railway Project
- [ ] Go to railway.app
- [ ] Click "New Project"
- [ ] Select your GitHub repo again
- [ ] This creates separate metrics-collector project
- [ ] Wait for deployment

### Configure Metrics Collector
- [ ] Add environment variables:
  - `API_URL`: https://your-app.vercel.app
  - `POLL_INTERVAL`: 30
- [ ] Set start command: `python agent/metrics_collector_enhanced.py`
- [ ] Verify running and no errors

### Verify Metrics
- [ ] Dashboard shows metrics appearing
- [ ] CPU, Memory, Disk metrics visible
- [ ] Values update every 30 seconds

## Phase 7: Deploy Anomaly Detector Agent (3 min)

### Create New Railway Project
- [ ] Go to railway.app
- [ ] Click "New Project"
- [ ] Select your GitHub repo
- [ ] Create anomaly-detector project
- [ ] Wait for deployment

### Configure Anomaly Detector
- [ ] Add environment variables:
  - `API_URL`: https://your-app.vercel.app
  - `POLL_INTERVAL`: 60
  - `ANOMALY_THRESHOLD`: 5
- [ ] Set start command: `python agent/anomaly_detector_enhanced.py`
- [ ] Verify running and no errors

### Verify Alerts
- [ ] Anomaly detector starts checking
- [ ] Alerts appear in dashboard
- [ ] Check /alerts endpoint returns data

## Phase 8: Verification (5 min)

### Full System Test
- [ ] [ ] Visit dashboard: https://your-app.vercel.app
- [ ] Status badge shows "Connected ✓"
- [ ] At least 5 logs visible
- [ ] At least 1 metric visible
- [ ] At least 1 alert visible
- [ ] All timestamps are current

### API Testing
- [ ] Test /health endpoint (should return 200)
- [ ] Test /logs endpoint (returns JSON)
- [ ] Test /metrics endpoint (returns JSON)
- [ ] Test /alerts endpoint (returns JSON)
- [ ] Test POST /logs/ingest (inserts and returns ID)

### Agent Status
- [ ] Log Watcher shows "Running" in Railway
- [ ] Metrics Collector shows "Running"
- [ ] Anomaly Detector shows "Running"
- [ ] All agents have recent logs (within last minute)
- [ ] No error messages in logs

### Database Status
- [ ] Supabase shows active connections
- [ ] Tables have data (check with SELECT * FROM logs)
- [ ] Data is being inserted in real-time

## Phase 9: Production Setup (10 min)

### Enable Auto-Deploy
- [ ] Railway: Each project has Auto-Deploy enabled
- [ ] Vercel: Already enabled for main branch
- [ ] Push to GitHub updates all services

### Set Up Monitoring
- [ ] [ ] Enable Vercel notifications (email on deployment)
- [ ] [ ] Configure Railway alerts
- [ ] [ ] Set up error tracking (optional: Sentry)
- [ ] [ ] Monitor Supabase backups

### Configure Backups
- [ ] [ ] Supabase: Enable daily backups
- [ ] [ ] Supabase: Set backup retention to 30 days
- [ ] [ ] Create backup of Supabase credentials

### Security
- [ ] [ ] Regenerate Supabase API keys
- [ ] [ ] Store credentials securely (LastPass/1Password)
- [ ] [ ] Enable 2FA on Vercel account
- [ ] [ ] Enable 2FA on Railway account
- [ ] [ ] Enable 2FA on Supabase account

## Phase 10: Documentation & Handoff (5 min)

### Create Documentation
- [ ] [ ] Write down API URL
- [ ] [ ] Write down Supabase URL
- [ ] [ ] Document dashboard login (if added later)
- [ ] [ ] Create runbooks for common issues
- [ ] [ ] Store credentials in secure location

### Team Handoff
- [ ] [ ] Share dashboard URL with team
- [ ] [ ] Explain how to add new logs
- [ ] [ ] Explain how to configure alerts
- [ ] [ ] Share contact for troubleshooting
- [ ] [ ] Schedule follow-up meeting

### Performance Baseline
- [ ] [ ] Record API response times
- [ ] [ ] Note log ingestion rate
- [ ] [ ] Note database growth rate
- [ ] [ ] Monitor for first week

## Phase 11: Ongoing Maintenance

### Daily Checks (5 min)
- [ ] All agents show "Running" status
- [ ] No errors in logs
- [ ] Dashboard loads without errors
- [ ] Data is flowing (recent timestamps)

### Weekly Checks (15 min)
- [ ] Review Vercel analytics
- [ ] Review Railway metrics
- [ ] Check Supabase storage usage
- [ ] Verify backups are being created
- [ ] Test restore from backup

### Monthly Checks (30 min)
- [ ] Review performance metrics
- [ ] Plan for scaling if needed
- [ ] Security audit
- [ ] Upgrade dependencies
- [ ] Update documentation

## Troubleshooting Quick Reference

### If dashboard shows "Disconnected"
```
1. Check API URL in browser console (F12 → Network)
2. Verify Vercel deployment is active: vercel --list
3. Test API manually: curl https://your-app.vercel.app/health
4. Check CORS headers are present
5. Redeploy if needed: vercel --prod
```

### If no logs appearing
```
1. Check Log Watcher is running: railway logs --project=log-watcher
2. Verify API_URL is correct in environment variables
3. Test ingestion manually: curl -X POST with test data
4. Check /logs endpoint has data
5. Review Railway logs for errors
```

### If database not working
```
1. Verify SUPABASE_URL and SUPABASE_KEY in Vercel
2. Test database connection in Vercel logs
3. Check Supabase project is active (check project settings)
4. Verify tables exist: SELECT * FROM information_schema.tables
5. Check network access (may need allowlisting)
```

### If agents disconnecting
```
1. Check Railway service logs for network errors
2. Verify API is reachable: curl from agent
3. Increase timeout values
4. Check if API is rate-limiting requests
5. Restart agent from Railway dashboard
```

## Final Sign-Off

- [ ] All phases completed
- [ ] All verification tests passed
- [ ] Team trained on system
- [ ] Documentation created
- [ ] Monitoring configured
- [ ] Backups tested

**Deployment Date:** _______________

**Deployed By:** _______________

**Verified By:** _______________

**Notes:**
```
[Space for deployment notes]
```

---

## 🎉 Deployment Complete!

Your distributed log analytics platform is now in production. 

**Key Resources:**
- Dashboard: https://your-app.vercel.app
- API Docs: https://your-app.vercel.app/docs
- Vercel Dashboard: vercel.com/dashboard
- Railway Dashboard: railway.app
- Supabase Console: app.supabase.com

**Next Steps:**
1. Monitor for the next 24 hours
2. Gather feedback from team
3. Make optimizations based on usage patterns
4. Plan for scaling if needed
5. Implement additional features

**Support:**
- API logs: Vercel dashboard → Logs
- Agent logs: Railway → Deployments → Logs
- Database logs: Supabase → Database → Logs

Good luck! 🚀
