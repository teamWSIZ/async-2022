from asyncio import sleep, create_task
from datetime import datetime

from aiohttp import web

from asynchr.db.db_config import DB_PASS, DB_HOST
from asynchr.db.db_service import DbService
from asynchr.db.model import User
from asynchr.http.some_service import Service
from asynchr.utils import log, task_name, ts

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
    s += ']'
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
    log(f'watcher report {n=:4d}: {format_report(get_percentiles(delays, [0.01, 0.05, 0.5, 0.95, 0.99]))}')


async def watcher():
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
service = Service()
db = DbService(DB_HOST, DB_PASS)


@routes.get('/')
async def hello(request):
    await service.my_exciting_async_job(11)
    return web.json_response({'comment': 'OK'})


@routes.get('/welcome')
async def welcome(request):
    if not 'user' in request.rel_url.query:
        return web.json_response({'comment': 'missing `user` parameter'}, status=400)
    user = request.rel_url.query.get('user')  # returns str

    return web.json_response({'comment': f'Welcome {user}!'})


@routes.get('/add')
async def addition(request):
    # przykład http://localhost:4001/add?a=10&b=12
    # wynik: {"result": 22}
    a = float(request.rel_url.query.get('a', default='0'))
    b = float(request.rel_url.query.get('b', default='0'))
    result = a + b
    return web.json_response({'result': result})


@routes.get('/compute')
async def computation(request):
    # support dla "add", "subtract", "multiply", "divide", "power"; a,b mogą być float-ami
    # przykład http://localhost:4001/add?a=10&b=4?operation=divide
    # wynik: {"result": 2.5}
    return web.json_response({'result': f'...fill_me...'})


@routes.get('/square')
async def square(request):
    # call: http://0.0.0.0:4000/square?x=12
    sx: str = request.rel_url.query['x']
    x = int(sx)
    xx = x ** 2
    return web.json_response({'result': xx})


@routes.get('/users')
async def fetch_users(request):
    offset = int(request.rel_url.query.get('offset', default='0'))
    limit = int(request.rel_url.query.get('b', default='500'))
    users = await db.get_users(offset, limit)
    users_d = [u.__dict__ for u in users]
    return web.json_response(users_d)


@routes.post('/users')
async def new_user(request):
    log('creating a user')
    user_dict = await request.json()
    user = User(**user_dict)

    user_inserted = await db.upsert(user)

    log(f'new user: {user_inserted}')

    return web.json_response(user_inserted.__dict__)


@routes.get('/images')
async def serve_a_file(request):
    log('serving a file')
    return web.FileResponse('images/hills.zip')


@routes.post('/images')
async def accept_file(request):
    # https://docs.aiohttp.org/en/stable/web_quickstart.html#file-uploads
    log('file upload request')
    reader = await request.multipart()

    field = await reader.next()
    assert field.name == 'file'
    filename = field.filename
    log(f'filename:{filename}')
    filename = 'images/' + filename
    size = 0
    with open(filename, 'wb') as f:
        file_as_bytes = b''
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            # file_as_bytes += chunk
            f.write(chunk)
        # f.write(file_as_bytes)

    return web.json_response({'name': filename, 'size': size})


app = web.Application(client_max_size=100 * 2 ** 20)
app.add_routes(routes)


async def app_factory():
    """
    Function run at the startup of the application. If some async initialization is needed - put it in here.
    :return:
    """
    await sleep(0.01)
    await service.initialize()
    await db.initialize()
    create_task(watcher())
    return app


web.run_app(app_factory(), port=4001)
