# 🗄️ PostgreSQL Database Setup with Supabase

Supabase provides a free PostgreSQL database hosted on the cloud. Perfect for production!

## 🚀 Quick Start (5 minutes)

### Step 1: Create Supabase Project
1. Go to https://supabase.com
2. Sign up with GitHub
3. Create new project (free tier available)
4. Wait for database setup (~2 minutes)

### Step 2: Get Connection Credentials
In Supabase dashboard:
1. Go to **Settings → API**
2. Copy **Project URL** → `SUPABASE_URL`
3. Copy **anon public key** → `SUPABASE_KEY`

### Step 3: Create Database Tables

Go to **SQL Editor** and run:

```sql
-- Logs table
CREATE TABLE logs (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  message TEXT NOT NULL,
  level VARCHAR(20) DEFAULT 'INFO',
  source VARCHAR(100),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster searches
CREATE INDEX idx_logs_timestamp ON logs(timestamp DESC);
CREATE INDEX idx_logs_level ON logs(level);
CREATE INDEX idx_logs_message ON logs USING GIN(to_tsvector('english', message));

-- Alerts table
CREATE TABLE alerts (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  title VARCHAR(255) NOT NULL,
  message TEXT,
  severity VARCHAR(20) DEFAULT 'INFO',
  resolved BOOLEAN DEFAULT FALSE,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  resolved_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for active alerts
CREATE INDEX idx_alerts_resolved ON alerts(resolved);
CREATE INDEX idx_alerts_timestamp ON alerts(timestamp DESC);

-- Metrics table
CREATE TABLE metrics (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name VARCHAR(100) NOT NULL,
  value FLOAT NOT NULL,
  tags JSONB,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for metrics
CREATE INDEX idx_metrics_name ON metrics(name);
CREATE INDEX idx_metrics_timestamp ON metrics(timestamp DESC);

-- Enable Row Level Security (optional, for multi-user)
ALTER TABLE logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE metrics ENABLE ROW LEVEL SECURITY;

-- Create policy to allow public read/write (for demo)
CREATE POLICY "Enable read for all" ON logs FOR SELECT USING (true);
CREATE POLICY "Enable write for all" ON logs FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable read for all" ON alerts FOR SELECT USING (true);
CREATE POLICY "Enable write for all" ON alerts FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable read for all" ON metrics FOR SELECT USING (true);
CREATE POLICY "Enable write for all" ON metrics FOR INSERT WITH CHECK (true);
```

### Step 4: Set Environment Variables

In Vercel dashboard, add:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

Or locally in `.env.local`:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### Step 5: Test Connection

```bash
# Test API with database
curl "https://your-app.vercel.app/logs/stats"
```

Response should show real database counts!

## 📊 Database Schema

### Logs Table
```
id              BIGINT (Primary Key)
message         TEXT
level           VARCHAR(20)  - ERROR, WARN, INFO, DEBUG
source          VARCHAR(100) - Where log came from
timestamp       TIMESTAMP    - When log occurred
created_at      TIMESTAMP    - When inserted
```

### Alerts Table
```
id              BIGINT (Primary Key)
title           VARCHAR(255)
message         TEXT
severity        VARCHAR(20)  - CRITICAL, WARNING, INFO
resolved        BOOLEAN
timestamp       TIMESTAMP
resolved_at     TIMESTAMP
created_at      TIMESTAMP
```

### Metrics Table
```
id              BIGINT (Primary Key)
name            VARCHAR(100) - Metric name (cpu, memory, etc)
value           FLOAT        - Metric value
tags            JSONB        - Custom metadata
timestamp       TIMESTAMP
created_at      TIMESTAMP
```

## 🔧 Advanced Configuration

### Row Level Security (Multi-user)

