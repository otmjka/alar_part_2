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

user='trifonovdmitry',
                                 database='aiohttp_security',


                                 host='127.0.0.1'


-d "param1=value1&param2=value2"
curl -X POST -d '{"user":"admin", "password": "password"}' 127.1:9001/login -v -c cookie.txt

# response = web.HTTPFound('/')
  # # response = web.json_response({'status': 200})
  # form = await request.json()
  # login = form.get('user')
  # password = form.get('password')
  # print(login, password)
  # db_engine = request.app.db_engine
  # if await check_credentials(db_engine, login, password):
  #   await remember(request, response, login, max_age=30 * 24 * 3600)
  #   raise response
  #
  # raise web.HTTPUnauthorized(body=b'Invalid username/password combination')

forget, authorized_userid,
    check_permission, check_authorized,

# print(type(users_recs), users_recs)
    # return web.json_response(users_recs)

# router = app.router
  # router.add_get('/', index)
  # router.add_get('/users', user_handler)

print(config['postgres'])
# ** config['postgres']