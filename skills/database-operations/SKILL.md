# Database Operations Skill

Connect to PostgreSQL, explore schemas, run queries, and manage migrations.

## Trigger

Activated when the user needs to inspect the database, debug data issues, explore the schema, or run migrations.

## Connecting to Local PostgreSQL

### Via Docker

```bash
docker compose exec postgres psql -U app -d app
```

### Direct Connection

```bash
psql postgresql://app:app@localhost:5432/app
```

### Connection Details (from env.example)

| Parameter | Value |
|-----------|-------|
| Host | localhost |
| Port | 5432 |
| Database | app |
| User | app |
| Password | app |

## Schema Exploration

### List All Tables

```sql
\dt
-- or
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public' ORDER BY table_name;
```

### Describe a Table

```sql
\d table_name
-- or for full details including constraints
\d+ table_name
```

### List All Columns for a Table

```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'your_table'
ORDER BY ordinal_position;
```

### List Foreign Keys

```sql
SELECT
    tc.table_name, kcu.column_name,
    ccu.table_name AS foreign_table,
    ccu.column_name AS foreign_column
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';
```

### List Indexes

```sql
SELECT indexname, indexdef FROM pg_indexes
WHERE schemaname = 'public' ORDER BY tablename, indexname;
```

## Common Queries

### Count Rows

```sql
SELECT count(*) FROM table_name;
```

### Recent Records

```sql
SELECT * FROM table_name ORDER BY created_at DESC LIMIT 10;
```

### Find by ID

```sql
SELECT * FROM table_name WHERE id = 'uuid-here';
```

### Check for Orphaned Records

```sql
SELECT c.id FROM child_table c
LEFT JOIN parent_table p ON c.parent_id = p.id
WHERE p.id IS NULL;
```

## Migration Commands

### Check Current State

```bash
alembic current
```

### Apply All Pending Migrations

```bash
alembic upgrade head
```

### Create a New Migration

```bash
alembic revision --autogenerate -m "add phone column to users"
```

### Rollback One Migration

```bash
alembic downgrade -1
```

### Check for Multiple Heads

```bash
alembic heads
```

If multiple heads exist, merge them:
```bash
alembic merge heads -m "merge migration heads"
```

### View Migration History

```bash
alembic history --verbose
```

## Safety Rules

- **Never run destructive queries on production** without explicit user confirmation
- **Always use transactions** for multi-statement operations: `BEGIN; ... COMMIT;` (or `ROLLBACK;`)
- **Back up before bulk updates**: `CREATE TABLE backup_table AS SELECT * FROM table_name;`
- **Use LIMIT** when exploring unfamiliar tables to avoid dumping millions of rows
- **Check row count first** before UPDATE/DELETE: `SELECT count(*) FROM ... WHERE ...`

## Debugging Data Issues

### Check if a Record Exists

```sql
SELECT exists(SELECT 1 FROM table_name WHERE id = 'uuid');
```

### Find Records Modified Recently

```sql
SELECT * FROM table_name
WHERE updated_at > now() - interval '1 hour'
ORDER BY updated_at DESC;
```

### Check Soft-Deleted Records

```sql
-- Records that are soft-deleted
SELECT * FROM table_name WHERE deleted_at IS NOT NULL;

-- Records that are active
SELECT * FROM table_name WHERE deleted_at IS NULL;
```

### View Active Database Connections

```sql
SELECT pid, usename, application_name, state, query_start, query
FROM pg_stat_activity
WHERE datname = 'app';
```
