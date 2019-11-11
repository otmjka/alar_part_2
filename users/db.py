from db import permissions, users


PERM = 'permissions'

async def is_login_exists(login, request=None):
  db_engine = request.app.db_engine
  async with db_engine.acquire() as conn:
    query = users.select().where(users.c.login == login)
    ret = await conn.execute(query)
    user = await ret.fetchone()
    return False if user == None else True

from passlib.hash import sha256_crypt

async def add_user(user_edit=None, request=None):
  db_engine = request.app.db_engine
  async with db_engine.acquire() as conn:
    query = users.count()
    count = await conn.scalar(query)
    passwd = sha256_crypt.hash(user_edit['password'])
    query = users.insert().values(id=count + 1,
                                  login=user_edit['login'],
                                  passwd=passwd,
                                  is_superuser=False,
                                  disabled=False, )
    result = await conn.execute(query)
    print('!', result)
    return None

async def fetch_full_user(user_id=None, request=None):
  db_engine = request.app.db_engine
  async with db_engine.acquire() as conn:
    query = users.select().where(users.c.id == user_id)
    ret = await conn.execute(query)
    user = await ret.fetchone()
    print(user)
    user_edit = dict(id=user[0], login=user[1],
                     is_superuser=user[3], disabled=user[4])
    print(user_edit)
    # fetch user permissions
    query = permissions.select().where(permissions.c.user_id == user_id)
    async for permission in conn.execute(query):
      print('permission', permission)
      p_list = user_edit.get(PERM, list())
      p_list.append(permission[2])
    user_edit[PERM] = p_list

async def fetch_all_users(request=None):
  db_engine = request.app.db_engine
  users_recs = []
  async with db_engine.acquire() as conn:
    async for user in conn.execute(users.select()):
      users_recs += [dict(id=user[0], login=user[1],
                          is_superuser=user[3], disabled=user[4])]

    # fetch permissions and mutate users_recs
    async for permission in conn.execute(permissions.select().order_by(permissions.c.user_id)):
      user_id = permission[1] - 1
      p_name = permission[2]
      permission_list = users_recs[user_id].get(PERM, list())
      permission_list += [p_name]
      users_recs[user_id][PERM] = permission_list
    return users_recs