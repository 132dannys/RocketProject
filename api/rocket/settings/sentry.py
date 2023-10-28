import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

from rocket.enviroment import env


USE_SENTRY = env.bool("ROCKET_USE_SENTRY", default=True)
if USE_SENTRY:
    sentry_kwargs = {
        "dsn": env.str("ROCKET_SENTRY_DSN"),
        "environment": env.str("ROCKET_SENTRY_ENVIRONMENT"),
        "integrations": [DjangoIntegration(), CeleryIntegration()],
    }
    sentry_sdk.init(**sentry_kwargs)
