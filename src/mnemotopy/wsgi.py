import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mnemotopy.settings.heroku")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
