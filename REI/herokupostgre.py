import dj_database_url
import django_heroku
from .settings import *

ALLOWED_HOSTS.append('https://rei-postgre.herokuapp.com/')
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
django_heroku.settings(locals())
