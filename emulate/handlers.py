import json

from simple_settings import settings
from tornado import gen, web
from tornado.escape import json_decode
from tornado.log import app_log
from tornado.web import RequestHandler

from emulate.mapping import RedirectResolver
from emulate.validate import validate_status_request


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

        app_log.info('Response to request {}'.format(self.body['request_id']))


class ProxyStatusHandler(RequestHandler):
    """Обработчик получения статуса устройства proxy-сервером."""

    def prepare(self):
        try:
            self.body = json_decode(self.request.body)
        except (TypeError, json.JSONDecodeError) as error:
            raise web.HTTPError(400, error)

    def post(self):
        validate_status_request(self.body)

        conf = settings.as_dict()
        body = json_decode(self.request.body)
        device_id = body['device_id']

        mapper = RedirectResolver(conf['MAP'])

        default = tuple(conf['DEFAULT_SERVER'].split(':'))
        host, port = mapper.get_redirect_address(device_id, default)

        redirect_url = 'http://{host}:{port}{uri}'.format(
            host=host, port=port, uri=self.request.uri)

        self.redirect(url=redirect_url, permanent=True)

        app_log.info(
            'Request {} from device {} redirects to {}'
            ''.format(body['request_id'], device_id, redirect_url))
