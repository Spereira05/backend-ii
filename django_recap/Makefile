startproject:
	django-admin startapp $(APP) . 

startapp:
	docker compose run --rm web python3 manage.py startapp $(APP)

build:
	docker compose build

down:
	docker compose down 

clean:
	docker compose down --volumes

run: build
	dopcker compose up --force-recreate

migrate:
	docker compose run --force-recreate python3 manage.py migrate

makemigrations:
	docker compose run --force-recreate python3 manage.py makemigrations
