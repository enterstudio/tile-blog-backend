# tile-blog-backend
A simple REST API for ember-tile-blog

...so yeah, I was going to use firebase.  Turns out Amazon S3 integration (and other admin tasks) isn't so easy without a backend.  

On the upside, this repo is still pretty easy to use!

## Setup

You need `pip`, `postgres`, and `virtualenv`.  You also need a config file (This app will look for `config/local.env`) 
with the following fields (Set these as environment variables if working on Heroku):

```
DJANGO_SECRET_KEY=<some-secret-key>
BLOG_DB_NAME=<your-local-postgres-db-name>
PAGE_SIZE=<number-of-posts-per-page>
POSTGRES_DB_USER=<your-postgres-username>
POSTGRES_DB_PASS=<your-postgres-password>
AWS_ACCESS_KEY=<your-aws-access-key-id>
AWS_SECRET_KEY=<your-aws-secret-key>
S3_BUCKET=<your-aws-bucket-name>
```

To run download and the server locally, just enter the following commands from your working directory:

```
$ git clone https://github.com/Fuiste/tile-blog-backend.git
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ ./manage.py runserver
```
