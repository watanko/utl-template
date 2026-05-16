# migrations

Alembic migration scripts live here.

```sh
cd backend
uv run alembic revision --autogenerate -m "create example"
uv run alembic upgrade head
```
