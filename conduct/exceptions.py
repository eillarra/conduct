class ConductException(Exception):
    pass


class BadRequestException(ConductException, ValueError):
    """The request was somehow invalid."""


class BadAuthException(ConductException, ValueError):
    """The wallet credentials were somehow invalid."""


class InsufficientPermissionsException(ConductException, ValueError):
    """Insuficient permissions."""


class InvalidInvoiceException(ConductException, ValueError):
    """Not a valid invoice."""


class PaymentException(ConductException):
    """An error ocurred when trying to pay an invoice."""


class NotEnoughBalanceException(ConductException):
    """Not enough balance."""


class NotFoundException(ConductException):
    """The requested resource was not found."""


class LndRoutingException(ConductException):
    """LND route not found, or bad partners."""


class ServerErrorException(ConductException):
    """General server error."""
