#!/usr/bin/env python3
"""
Module for filtering sensitive information from log messages
"""
import re
import logging
import mysql.connector
import os


# PII fields to be redacted
# PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


def get_logger() -> logging.Logger:
    """
    Returns a Logger object for handling
    Personal Identifiable Information (PII)
    Returns:
        logging.Logger: Logger object
    """
    # Create logger
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    # Add handler to logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the MySQL database
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', 'root')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: tuple):
        """Initializing the variables.

        Args:
            fields

        Returns:
            None.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the specified log record, redacting sensitive information.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with sensitive data redacted.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def main():
    """
    Main function to retrieve and display filtered user data
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    logger = get_logger()

    fields = ['name', 'email', 'phone', 'ssn', 'password', 'ip',
              'last_login', 'user_agent']

    for row in cursor:
        message_parts = []
        for i in range(len(fields)):
            field = fields[i]
            value = row[i]
            message_parts.append(f"{field}={value}")
        message = '; '.join(message_parts)
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
