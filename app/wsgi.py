# flake8: noqa
from bottle import run

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from web_api import app

application = app


if __name__ == '__main__':
    run(application, host='0.0.0.0', port=8080, reloader=True, debug=True)
