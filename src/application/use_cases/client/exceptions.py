from src.shared.exceptions import CustomHttpException


class ClientEmailAlreadyExistsException(CustomHttpException):
    pass


class ClientNotFoundException(CustomHttpException):
    pass
