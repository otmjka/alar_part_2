## common setup

``` 
# create virtual env
python -m venv env

# activate
source env/bin/activate

# install dependensies
pip install -r requirements.txt 

# ModuleNotFoundError: No module named 'yaml'
pip install pyyaml
```

## Part 1
---

### db setup
```
psql template1 < sql/init_db.sql
```


### permission error

```
psql -U [user_admin] -d aiohttp_security
```

```
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public  TO aiohttp_security;
```

psql aiohttp_security < sql/sample_data.sql -U aiohttp_security

### config

see `config/default.yaml` 

### launch

```
python main.py 
```
open http://localhost:9001

## Part 2

```
source env/bin/activate
python api.py
```

```
source env/bin/activate
python concurently.py
```

in `concurently.py` you can set up timeout, error endpoints for testing

http://0.0.0.0:3333/api/error
http://0.0.0.0:3333/api/timeout




