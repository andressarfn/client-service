from src.shared.exceptions import CustomHttpException


class CreateClientEmailAlreadyExistsException(CustomHttpException):
    pass


class GetClientNotFoundException(CustomHttpException):
    pass


class UpdateClientNotFoundException(CustomHttpException):
    pass


class DeleteClientNotFoundException(CustomHttpException):
    pass
