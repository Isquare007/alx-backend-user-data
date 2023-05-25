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
        message = re.sub(f'{field}=.*?(?={separator})',
                         f'{field}={redaction}', message)
    return message
