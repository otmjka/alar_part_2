from views import index, users

def setup_routes(app):
  router = app.router
  router.add_get('/', index)
  router.add_get('/users', users)

