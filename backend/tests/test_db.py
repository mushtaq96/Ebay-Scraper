# pytest is a testing framework for Python that allows you to easily create small, simple tests
import pytest

# Here we're importing the get_db_conn function from the db module in the backend.db package
from backend.db.db import create_links_table, get_db_conn, insert_links

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


@pytest.mark.asyncio
async def test_create_links_table():
    async with get_db_conn() as conn:
        # We call the create_links_table function and pass the connection to it
        await create_links_table(conn)
        # After creating the table, we try to fetch from it to see if it exists
        result = await conn.fetch('SELECT * FROM links')
        # If the table doesn't exist, an error will be thrown and the test will fail
        assert result is not None


@pytest.mark.asyncio
async def test_insert_links():
    url = 'https://www.example.com'
    async with get_db_conn() as conn:
        # We call the insert_links function and pass the connection and a URL to it
        await insert_links(conn, url)
        # After inserting the link, we fetch from the table where URL is the one we inserted
        result = await conn.fetch('SELECT * FROM links WHERE url = $1', url)
        # If the URL doesn't exist in the table, then our insert_links function didn't work correctly and the test will fail
        assert len(result) > 0
