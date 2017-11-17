dependencies:
	pip install -r requirements.txt


run-worker:
	DJANGO_SETTINGS_MODULE=mnemotopy.settings.local bin/worker -Q medias -l info worker
