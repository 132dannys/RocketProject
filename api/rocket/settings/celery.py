from rocket.enviroment import env
from .django import TIME_ZONE as DJANGO_TIME_ZONE


CELERY_ALWAYS_EAGER = env.bool("ROCKET_CELERY_ALWAYS_EAGER", default=False)
CELERY_BROKER_URL = env.str("ROCKET_CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env.str("ROCKET_CELERY_RESULT_BACKEND_URL", default=CELERY_BROKER_URL)

CELERY_TIMEZONE = DJANGO_TIME_ZONE
CELERY_TASK_IGNORE_RESULT = True

CELERY_BEAT_SCHEDULE = {}