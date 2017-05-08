import json

from cerberus import Validator
from simple_settings import settings
from tornado import gen, web
from tornado.escape import json_decode
from tornado.log import app_log
from tornado.web import RequestHandler

from emulate.mapping import RedirectMapper


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


class ProxyStatusHandler(RequestHandler):
    """Обработчик запроса на proxy-сервер."""

    def post(self):
        conf = settings.as_dict()
        device_id = json_decode(self.request.body)['device_id']

        mapper = RedirectMapper(conf['MAP'])
        host, port = mapper.get_redirect_address(
            device_id, tuple(conf['DEFAULT_SERVER'].values()))

        redirect_url = 'http://{host}:{port}{uri}'.format(
            host=host, port=port, uri=self.request.uri)

        self.redirect(url=redirect_url, permanent=True)
