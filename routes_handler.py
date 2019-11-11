from aiohttp import web

from aiohttp_security import (remember, check_authorized, forget)

from db_auth import check_credentials

async def login_handler(request):
  response = web.HTTPFound('/')
  form = await request.post()
  login = form.get('login')
  password = form.get('password')
  db_engine = request.app.db_engine
  if await check_credentials(db_engine, login, password):
    await remember(request, response, login)
    raise response

  raise web.HTTPUnauthorized(
    body=b'Invalid username/password combination')

async def logout_handler(request):
  await check_authorized(request)
  response = web.HTTPFound('/')
  await forget(request, response)
  return response




