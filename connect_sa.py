import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa

metadata = sa.MetaData()

users = sa.Table(
  'users', metadata,
  sa.Column('id', sa.Integer, nullable=False),
  sa.Column('login', sa.String(256), nullable=False),
  sa.Column('passwd', sa.String(256), nullable=False),
  sa.Column('is_superuser', sa.Boolean, nullable=False,
            server_default='FALSE'),
  sa.Column('disabled', sa.Boolean, nullable=False,
            server_default='FALSE'),

  # indices
  sa.PrimaryKeyConstraint('id', name='user_pkey'),
  sa.UniqueConstraint('login', name='user_login_key'),
)

async def init():
    db_engine = await create_engine(database = 'aiohttp_security', user='admin')

    async with db_engine.acquire() as conn:
        async for row in conn.execute(users.select()):
            print(row.id, row.login)

loop = asyncio.get_event_loop()
loop.run_until_complete(init())

