from flask import Flask
from flask_apscheduler import APScheduler


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

    scheduler = APScheduler()
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run()

# from pingpong import start
#
# from timeloop import Timeloop
# from datetime import timedelta
# import datetime
#
# tl = Timeloop()
#
# @tl.job(interval=timedelta(seconds=10))
# def print_jello():
#     print('hello ',datetime.datetime.now())
#
#
#
#
# if __name__ == '__main__':
#
#
#     tl.start(block=True)
#     start()
#
#
