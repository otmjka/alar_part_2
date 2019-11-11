import asyncio
import aiohttp
import async_timeout


BASE_URL = 'http://0.0.0.0:3333/api/{}'
FETCH_TIMEOUT = 2
end_points = ['first', 'second', 'error']
urls = [BASE_URL.format(s) for s in end_points]


async def fetch(client, url):
  try:
    with async_timeout.timeout(FETCH_TIMEOUT):
      async with client.get(url) as resp:
        print(resp.status, url)
        assert resp.status == 200
        return await resp.json()
  except (asyncio.TimeoutError, AssertionError):
    # expired or ani HTTP error while requestion
    return []


async def main():
  async with aiohttp.ClientSession() as client:
    fetch_all = await asyncio.gather(fetch(client, urls[0]), fetch(client, urls[1]), fetch(client, urls[2]))
    result = []

    for part in fetch_all:
      result += part

    sorted_result = sorted(result, key=lambda key: key['id'])
    print(sorted_result)
    return result


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
