from asyncio import run, create_task, gather

import aiofiles
import aiohttp

from asynchr.http.some_model import SimpleResult


async def call_server():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:4001') as resp:
            print(resp.status)
            res_json = await resp.json()
            print(type(res_json))
            print(res_json)


async def test_add_endpoint(a, b, expected_result, expected_status=200):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:4001/add?a={a}&b={b}') as resp:
            assert resp.status == expected_status
            res_json = await resp.json()
            assert res_json['result'] == expected_result


async def test_call_auth():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://auth.wsi.edu.pl/status') as resp:
            res_dict = await resp.json()
            res = SimpleResult(**res_dict)
            assert 'OK' in res.result


async def test_call_post():
    user_dict = {'id': 113, 'name': 'William'}
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://localhost:4001/users', json=user_dict) as resp:
            res_dict = await resp.json()
            print(res_dict)


async def upload_image():
    with open('hills.png', 'rb') as f:
        async with aiohttp.ClientSession() as session:
            files = {'file': f}
            await session.post('http://localhost:4001/images', data=files)


async def download_image():
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:4001/images"
        async with session.get(url) as resp:
            async with aiofiles.open('images/served.png', mode='wb') as f:
                await f.write(await resp.read())


async def main():
    # t = []
    # for i in range(100):
    #     t.append(create_task(call_server()))
    # print('czekamy...')
    # await gather(*t)
    # print('done')
    # await call_server()
    # await test_add_endpoint(10, 12, expected_result=22)
    # await test_add_endpoint(11, 12, expected_result=22)
    # await test_call_auth()
    # await test_call_post()
    # await download_image()
    await upload_image()


if __name__ == '__main__':
    run(main())
