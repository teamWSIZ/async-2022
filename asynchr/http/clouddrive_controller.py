import os.path
from asyncio import sleep, create_task

from aiofile import async_open
from aiohttp import web

# from asynchr.db.db_config import DB_PASS, DB_HOST
# from asynchr.db.db_service import DbService
from utils import log, task_name, ts

"""
https://docs.aiohttp.org/en/stable/web_quickstart.html#

#http://localhost/user/{user_id}/badge/{pythonista}/add

query = req.match_info.get('query', '')  # for route-resolving, /{query}    
query = req.rel_url.query['query']  # params; required; else .get('query','default')
"""


def format_report(q_values):
    q_values = [q * 1000 for q in q_values]
    s = f'[{q_values[0]:.3f}'
    for v in q_values:
        s += ',' + f'{v:.3f}'
    s += '] (ms)'
    return s


def get_percentiles(delays: list[float], quantiles: list[float]):
    delays.sort()
    n = len(delays)
    q_values = [delays[int(n * q)] for q in quantiles]
    # for (q, v) in zip(quantiles, q_values):
    #     print(f'p[{q:.3f}]={v:.5f}')
    return q_values


async def report_from_watcher(delays: list[float]):
    n = len(delays)
    log(f'watcher report - delays on ticks every 10ms {n=:4d}: {format_report(get_percentiles(delays, [0.01, 0.05, 0.5, 0.95, 0.99]))}')


async def watcher():
    """
    Engine supporting continuous monitoring of the event loop of the application.

    """
    log(f'watcher started on task: {task_name()}')
    start = ts()
    previous = start
    delays = []
    while True:
        await sleep(0.01)
        delay = ts() - previous
        previous = ts()
        delays.append(delay - 0.01)
        if ts() - start > 1:
            await report_from_watcher(delays)
            delays = []
            start = ts()


# ----------------
routes = web.RouteTableDef()


# db = DbService(DB_HOST, DB_PASS) # rough way to create services


@routes.get('/')
async def hello(request):
    return web.json_response({'comment': 'OK'})


@routes.get('/welcome')
async def welcome(request):
    if not 'user' in request.rel_url.query:
        return web.json_response({'comment': 'missing `user` parameter'}, status=400)
    user = request.rel_url.query.get('user')  # returns str

    return web.json_response({'comment': f'Welcome {user}!'})


# @routes.get('/users')
# async def fetch_users(request):
#     offset = int(request.rel_url.query.get('offset', default='0'))
#     limit = int(request.rel_url.query.get('b', default='500'))
#     users = await db.get_users(offset, limit)
#     users_d = [u.__dict__ for u in users]
#     return web.json_response(users_d)


@routes.get('/images')
async def serve_a_file(request):
    log('serving a file')
    return web.FileResponse('images/hills.zip')


@routes.post('/images')
async def accept_file(request):
    """
    Main goal of the application -- support for efficient upload.

    :param request:
    :return:
    """
    # https://docs.aiohttp.org/en/stable/web_quickstart.html#file-uploads
    reader = await request.multipart()  # first one is field.name = 'files'
    field = await reader.next()
    if field.name == 'files':
        field = await reader.next()  # these are the actual files in many cases

    # async for field in (await request.multipart()):   #check all parts
    #     print(f'{field.name}')

    filename = field.filename
    # log(f'filename:{filename}')
    # filename = 'images/' + filename
    filename = 'saved.bin'
    # filename = os.path.join('/home/wrong/ramdrive/', filename)
    size = 0

    # with open(filename, 'wb') as f:   # blocking
    async with async_open(filename, 'wb') as f:  # aiofile
        while True:
            chunk = await field.read_chunk(size=8192 * 1)  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            await f.write(chunk)  # aiofile
            # f.write(chunk)    # blocking

    return web.json_response({'name': filename, 'size': size})


app = web.Application(client_max_size=100 * 2 ** 20)
app.add_routes(routes)


async def app_factory():
    """
    Function run at the startup of the application. If some async initialization is needed - put it in here.
    :return:
    """
    await sleep(0.01)
    # await db.initialize()
    create_task(watcher())
    return app


web.run_app(app_factory(), port=4001)
