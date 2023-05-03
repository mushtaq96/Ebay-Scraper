import asyncpg

async def create_table():
    conn = await asyncpg.connect(user='yourusername', password='yourpassword',
                                 database='yourdatabase', host='yourhost')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS search_results (
            id serial PRIMARY KEY,
            query text NOT NULL,
            link text NOT NULL
        )
    ''')
    await conn.close()

async def insert_data(query, link):
    conn = await asyncpg.connect(user='yourusername', password='yourpassword',
                                 database='yourdatabase', host='yourhost')
    await conn.execute('''
        INSERT INTO search_results(query, link) VALUES($1, $2)
    ''', query, link)
    await conn.close()
