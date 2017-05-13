import json

from simple_settings import settings
from tornado import web
from tornado.escape import json_decode
from tornado.log import app_log

from proxy.redirect import RedirectResolver


class ProxyStatusHandler(web.RequestHandler):
    """Обработчик получения статуса устройства proxy-сервером."""

    def prepare(self):
        try:
            self.body = json_decode(self.request.body)
        except (TypeError, json.JSONDecodeError) as error:
            raise web.HTTPError(400, error)

    def post(self):
        conf = settings.as_dict()
        device_id = self.body['device_id']

        resolver = RedirectResolver(conf['MAP'])

        default = tuple(conf['DEFAULT_SERVER'].split(':'))
        host, port = resolver.get_redirect_address(device_id, default)

        redirect_url = 'http://{host}:{port}{uri}'.format(
            host=host, port=port, uri=self.request.uri)

        self.redirect(url=redirect_url, permanent=True)

        app_log.info(
            'Redirect request {} from device {} to {}'
            ''.format(self.body['request_id'], device_id, redirect_url))
