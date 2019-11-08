from aiohttp import web
import aiohttp_jinja2
from aiohttp_security import authorized_userid


@aiohttp_jinja2.template('index.html')
async def index(request):
  username = await authorized_userid(request)
  return {'user': username} if username != None else {}

