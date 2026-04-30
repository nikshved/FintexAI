class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class BadRequestError(Exception):
    pass


class DatabaseError(Exception):
    pass


class InternalServerError(Exception):
    pass
