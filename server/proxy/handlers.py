import json

from simple_settings import settings
from tornado import web, gen
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.log import app_log

from server.proxy.redirect import RedirectResolver
from server.validate import validate_status_request


class ProxyStatusHandler(web.RequestHandler):
    """Обработчик получения статуса устройства proxy-сервером."""

    def prepare(self):
        try:
            self.body = json_decode(self.request.body)
        except (TypeError, json.JSONDecodeError) as error:
            raise web.HTTPError(400, error)

    @gen.coroutine
    def post(self):
        is_validate, reason = validate_status_request(self.body)

        if not is_validate:
            self.write({
                'result': 'Validation error',
                'reason': reason
            })
            self.finish()

        conf = settings.as_dict()
        device_id = self.body['device_id']

        resolver = RedirectResolver(conf['MAP'])

        default = tuple(conf['DEFAULT_SERVER'].split(':'))
        host, port = resolver.get_redirect_address(device_id, default)

        redirect_url = 'http://{host}:{port}{uri}'.format(
            host=host, port=port, uri=self.request.uri)

        # Создаем новый запрос, с подменой URL
        redirect_request = HTTPRequest(
            url=redirect_url,
            method='POST',
            headers=self.request.headers,
            body=self.request.body
        )

        app_log.info(
            'Redirect request {} from device {} to {}'
            ''.format(self.body['request_id'], device_id, redirect_url))

        # Перенаправляем запрос и ожидаем ответа от сервера
        response = yield AsyncHTTPClient().fetch(redirect_request)

        # Отправляем ответ клиенту
        self.write(json_decode(response.body))

        app_log.info(
            'Send response (body = {}) after redirect from {}'
            ''.format(response.body, redirect_url))
