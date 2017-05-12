import json

from simple_settings import settings
from tornado import gen, web
from tornado.escape import json_decode
from tornado.log import app_log
from tornado.web import RequestHandler

from emulate.server.validate import validate_status_request


class StatusHandler(RequestHandler):
    """Обработчик получения статуса устройства."""

    def prepare(self):
        try:
            self.body = json_decode(self.request.body)
        except (TypeError, json.JSONDecodeError) as error:
            raise web.HTTPError(400, error)

    @gen.coroutine
    def post(self):
        validate_status_request(self.body)

        yield gen.sleep(settings.DELAY_TIME)

        self.write(json.dumps({
            'device_id': self.body['device_id'],
            'request_id': self.body['request_id'],
            'result': 'OK'
        }))

        app_log.info(
            'Response to request {} ({}) from {}'.format(
                self.body['request_id'], self.body['device_id'],
                self.request.host))
