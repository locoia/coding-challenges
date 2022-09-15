class Development:
    DEBUG = True
    RATELIMIT_ENABLED = True
    ENVIRONMENT = "Dev"
    ENV = ENVIRONMENT
    PORT = 5000
    ...  # add more if needed


class Production:
    DEBUG = False
    SECRET_KEY = "rabbit-x-key"
    RATELIMIT_ENABLED = False
    ENVIRONMENT = "Prod"
    ENV = ENVIRONMENT
