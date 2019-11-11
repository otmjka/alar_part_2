import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import (authorized_userid)


async def handle_404(request):
  return aiohttp_jinja2.render_template('404.html', request, {})


async def handle_500(request):
  return aiohttp_jinja2.render_template('500.html', request, {})

async def handle_403(request):
  username = await authorized_userid(request)
  view_data = {'error': True, 'error_msg': '403: Forbidden'}
  if username != None:
    view_data = {**view_data, **{'user': username}}
  return aiohttp_jinja2.render_template('403.html', request, view_data)


async def handle_401(request):
  return aiohttp_jinja2.render_template('index.html', request, {})


def create_error_middleware(overrides):
  @web.middleware
  async def error_middleware(request, handler):

    try:
      response = await handler(request)

      override = overrides.get(response.status)
      if override:
        return await override(request)

      return response

    except web.HTTPException as ex:
      override = overrides.get(ex.status)
      if override:
        return await override(request)

      raise

  return error_middleware

def setup_middlewares(app):
  error_middleware = create_error_middleware({
    401: handle_401,
    403: handle_403,
    404: handle_404,
    500: handle_500
  })
  app.middlewares.append(error_middleware)
