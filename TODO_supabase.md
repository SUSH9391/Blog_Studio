# Supabase Integration TODO

## Plan Steps (Approved)

1. [x] Create this TODO_supabase.md to track progress
2. [x] Install dependencies: psycopg2-binary==2.9.11, python-dotenv (added via uv)
3. Update .env with Supabase credentials (user=postgres, password=[YOUR-PASSWORD] → replace, host/port/dbname)
4. [x] Update config.py: Add env fields (db_user/db_password/db_host/db_port/db_name), construct database_url as postgresql+asyncpg://... if not set
5. [x] Update database.py: Add sync_engine creation using psycopg2 for tests/migrations
6. [x] Update main.py: Add sync connection code + test at module level (with logging.info/error)
7. Test connection: Run main.py or test script
8. Run Alembic migrations: alembic upgrade head
9. Start app: uvicorn main:app --reload
10. [Optional] Install Supabase agent skills: npx skills add supabase/agent-skills
11. Migrate any local data if needed
12. Verify endpoints/DB operations with Supabase

**Next Step:** #7 - Test connection: `uv run python main.py`
3. [ ] User: Add to .env (required for connection):
```
user=postgres
password=YOUR_SUPABASE_PASSWORD (from Supabase dashboard)
host=db.fdeeliegupqyseuqpbxi.supabase.co
port=5432
dbname=postgres
```
10. [ ] Optional: `npx skills add supabase/agent-skills`


