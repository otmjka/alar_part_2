import asyncio
from aiohttp import web
from typing import List, Dict


def make_src(start: int = 1, amount: int = 10) -> List[Dict[str, str]]:
    return [dict(id=uuid, name='Test {}'.format(uuid)) for uuid in range(start, start + amount)]


def make_all_sources():
    first_src = make_src(start=1) + make_src(start=31)
    second_src = make_src(start=11) + make_src(start=41)
    third_src = make_src(start=21) + make_src(start=51)
    return first_src, second_src, third_src


# app staff
def make_handler(src: List[Dict[str, str]]):
    async def src_handler(request):
        return web.json_response(src)
    return src_handler


async def timeout_handler(request):
    await asyncio.sleep(3)
    response = make_src(start=100, aount=20)
    return web.json_response(response)


def setup_routes(app):
    first_src, second_src, third_src = make_all_sources()
    router = app.router
    router.add_get('/api/first', make_handler(first_src))
    router.add_get('/api/second', make_handler(second_src))
    router.add_get('/api/third', make_handler(third_src))
    router.add_get('/api/timeout', timeout_handler)


def run():
    app = web.Application()
    setup_routes(app)
    web.run_app(app, port=3333)


if __name__ == '__main__':
    run()
