from flask import Flask
from flask_apscheduler import APScheduler
from flask_restful import Api
from pingpong import PingPong, SelTest


#scheduling class
class Config(object):
    JOBS = [
        {
            'id': 'crawl_krakow_data',
            'func': 'app:crawl_krakow_data',
            'trigger': 'interval',
            'seconds': 86400
        }
    ]

    SCHEDULER_API_ENABLED = True

#function triggered in intervals (once a day)
def crawl_krakow_data():
    # get_values_from_counters(dict_of_streets_with_counters_urls(get_counters_urls(),get_street_names()))
    pass



app = Flask(__name__)
app.config.from_object(Config())
api = Api(app)

#add 'ping' routing for healthchecker service
api.add_resource(PingPong, '/ping')
api.add_resource(SelTest, '/cycling')
scheduler = APScheduler()

#scheduling start
scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
