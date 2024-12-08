import json

from tornado import gen, web
from tornado.escape import json_decode
from tornado.log import app_log

from server.validate import validate_status_request


class StatusHandler(web.RequestHandler):
    """Обработчик получения статуса устройства."""

    def prepare(self):
        try:
            self.body = json_decode(self.request.body)
        except (TypeError, json.JSONDecodeError) as error:
            app_log.error("Error %s" % error)
            raise web.HTTPError(400, error)

    @gen.coroutine
    def post(self):
        is_validate, reason = validate_status_request(self.body)

        if not is_validate:
            self.write({
                'result': 'Validation error',
                'message': reason
            })
            app_log.info(
                'Request {} validation error: {}'.format(
                    self.body['request_id'], reason))

            raise gen.Return()

        yield gen.sleep(2)

        self.write({
            'device_id': self.body['device_id'],
            'request_id': self.body['request_id'],
            'result': 'OK'
        })

        app_log.info(
            'Response to request {} ({}) from {}'.format(
                self.body['request_id'], self.body['device_id'],
                self.request.host))
