async def validate_add_user_form(request):
  form = await request.post()
  user_edit = dict(login = form.get('login'),
                   password = form.get('password'),
                   password2 = form.get('password2'),
                   public = form.get('public'),
                   protected = form.get('protected'),
                   is_super = form.get('is_super'),
                   is_disabled = form.get('is_disabled'))
  error = ''
  if (not isinstance(user_edit['login'], str)
    or len(user_edit['login']) < 6):
    error += 'login should be a string with length greater than 6. '
  if error == '':
    login_exists = await is_login_exists(user_edit['login'], request=request)
    if login_exists:
      error += 'The User with typed login are exists'
  if (not isinstance(user_edit['password'], str)
    or len(user_edit['password']) < 6):
    error += 'password should be a string with length greater than 6. '
  if (not isinstance(user_edit['password'], str)
    or user_edit['password'] != user_edit['password2']):
    error += 'password and retype password fields should be equal'

  error = None if error == '' else error

  print('users_edit_handler', user_edit, error)
  if error == None:
    return user_edit, None

  username = await authorized_userid(request)
  user_id = request.match_info.get('user_id', None)
  return user_edit, {
    'user': username,
    'is_add': user_id == 'add',
    'user_id': user_id,
    'user_edit': user_edit,
    'error': error
  }