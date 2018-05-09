dependencies:
	pip install -r requirements.txt


run-worker:
	cd src && DJANGO_SETTINGS_MODULE=mnemotopy.settings.local celery -A mnemotopy -Q media -l info worker

run-worker-prod:
	cd src && DJANGO_SETTINGS_MODULE=mnemotopy.settings.prod celery -A mnemotopy -Q medias -l info worker

run-server:
	DJANGO_SETTINGS_MODULE=mnemotopy.settings.local python manage.py runserver 8081

docker-up:
	docker-compose build
	docker-compose up --scale worker=2

docker-stop:
	docker-compose -f docker-compose.yml stop


# 	docker-compose -f docker-compose.yml up --build -d
#	docker-compose scale worker=2
#	docker-compose up
