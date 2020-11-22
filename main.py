from flask import Flask
from flask_apscheduler import APScheduler
from flask_restful import Api

from pingpong import PingPong


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'main:job1',
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 10
        }
    ]

    SCHEDULER_API_ENABLED = True


def job1(a, b):
    print(str(a) + ' ' + str(b))

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config())
    api = Api(app)
    api.add_resource(PingPong, '/ping')
    scheduler = APScheduler()
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run()

