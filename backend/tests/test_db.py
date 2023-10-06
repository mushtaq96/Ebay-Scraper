import pytest
from backend.db.db import get_db_conn


@pytest.mark.asyncio
async def test_get_db_conn():
    async with get_db_conn() as conn:
        assert conn is not None
