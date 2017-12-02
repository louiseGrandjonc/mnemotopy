dependencies:
	pip install -r requirements.txt


run-worker:
	cd src && DJANGO_SETTINGS_MODULE=mnemotopy.settings.local celery -A mnemotopy -Q media -l info worker

run-worker-prod:
	cd src && DJANGO_SETTINGS_MODULE=mnemotopy.settings.prod celery -A mnemotopy -Q medias -l info worker
