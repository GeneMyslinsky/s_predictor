import faust, json
import pickle
import asyncpg,asyncio
loop = asyncio.get_event_loop()
async def init_app():
    pool = await asyncpg.create_pool('postgres://postgresql:FoolishPassword@postgres:5432/data')
    print('sec')
    return pool
pool = loop.run_until_complete(init_app())

app = faust.App('tester',key_serializer='raw',value_serializer='raw',broker='kafka://broker:29092')
topic = app.topic('tester', value_type=bytes)

@app.agent(topic)
async def processor(stream):
    async for e in stream.events():
    # async for payload in stream:
        print(e.key.decode('UTF-8'))
        print(e.message.timestamp)
        data = json.loads(e.value)
        print(data)

async def checkTable():
    async with pool.acquire() as con:
        r = await con.fetchval(f"""
                            SELECT EXISTS (
                            SELECT FROM pg_catalog.pg_class c
                            JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                            WHERE  n.nspname = 'data'
                            AND    c.relname = '{contract}_{candles}'
                            AND    c.relkind = 'r'    -- only tables
                            );""")
        print(r)
async def createTable():
    cur.execute("""CREATE TEMP TABLE codelist(id INTEGER, z INTEGER) ON COMMIT DROP""")

    cur.execute("""
        UPDATE table_name
        SET z = codelist.z
        FROM codelist
        WHERE codelist.id = vehicle.id;
        """)
async def createTempTable():
    cur.execute("""CREATE TEMP TABLE codelist(id INTEGER, z INTEGER) ON COMMIT DROP""")
    cur.executemany("""INSERT INTO codelist (id, z) VALUES(%s, %s)""", rows)

    cur.execute("""
        UPDATE table_name
        SET z = codelist.z
        FROM codelist
        WHERE codelist.id = vehicle.id;
        """)


# tuples = [tuple(x) for x in df.values]
# s = await conn.copy_records_to_table(table_name, records=tuples, columns=list(df.columns), timeout=10)

#faust -A f_store_hist worker -l info --web-port 6066