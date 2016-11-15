from settings import *

INTERNAL_IPS.append(DOCKER_IPS)

ALLOWED_HOSTS += ['.{{project}}.dev']

DEBUG = True

# Don't log static files
# Grab the original log_message method.
_log_message = WSGIRequestHandler.log_message


def log_message(self, *args):
    # Don't log if path starts with /static/
    if self.path.startswith('/static/'):
        return
    else:
        return _log_message(self, *args)

# Replace log_message with our custom one.
WSGIRequestHandler.log_message = log_message
