from asyncio import run, create_task, gather

import aiohttp


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


async def main():
    # t = []
    # for i in range(100):
    #     t.append(create_task(call_server()))
    # print('czekamy...')
    # await gather(*t)
    # print('done')
    # await call_server()
    await test_add_endpoint(10, 12, expected_result=22)
    await test_add_endpoint(11, 12, expected_result=22)


if __name__ == '__main__':
    run(main())
