class NetrangeException(Exception):
    """Base exception for this module"""


class NetrangeCLIError(NetrangeException):
    """Generic exception for raising errors during CLI operation"""


class NetrangeParserError(NetrangeException):
    """Generic exception for raising errors during parser operation"""
