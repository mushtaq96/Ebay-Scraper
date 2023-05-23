from contextlib import asynccontextmanager
import asyncpg

@asynccontextmanager
async def get_db_conn():
    # conn = await asyncpg.connect('postgresql://postgres:mushtaq96@db/ebay')
    conn = await asyncpg.connect('postgresql://postgres:mushtaq96@192.168.1.150:5432/ebay')#<windows_host_ip>:5432
    #db is the name of the container or host
    try:
        yield conn
        #yield is like return but it returns a generator
    finally:
        await conn.close()
        #closes the connection to the database
        
async def create_links_table(conn):
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL
        );
    ''')

async def get_links(conn):
    result = await conn.fetch('SELECT * FROM links')
    return result

async def insert_links(conn, url):
    await conn.execute('INSERT INTO links (url) VALUES ($1)', url)
    #inserts the url into the database
    
async def link_exists(conn, url):
    result = await conn.fetch('SELECT * FROM links WHERE url = $1', url)
    return len(result) > 0
    #checks if the url exists in the database

