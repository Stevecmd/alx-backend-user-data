#!/usr/bin/env python3
"""
Module for filtering sensitive information from log messages
"""
import re
import logging


def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated
    Args:
        fields: list of strings representing fields to obfuscate
        redaction: string to replace sensitive info with
        message: string representing the log line
        separator: string representing the character separating fields
    Returns:
        The obfuscated log message
    """
    pattern = f'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, f'\\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: tuple):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)
