from flask_restful import Resource

#class for healthchecker service
from mobilekrakowcrawler import get_values_from_counters, dict_of_streets_with_counters_urls, get_counters_urls, \
    get_street_names


class PingPong(Resource):

    def get(self):
        return 'pong'

#class for testing selenium only for moment
class SelTest(Resource):

    def get(self):
        try:
            get_values_from_counters(dict_of_streets_with_counters_urls(get_counters_urls(),get_street_names()))
            return 'success'
        except Exception as shiet:
            print(shiet)
            return 'failure'