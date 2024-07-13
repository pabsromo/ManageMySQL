# ManageMySQL
A containerized Django application that allows users to create and manage MySQL db virtual machines through a simple barebones UI.

# Steps to Build and Run
1. Make sure you have docker and docker compose installed
2. Go to root of project where `docker-compose.yaml` exists and run this:
    * ```docker compose build```
3. Clean up existing containers
    * ```docker stop $(docker ps -a -q)```
    * ```docker rm $(docker ps -a -q)```
5. Check to make sure no containers are left
    * ```docker ps -a```
6. Spin up containers. Make sure you are in same directory as `.env`
    * ```docker compose up```
7. Apply migrations for apps
    * ```docker compose run web python manage.py migrate```
8. Go to http://localhost:8000/ to make sure everything is up and good!

# Research
## Sending Shell Commands to Host
- https://stackoverflow.com/questions/32163955/how-to-run-shell-script-on-host-from-docker-container/49873529#49873529
- https://stackoverflow.com/questions/32163955/how-to-run-shell-script-on-host-from-docker-container
- https://betterstack.com/community/guides/scaling-python/dockerize-django/#step-2-setting-up-a-local-postgresql-database

## Creating a mysql container with docker commands:
### Template:
```
docker run -d \
  --name <name> \
  -e MYSQL_DATABASE=<database name> \
  -e MYSQL_ROOT_PASSWORD=<password here> \
  -v <name>-data:/var/lib/mysql \
  -p <non-clashing port>:3306 \
  mysql:8.0.19 --default-authentication-plugin=mysql_native_password
```
### Example:
```
docker run -d \
  --name db2 \
  -e MYSQL_DATABASE=example2 \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw-2 \
  -v db2-data:/var/lib/mysql \
  -p 3307:3306 \
  mysql:8.0.19 --default-authentication-plugin=mysql_native_password
  ```
Should have...
- Default user as `root`
- IP address of WSL2 if running on there or localhost if not

## General Resource
- Example this is based off: https://github.com/betterstack-community/django-todo-app/tree/docker