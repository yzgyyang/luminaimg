# LuminaImg

An image repository.

## Deployment

Have these environmental variables available:
```
export S3_BUCKET=""
export S3_KEY=""
export S3_SECRET=""
```

The following environmental variables are optional:
```
export APP_SECRET_KEY="" # default is "dev"
export DB_USER="" # default is "luminauser"
export DB_PASSWORD="" # default is "luminapassword"
export DB_URI="" # default is "localhost:3306"
export DB_NAME="" # default is "luminadb"
```

Create an virtual environment:
```
virtualenv env --python=python3
source env/bin/activate
(env) pip install -r requirements.txt
```

Run a production server at port 7200:
```
(env) pip install gunicorn
(env) gunicorn --bind 0.0.0.0:7200 app:app
```

Finally, run a reverse proxy server ;)
