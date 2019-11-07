async def root_handler(req):
  return web.HTTPFound('/index.html') # FileResponse('/index.html')#

# app.router.add_static('/build/',
  #                       path='./build',
  #                       name='build')

# cors = aiohttp_cors.setup(app)
# cors_headers = {
#   "http://localhost:3000": aiohttp_cors.ResourceOptions(
#     allow_credentials=True,
#     expose_headers=("X-Custom-Server-Header",),
#     allow_headers=("X-Requested-With", "Content-Type"),
#     max_age=3600,
#   )
# }
# res_user = cors.add(app.router.add_resource('/user'))
# cors.add(res_user.add_route('GET', user_handler), cors_headers)
#
# app.router.add_route('GET', '/api', api_handler)