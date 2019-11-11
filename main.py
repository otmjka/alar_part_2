import asyncio

import aiohttp_jinja2
import jinja2
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy
from aiopg.sa import create_engine
from aioredis import create_pool

from aiohttp import web

from db_auth import DBAuthorizationPolicy
from settings import config

from routes import setup_routes
from middlewares import setup_middlewares


async def init(loop):
  # Redis
  redis_opts = (config['redis']['host'], config['redis']['port'])
  redis_pool = await create_pool(redis_opts)

  # SQLAlchemy
  sa_cfg = config['postgres']
  dbengine = await create_engine(database=sa_cfg.get('database', 'aiohttp_security'),
                                 user=sa_cfg.get('user', 'admin'))

  app = web.Application()
  app.db_engine = dbengine
  # Auth
  setup_session(app, RedisStorage(redis_pool))
  setup_security(app,
                 SessionIdentityPolicy(),
                 DBAuthorizationPolicy(dbengine))
  aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./templates'))
  setup_routes(app)
  setup_middlewares(app)


  handler = app._make_handler()

  app_conf = config['app']
  srv = await loop.create_server(handler,
                                 app_conf['host'],
                                 app_conf['port'])

  print('Server started at http://{}:{}'.format(str(app_conf['host']), str(app_conf['port'])))

  return srv, app, handler


async def finalize(srv, app, handler):
  # TODO: correct
  sock = srv.sockets[0]
  app.loop.remove_reader(sock.fileno())
  sock.close()
  srv.close()
  await srv.wait_closed()
  await app.finish()


def main():
  loop = asyncio.get_event_loop()
  srv, app, handler = loop.run_until_complete(init(loop))
  try:
    loop.run_forever()
  except KeyboardInterrupt:
    loop.run_until_complete((finalize(srv, app, handler)))


if __name__ == '__main__':
  main()
