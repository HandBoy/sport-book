import werkzeug


class ApiSportNotFound(werkzeug.exceptions.HTTPException):
    code = 404
    description = 'Sport not found'
