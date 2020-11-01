import faust, json
import pickle
import asyncpg,asyncio
loop = asyncio.get_event_loop()
async def init_app():
    pool = await asyncpg.create_pool('postgres://postgresql:FoolishPassword@postgres:5432/data')
    print('sec')
    return pool
pool = loop.run_until_complete(init_app())

async def checkTable(contract,candles):
    async with pool.acquire() as con:
        r = await con.fetchval(f"""
                            SELECT EXISTS (
                            SELECT FROM pg_catalog.pg_class c
                            JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                            WHERE  n.nspname = 'data'
                            AND    c.relname = '{contract}_{candles}'
                            AND    c.relkind = 'r'    -- only tables
                            );""")
        
        c = "TABLE EXISTS"
        print(r)
        if r == False:
            c = await con.execute(f"""
                        CREATE TABLE IF NOT EXISTS "data".{contract}_{candles} (
                        "date" timestamptz(0) NOT NULL,
                        "open" float8 NULL,
                        high float8 NULL,
                        low float8 NULL,
                        "close" float8 NULL,
                        volume int4 NULL,
                        average float8 NULL,
                        barcount int4 NULL,
                        CONSTRAINT {contract}_{candles}_pk PRIMARY KEY (date)
                        );
                    """)
        
        return c
async def createTemp(contract,candles,values):
    async with pool.acquire() as con:
        await con.execute(f"""
                            CREATE TEMP TABLE _{contract}_{candles} (
                            "date" varchar(25) NOT NULL,
                            "open" float8 NULL,
                            high float8 NULL,
                            low float8 NULL,
                            "close" float8 NULL,
                            volume int4 NULL,
                            average float8 NULL,
                            barcount int4 NULL
                            )
                        """)
        await con.copy_records_to_table(f"_{contract}_{candles}", records=values)
        await con.execute(f"""
                                INSERT INTO "data".{contract}_{candles}("date", "open", high, low, "close", volume, average, barcount)
                                SELECT cast("date" as timestamp)::timestamp at time zone 'America/Toronto' , "open", high, low, "close", volume, average, barcount FROM _{contract}_{candles}
                                ON CONFLICT ("date")
                                DO UPDATE SET 
                                    "open"=EXCLUDED."open",
                                     high=EXCLUDED.high, 
                                     low=EXCLUDED.low, 
                                     "close"=EXCLUDED."close", 
                                     volume=EXCLUDED.volume, 
                                     average=EXCLUDED.average, 
                                     barcount=EXCLUDED.barcount
                                     ;
                            """)
        await con.execute(f"""
                            DROP TABLE IF EXISTS _{contract}_{candles}
                                 ;
                        """)
        print("SUCCESSFUL INSERT")
        return 1
app = faust.App('tester',key_serializer='raw',value_serializer='raw',broker='kafka://broker:29092')
topic = app.topic('tester', value_type=bytes)

@app.agent(topic)
async def processor(stream):
    async for e in stream.events():
    # async for payload in stream:
        key = json.loads(e.key)
        contract,params = key['contract']['symbol'].lower(),key['params']['candles'].replace(" ", "")
        # print(e.message.timestamp)
        data = pickle.loads(e.value)
        data.index = data.index.astype(str)
        data = list(data.to_records())
        await checkTable(contract,params)
        await createTemp(contract,params,data)






# tuples = [tuple(x) for x in df.values]
# s = await conn.copy_records_to_table(table_name, records=tuples, columns=list(df.columns), timeout=10)

#faust -A f_store_hist worker -l info --web-port 6066