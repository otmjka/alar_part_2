import asyncio
import aiohttp
from aiohttp_security import (
    remember, forget, authorized_userid,
    check_permission, check_authorized,
)
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
# from handlers import Web
from views import index
import async_timeout
from db_auth import check_credentials
from settings import config


async def user_handler(request):
  # await check_permission(request, 'protected')
  response = {'user': 'vasya'}
  return web.json_response(response)

async def users(request):
  response = {'id':  1, 'name': 'vasya'}
  return web.json_response(response)

async def login(request):
  response = web.HTTPFound('/')
  form = await request.post()
  login = form.get('login')
  password = form.get('password')
  print(login, password)
  db_engine = request.app.db_engine
  if await check_credentials(db_engine, login, password):
    await remember(request, response, login)
    raise response

  raise web.HTTPUnauthorized(body=b'Invalid username/password combination')


async def init(loop):

  redis_opts = (config['redis']['host'], config['redis']['port'])
  redis_pool = await create_pool(redis_opts)
  print(config['postgres'])
  # ** config['postgres']
  dbengine = await create_engine(database = 'aiohttp_security', user='admin')
  app = web.Application()
  app.db_engine = dbengine
  setup_session(app, RedisStorage(redis_pool))
  setup_security(app,
                 SessionIdentityPolicy(),
                 DBAuthorizationPolicy(dbengine))

  aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./templates'))

  router = app.router
  router.add_get('/', index)
  router.add_get('/users', user_handler)
  router.add_route('POST', '/login', login, name='login')

  router.add_static('/static/',
                        path='./static',
                        name='static')



  handler = app._make_handler()

  app_conf = config['app']
  srv = await loop.create_server(handler,
                                 app_conf['host'],
                                 app_conf['port'])

  print('Server started at http://{}:{}',
        format(str(app_conf['host']), str(app_conf['port'])))

  return srv, app, handler

async def finalize(srv, app, handler):
  sock = srv.sockets[0]
  app.loop.remove_reader(sock.fileno())
  sock.close()

  await handler.finish_connections(1.0)
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
