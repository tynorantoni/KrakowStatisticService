import datetime

from flask_restful import Resource


# class for healthchecker service


class PingPong(Resource):

    def get(self):
        return 'pong'