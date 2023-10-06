# pytest is a testing framework for Python that allows you to easily create small, simple tests
import pytest

# Here we're importing the get_db_conn function from the db module in the backend.db package
from backend.db.db import create_links_table, get_db_conn

# The pytest.mark.asyncio decorator is used to mark a test function as a coroutine
# It tells pytest to handle this function asynchronously


@pytest.mark.asyncio
# This is the test function for get_db_conn
async def test_get_db_conn():
    # We're using the async with statement to handle the context manager returned by get_db_conn
    # The async with statement is used for context management in asynchronous code
    async with get_db_conn() as conn:
        # Here we're asserting that conn is not None
        # If get_db_conn is working correctly, it should return a connection object, which is not None
        # If conn is None, then the assert statement will fail, and pytest will know that our test has failed
        assert conn is not None
