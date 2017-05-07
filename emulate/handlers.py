import json

from cerberus import Validator
from simple_settings import settings
from tornado import gen, web
from tornado.escape import json_decode
from tornado.log import app_log
from tornado.web import RequestHandler


class StatusHandler(RequestHandler):
    """Обработчик получения статуса устройства."""

    # Схема валидации тела запроса
    schema = {
        'device_id': {'type': 'string'},
        'request_id': {'type': 'string', 'min': 16, 'max': 16},
        'status': {'type': 'string'},
        'data': {'type': 'dict'},
    }

    def prepare(self):
        self.args = json_decode(self.request.body)
        is_validate = Validator().validate(self.args, self.schema)

        if not is_validate:
            raise web.HTTPError(
                400, 'Request body ({}) is not validated to schema ({}).'
                     ''.format(self.request.body, self.schema))

    @gen.coroutine
    def post(self):
        yield gen.sleep(settings.DELAY_TIME)

        self.write(json.dumps({
            'device_id': self.args['device_id'],
            'request_id': self.args['request_id'],
            'result': 'OK'
        }))

        app_log.info('Response to request {}'.format(self.args['request_id']))
