# Start first part
``` 
# create virtual env
python -m venv env

# activate
source env/bin/activate

# install dependensies
pip install -r requirements.txt 

```

## db setup

psql template1 < sql/init_db.sql
psql aiohttp_security < sql/sample_data.sql

# install bootstrap
npm i bootstrap
cp node_modules/bootstrap/dist/css/bootstrap.min.css ./static
