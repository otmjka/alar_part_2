from aiohttp import web
import aiohttp_jinja2
from aiohttp_security import (authorized_userid,
                              check_permission)

from users.db import add_user, fetch_all_users, fetch_full_user
from users.validation import validate_add_user_form

ADD_USER = 'add'
PERM = 'permissions'

@aiohttp_jinja2.template('index.html')
async def index_page(request):
  username = await authorized_userid(request)
  return {'user': username} if username != None else {}


@aiohttp_jinja2.template('users.html')
async def users_page(request):
  await check_permission(request, 'public')
  username = await authorized_userid(request)
  users_recs = await fetch_all_users(request=request)
  return {'user': username, 'users': users_recs}

@aiohttp_jinja2.template('add_user_page.html')
async def users_add_page(request):
  await check_permission(request, 'protected')
  user_id = request.match_info.get('user_id', None)
  assert user_id != None

  username = await authorized_userid(request)
  user_edit = {}
  if user_id != ADD_USER:
    # user_id is number
    user_edit = await fetch_full_user(user_id=user_id, request=request)

  return {
    'user': username,
    'is_add': user_id == 'add',
    'user_id': user_id,
    'user_edit': user_edit,
  }

@aiohttp_jinja2.template('add_user_page.html')
async def users_add_handler(request):
  await check_permission(request, 'protected')
  # login exists, login, psw < 6, psw != psw2
  user_edit, error = await validate_add_user_form(request=request)

  # display template with errors
  if error:
    return error

  # redirect to users page with updated users info
  if add_user(request=request, user_edit=user_edit) == None:
    response = web.HTTPFound('/users')
    return response
