import re
import requests
import unittest


def find_emails(source, from_file=False, from_url=False):

    # Регулярное выражение для email-адресов
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    if from_file:
        # Чтение данных из файла
        with open(source, 'r', encoding='utf-8') as file:
            content = file.read()
    elif from_url:
        # Чтение данных с веб-страницы
        response = requests.get(source)
        response.raise_for_status()
        content = response.text
    else:
        # Работа с переданной строкой
        content = source

    # Поиск email-адресов
    emails = re.findall(email_regex, content)
    return emails

