# Supabase PostgreSQL Migration
Status: In Progress

1. [ ] Get full Supabase URL (with password)
2. [ ] Install deps: asyncpg alembic
3. [ ] Update config.py (database_url)
4. [ ] Update database.py (engine from settings)
5. [ ] Init alembic/
6. [ ] alembic revision --autogenerate
7. [ ] alembic upgrade head
8. [ ] Update populate_db.py for async
9. [ ] Test server + password reset

Notes:
- Current: SQLite blog.db
- Target: Supabase postgres://...

