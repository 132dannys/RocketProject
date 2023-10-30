from rocket.enviroment import env  # noqa: F401

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_RENDER_CLASSES": [
        "rest_framework.renders.JSONRenderer",
        "rest_framework.renders.BrowsableAPIRenderer",
    ],
}

# CORS_ALLOWED_ORIGINS = env.list("ROCKET_CORS_ALLOWED_ORIGINS", default=[])
# CORS_ALLOW_ALL_ORIGINS = env.bool("ROCKET_CORS_ALLOW_ALL_ORIGINS", default=False)
