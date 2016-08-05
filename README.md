# Queryset checker

## Installation (on Debian 8):
At first, need to install:
    
    sudo apt update 
    sudo apt install rabbitmq-server git-core python3-setuptools \
    python3-virtualenv python3-pip python-virtualenv postgresql-9.5 \
    postgresql-client-9.5 postgresql-contrib libpq-dev python3-dev \

Create postgress db & db user:

    CREATE USER checker WITH password '123456';
    ALTER USER checker CREATEDB;
    CREATE DATABASE checker;
    GRANT ALL privileges ON DATABASE checker TO checker;
    
After db creation:

    git clone git://github.com/vechnoe/queryset_checker && cd queryset_checker
    make
    
## Running on development mode:
    make run

Your server starts on *127.0.0.1:8000*

Admin login: *admin*
Admin password: *12345*

Then, needs to start Celery workers (on separate terms) following by:

    make celery_queries_node
    make celery_data_node
    make celery_results_node

Starting Celery-Flower management:
    
    make celery-flower
    
Celery starts on *127.0.0.1:9999*
    