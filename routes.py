from views import index_page, users_page, users_add_page, users_add_handler
from routes_handler import (login_handler, logout_handler)


def setup_routes(app):
  router = app.router
  router.add_get('/', index_page)
  router.add_get('/users', users_page)
  router.add_get('/users/{user_id}', users_add_page) # this handle user_id == 'add'
  router.add_post('/users/{user_id}', users_add_handler) # this handle user_id == 'add'

  router.add_route('*', '/logout', logout_handler, name='logout')

  router.add_post('/login', login_handler, name='login')

  router.add_static('/static/',
                    path='./static',
                    name='static')
