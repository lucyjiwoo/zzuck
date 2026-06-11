# Tests temporarily disabled — requires a running PostgreSQL instance.
# Re-enable once test DB setup is in place.

# from sqlalchemy import text
# from app.db.session import engine
#
#
# def test_database_connection():
#     with engine.connect() as conn:
#         result = conn.execute(text("SELECT 1")).scalar()
#     assert result == 1
#
#
# def test_database_is_postgres():
#     with engine.connect() as conn:
#         result = conn.execute(text("SELECT version()")).scalar()
#     assert "PostgreSQL" in result
