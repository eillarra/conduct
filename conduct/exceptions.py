class ConductException(Exception):
    pass


class InvalidCredentials(ConductException, ValueError):
    """The wallet credentials were somehow invalid."""


class BadAuthException(ConductException):
    """Bad auth."""


class NotEnoughBalanceException(ConductException):
    """Not enough balance."""


class NotValidInvoiceException(ConductException):
    """Not a valid invoice."""


class ServerErrorException(ConductException):
    """General server error."""
