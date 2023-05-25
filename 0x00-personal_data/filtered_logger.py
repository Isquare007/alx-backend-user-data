#!/usr/bin/env python3
"""filtered_logger"""

import logging
import mysql.connector
from os import environ
import re
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """filters the person data from a message

    Args:
        fields (list): a list of strings representing
        all fields to obfuscate
        redaction (str): a string representing by what
        the field will be obfuscated
        message (str): a string representing the log line
        separator (str): a string representing by whic
        character is separating all
        fields in the log line (message)
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """set up a logger with formatter, streamhandler and level"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """uses my-sql connector to connect to a db"""
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    db_connect = mysql.connector.connection.MySQLConnection(
        user=username, password=password, host=host, database=db_name)

    return db_connect


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        message = filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR)
        record.msg = message
        return super().format(record)


def main():
    """main function; fetches data
    from a db and hashes the PII"""
    db_connector = get_db()
    cursor = db_connector.cursor()
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    logger = get_logger()
    field_names = [i[0] for i in cursor.description]

    for row in rows:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db_connector.close()


if __name__ == "__main__":
    main()
