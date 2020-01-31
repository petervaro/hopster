from os import environ
from os.path import abspath, dirname
from sys import stderr, exit

from exitstatus import ExitStatus


APP_BASE_DIR = abspath(dirname(__file__))

_sk_env_var = 'HOPSTER_SERVER_SECRET_KEY'

try:
    SECRET_KEY = environ[_sk_env_var]
except KeyError:
    print('Have you forgot to define the secret key for the server?',
          f'(Hint: undefined environment variable: {_sk_env_var})',
          sep='\n',
          file=stderr)
    exit(ExitStatus.failure)
