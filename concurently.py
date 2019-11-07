# from  import aiohttp ClientSession, web
# import async_timeout
#
# FETCH_TIMEOUT = 2
#
# async def fetch(session, url):
#   # global fetch_counter
#   # with async_timeout.timeout(FETCH_TIMEOUT):
#   #   fetch_counter += 1
#   print(url)
#   async with session.get(url) as resp:
#     assert resp.status == 200
#     res = await resp.json()
#     print(res)
#     return res
#
#
# async def api_handler(request):
#   # loop = request.app.loop
#
#   async with ClientSession() as client:
#     results = asyncio.gather(fetch(client, urls[0]),
#                              fetch(client, urls[1]),
#                              fetch(client, urls[2]))
#     print(results)
#     return web.json_response(results)
#
#
# async def init(loop):
#   app = web.Application()
#   app.router.add_get('/run', api_handler)
#   handler = app._make_handler()
#   srv = await loop.create_server(handler, '127.0.0.1', 3334)
#   print('Server started at http://127.0.0.1:3334')
#   return srv, app, handler
#
# if __name__ == '__main__':
#   loop = asyncio.get_event_loop()
#   srv, app, handler = loop.run_until_complete(init(loop))
#

import asyncio
import aiohttp

BASE_URL = 'http://0.0.0.0:3333/api/{}'
end_points = ['first', 'second', 'third']
urls = [BASE_URL.format(s) for s in end_points]

async def fetch(client, url):
  async with client.get(url) as resp:
    print(resp.status, url)
    assert resp.status == 200
    return await resp.json()


async def main():
  async with aiohttp.ClientSession() as client:
    result = await asyncio.gather(fetch(client, urls[0]), fetch(client, urls[1]), fetch(client, urls[2]))
    print(result)
    return result
    # result = await fetch(client, urls[0])
    # print(result)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
