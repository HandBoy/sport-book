from http import HTTPStatus

import werkzeug
from flask import jsonify


class ApiSportNotFound(werkzeug.exceptions.HTTPException):
    code = 404
    description = "Sport not found"


class APISportBookException(Exception):
    def __init__(self, message, code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if code:
            self.code = code
        self.payload = payload

    def to_dict(self):
        data = dict(self.payload or ())
        data["message"] = self.message
        data["code"] = self.status_code
        return data


class ApiEventValidationError(APISportBookException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY


def handle_api_exceptions(app):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    @app.errorhandler(ApiEventValidationError)
    def handle_event_validator_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
