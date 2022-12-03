from asyncio import run, sleep

import asyncpg

from asynchr.db.db_config import DB_HOST, DB_PASS


class DbService:

    def __init__(self, host: str, passwd: str):
        self.host = host
        self.passwd = passwd


    async def initialize(self):
        self.pool =  await asyncpg.create_pool(host=self.host, password=self.passwd, user='postgres')
        print('connected!')


async def main():
    db = DbService(DB_HOST, DB_PASS)
    await db.initialize()
    await sleep(1)

if __name__ == '__main__':
    run(main())