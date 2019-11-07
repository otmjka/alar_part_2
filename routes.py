from views import index

def setup_routes(app):
  router = app.router
  router.add_get('/', index)

