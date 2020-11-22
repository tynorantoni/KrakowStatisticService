from flask import Flask
from flask_apscheduler import APScheduler
from flask_restful import Api

from mobilekrakowcrawler import *
from pingpong import PingPong


class Config(object):
    JOBS = [
        {
            'id': 'crawl_krakow_data',
            'func': 'main:crawl_krakow_data',
            'trigger': 'interval',
            'seconds': 86400
        }
    ]

    SCHEDULER_API_ENABLED = True


def crawl_krakow_data():
    # get_values_from_counters(dict_of_streets_with_counters_urls(get_counters_urls(),get_street_names()))
    print(666)

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

