from rocket.enviroment import env


ROCKET_FEATURES = env.list("ROCKET_FEATURES", default=[])
