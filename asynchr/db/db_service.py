from asyncio import run, sleep

import asyncpg

from asynchr.db.db_config import DB_HOST, DB_PASS
from asynchr.db.model import User


class DbService:

    def __init__(self, host: str, passwd: str):
        self.host = host
        self.passwd = passwd

    async def initialize(self):
        self.pool = await asyncpg.create_pool(host=self.host, password=self.passwd, user='postgres', database='postgres')
        print('connected!')

    async def get_users(self, offset=0, limit=500) -> list[User]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from users order by name offset $1 limit $2', offset, limit)
        return [User(**dict(r)) for r in rows]

    async def upsert(self, user: User) -> User:
        # if user.uid==0 -- new user -- insert; else update user with given user.uid
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow("insert into users(name, address) VALUES ($1, $2) returning *",
                                             user.name, user.address)
        return User(**dict(row))


async def main():
    db = DbService(DB_HOST, DB_PASS)
    await db.initialize()
    await db.upsert(User(0, 'Li', 'Ningbo'))
    for u in await db.get_users(offset=0):
        print(u)
    await sleep(1)
    await db.pool.close()
    await sleep(1)


if __name__ == '__main__':
    run(main())
