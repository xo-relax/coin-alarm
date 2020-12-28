import sys
import os
from dotenv import load_dotenv
from pathlib import Path

basedir = os.path.dirname(os.path.abspath(__file__))
env_path = Path(os.path.join(basedir, ".")) / '../.env'
load_dotenv(dotenv_path=env_path)
prevdir = basedir[:basedir.rfind('/')]
sys.path.append(basedir)
sys.path.append(prevdir)


def is_linux_system():
    return sys.platform == "linux" or sys.platform == "linux2"


if not is_linux_system():
    os.environ['DB_SERVICE'] = "localhost"
    os.environ['DB_PORT'] = "45432"


class BaseConfig(object):
    APP_NAME = 'CORE'

    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASS = os.environ['DB_PASS']
    DB_SERVICE = os.environ['DB_SERVICE']
    DB_PORT = os.environ['DB_PORT']
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(int(os.environ[
        'SQLALCHEMY_TRACK_MODIFICATIONS'
    ]))
