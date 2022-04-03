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
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY


class ApiEventNotFound(werkzeug.exceptions.HTTPException):
    code = HTTPStatus.NOT_FOUND
    description = "Event not found"


class ApiSelectionValidationError(APISportBookException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY


class ApiSelectionFilterError(APISportBookException):
    code = HTTPStatus.BAD_REQUEST
    status_code = HTTPStatus.BAD_REQUEST


class ApiSelectionNotFound(werkzeug.exceptions.HTTPException):
    code = HTTPStatus.NOT_FOUND
    description = "Selection not found"


def handle_api_exceptions(app):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    @app.errorhandler(ApiEventValidationError)
    def handle_event_validator_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(ApiSelectionValidationError)
    def handle_selection_validator_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(ApiSelectionFilterError)
    def handle_selection_filter_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(ApiSelectionNotFound)
    def handle_selection_not_found_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
