#faust -A f_getlive worker -l info --web-port 6067
import faust, json
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
