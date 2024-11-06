#!/usr/bin/env python3
"""
Module for filtering sensitive information from log messages
"""
import re


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