```sql
-- Create role for authenticated users
CREATE ROLE authenticated;

-- Allow authenticated users to see only their own logs
CREATE POLICY "Users see own logs" ON logs
  FOR SELECT USING (auth.uid() = user_id);

-- Allow users to insert their own logs
CREATE POLICY "Users insert own logs" ON logs
  FOR INSERT WITH CHECK (auth.uid() = user_id);
```

### Backup & Recovery

Supabase includes:
- ✅ Automatic daily backups
- ✅ 30-day backup history
- ✅ One-click restore
- ✅ Point-in-time recovery

Go to **Settings → Backups** to manage.

### Performance Tuning

```sql
-- Analyze table for query planning
ANALYZE logs;

-- View query plans
EXPLAIN ANALYZE SELECT * FROM logs WHERE level = 'ERROR';

-- Vacuum for cleanup
VACUUM ANALYZE logs;
```

## 📈 Monitoring & Analytics

Supabase includes:
- **Table statistics** - Size, row count
- **Query performance** - Slow queries
- **Realtime stats** - Live connections
- **Disk usage** - Storage monitor

View in **Dashboard → Inspect**

## 🔐 Security Best Practices

### 1. Never commit credentials
```bash
# .gitignore
.env
.env.local
.env.*.local
```

### 2. Use Read-only keys for frontend
- Create a **read-only key** for dashboard
- Keep **write key** only on backend

### 3. Enforce Row Level Security
```sql
ALTER TABLE logs ENABLE ROW LEVEL SECURITY;
```

### 4. Set data retention policies
```sql
-- Delete logs older than 30 days
DELETE FROM logs WHERE created_at < NOW() - INTERVAL '30 days';
```

## 💾 Data Retention Policy

```sql
-- Archive old logs to storage
CREATE TABLE logs_archive AS
  SELECT * FROM logs
  WHERE created_at < NOW() - INTERVAL '90 days';

DELETE FROM logs
  WHERE created_at < NOW() - INTERVAL '90 days';
```

## 🚀 Scaling Strategies

| Size | Solution |
|------|----------|
| < 1 GB | Supabase Free |
| 1-10 GB | Supabase Pro ($25/mo) |
| > 10 GB | Self-hosted PostgreSQL |

### Optimize for large datasets:

```sql
-- Partition by date
CREATE TABLE logs_2025_12 PARTITION OF logs
  FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');

-- Archive older partitions
ALTER TABLE logs_2025_01 SET TABLESPACE archive_space;
```

## 📱 Access Database UI

Supabase provides web UI at:
```
https://app.supabase.com/project/your-project-id
```

Features:
- 🔍 Browse/edit tables
- 💾 SQL editor
- 📊 View statistics
- 🔄 Sync operations
- 🔐 Manage permissions

## 🧪 Test Data

```sql
-- Insert test logs
INSERT INTO logs (message, level, source) VALUES
  ('Application started', 'INFO', 'system'),
  ('High memory usage detected', 'WARN', 'monitor'),
  ('Database connection failed', 'ERROR', 'database');

-- Insert test alerts
INSERT INTO alerts (title, message, severity) VALUES
  ('CPU Alert', 'CPU usage > 80%', 'CRITICAL'),
  ('Memory Warning', 'Memory usage > 75%', 'WARNING');

-- View data
SELECT * FROM logs ORDER BY timestamp DESC LIMIT 10;
SELECT * FROM alerts WHERE resolved = FALSE;
```

## 📞 Support & Resources

- Supabase Docs: https://supabase.com/docs
- PostgreSQL Docs: https://www.postgresql.org/docs
- Query Optimization: https://www.postgresql.org/docs/current/sql-explain.html

## ✅ Checklist

- [ ] Supabase account created
- [ ] Project set up
- [ ] Tables created
- [ ] Credentials saved in `.env.example`
- [ ] Vercel environment variables set
- [ ] Test connection successful
- [ ] Data appearing in dashboard
- [ ] Backups enabled

---

**Database ready!** 🎉 Your API now persists data forever.
