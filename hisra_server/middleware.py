import settings


class CorsMiddleware(object):

    def __init__(self):
        self.allowed_origin = settings.ALLOWED_ORIGIN

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = self.allowed_origin
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT'
        return response
