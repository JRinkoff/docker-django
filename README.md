# docker-django
Ready to go dockerized Django project containing NGINX, Redis, PostgreSQL and Varnish.

## What is included

* Django 1.8
* Postgres 9.4
* Redis
* Nginx
* Varnish

## Prerequisites

1. Docker Compose <https://docs.docker.com/compose/install/>
2. Redirect ```myprojectname.dev``` to ```127.0.0.1``` if you want to use the development server.
3. Done!

## Getting started

Clone the repository

```
git clone https://github.com/MarkDoggen/docker-django.git
```

Run deploy.sh with your projectname to replace placeholders used within the project:

```
bash deploy.sh myprojectname
```

And you're all set! You can now fire up the development server:

```
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

This will make the development server available at http://www.myprojectname.dev

If you want to use the production server, use the following command:

```
docker-compose -f docker-compose.yml -f docker-compose.production.yml up
```

By default, this makes the production server available at http://www.myprojectname.com

## Django applications included

The following applications are included to kickstart your Django project. Of course, you can remove any unwanted dependencies.

* django-cachalot <https://github.com/BertrandBordage/django-cachalot>
* django-compressor <https://github.com/django-compressor/django-compressor>
* django-dbbackup <https://github.com/django-dbbackup/django-dbbackup>
* django-debug-toolbar <https://github.com/jazzband/django-debug-toolbar>
* django-debug-toolbar-template-timings <https://github.com/orf/django-debug-toolbar-template-timings> 
* django-jet <https://pypi.python.org/pypi/django-jet>

Also some middleware like ```TTLMiddleware``` and ```VaryMiddleware``` is included to make it possible to set the Vary and TTL headers from within a Django class-based view. Varnish can then use these headers to determine what to vary on and to determine the TTL of an object.


## Good to know

See ```dev.env``` and ```production.env``` for environment variables being used by Django. Also make sure to check out the config files used by NGINX, Redis, Postgres and Varnish. The default config files included in this project are just added as a basic set-up and it is recommended you edit them so they meet your requirements. 

## Using HTTPS

HTTPS support is also included, with NGINX performing the SSL termination. To use it:

1. Replace ```docker/nginx/nginx.crt``` and ```docker/nginx/nginx.key``` with your own certificate and key.
2. Uncomment the ```ports:  '443:443'``` in docker-compose.yml to open up port 443.
3. Restart the server.




