---
Project name: Django_tatum
Topic: Startup instructions
---


1. Please see these articles on using poetry to manage virtualenvironments:

a. [Using to Poetry with Django]("https://rasulkireev.com/managing-django-with-poetry/"){target="_blank"}
b. [Dependency Management with Python Poetry](https://realpython.com/dependency-management-python-poetry/){target="_blanck"}

Here is the poetry doc for installing dependencies to the project:
["https://python-poetry.org/docs/basic-usage/#installing-dependencies"]{target="_blank"}

2. Preferably, use this command to create a virtual in the same directory as the current directory:

> poetry config virtualenvs.in-project true

3. To activate virtualenv from default directory of installation:
> source $(poetry env info --path)/bin/activate

3. For populating requirements.txt, use this command:
	> poetry export -f requirements.txt --output requirements.txt

4.[Connect Azure Postgres instance to pgAdmin4]("https://www.sqlshack.com/accessing-azure-database-for-postgresql-using-pgadmin/"){target="_blank"}

5. [Running cron jobs with django extensions]('https://django-extensions.readthedocs.io/en/latest/jobs_scheduling.html'){target="_blank"}
6. [Graphene bug fix]('https://stackoverflow.com/questions/70382084/import-error-force-text-from-django-utils-encoding'){target="_blank"}


# Running the application

# Working with Tatum KMS
[Tatum KMS Docs](https://docs-v3.tatum.io/private-key-management/tatum-key-management-system-kms)
KMS securely stores private keys and mnemonics of blockchain wallets.
KMS periodically pulls pending transactions to sign from Tatum, signs them locally using the stored private keys and mnemonics, and broadcasts them to the blockchain.


# Publishing updates to the package to pypi
1. Update the version number in setup.py
2. Run the following command to build the package
> python setup.py sdist bdist_wheel
3. Run the following command to upload the package to pypi
> twine upload dist/*
4. Run the following command to install the package from pypi
> pip install django-tatum
5. If you want to publish your app to dockerhub, follow these steps:
a. Create a dockerhub account
b. Create a repository in dockerhub
c. Create a dockerfile in the root of your project
d. Build the docker image
> docker build -t <dockerhub_username>/<dockerhub_repository_name>:<tag_name> .
e. Push the docker image to dockerhub
> docker push <dockerhub_username>/<dockerhub_repository_name>:<tag_name>
f. Run the docker image
> docker run -p 8000:8000 <dockerhub_username>/<dockerhub_repository_name>:<tag_name>
g. If you want to run the docker image in the background, run the following command
> docker run -d -p 8000:8000 <dockerhub_username>/<dockerhub_repository_name>:<tag_name>
h. If you want to stop the docker image, run the following command
> docker stop <container_id>
i. If you want to remove the docker image, run the following command
> docker rm <container_id>
j. If you want to remove the docker image, run the following command
> docker rmi <image_id>

# Running the application
1. Run the following command to start the application
> python manage.py runserver
2. Run the following command to run the tests
> python manage.py test
3. Run the following command to run the tests with coverage
> coverage run --source='.' manage.py test
4. Run the following command to generate the coverage report
> coverage report
5. Run the following command to generate the coverage html report
> coverage html
6. Run the following command to generate the coverage xml report
> coverage xml

# Running the application with docker
1. Run the following command to build the docker image
> docker build -t django-tatum .
2. Run the following command to run the docker image
> docker run -p 8000:8000 django-tatum

# Running the application with docker-compose
1. Run the following command to build the docker image
> docker-compose build
2. Run the following command to run the docker image
> docker-compose up
3. Run the following command to run the docker image in the background
> docker-compose up -d
4. Run the following command to stop the docker image
> docker-compose stop
5. Run the following command to remove the docker image
> docker-compose rm

# Running the application with docker-compose and postgres
1. Run the following command to build the docker image
> docker-compose -f docker-compose-postgres.yml build
2. Run the following command to run the docker image
> docker-compose -f docker-compose-postgres.yml up
3. Run the following command to run the docker image in the background
> docker-compose -f docker-compose-postgres.yml up -d
4. Run the following command to stop the docker image
> docker-compose -f docker-compose-postgres.yml stop

# Running the application with docker-compose and postgres and redis
1. Run the following command to build the docker image
> docker-compose -f docker-compose-postgres-redis.yml build
2. Run the following command to run the docker image
> docker-compose -f docker-compose-postgres-redis.yml up
3. Run the following command to run the docker image in the background
> docker-compose -f docker-compose-postgres-redis.yml up -d
4. Run the following command to stop the docker image
> docker-compose -f docker-compose-postgres-redis.yml stop


# Running the application with docker-compose and postgres and redis and celery and flower
1. Run the following command to build the docker image
> docker-compose -f docker-compose-postgres-redis-celery-flower.yml build
2. Run the following command to run the docker image
> docker-compose -f docker-compose-postgres-redis-celery-flower.yml up
3. Run the following command to run the docker image in the background
> docker-compose -f docker-compose-postgres-redis-celery-flower.yml up -d
4. Run the following command to stop the docker image
> docker-compose -f docker-compose-postgres-redis-celery-flower.yml stop
