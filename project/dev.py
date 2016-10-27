from settings import *

INTERNAL_IPS.append(DOCKER_IPS)

ALLOWED_HOSTS += ['.{{project}}.dev']

DEBUG = True
