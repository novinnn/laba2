import re
import requests
import unittest
import os
import tldextract


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

    # Поиск email-адресов@
    emails = re.findall(email_regex, content)

    # Фильтрация по доменам
    valid_emails = []
    for email in emails:
        domain = email.split('@')[1]
        # Проверка домена с помощью tldextract
        ext = tldextract.extract(domain)
        if ext.domain and ext.suffix:  # Проверка на существующий домен и TLD
            valid_emails.append(email)

    return valid_emails


# Пример использования
if __name__ == "__main__":
    user_input = input("Введите текст, URL или путь к файлу: ")
    mode = input("Выберите режим (string/file): ").strip().lower()

    if mode == "file":
        emails = find_emails(user_input, from_file=True)
    elif mode == "url":
        emails = find_emails(user_input, from_url=True)
    else:
        emails = find_emails(user_input)

    print("Найденные email-адреса:")
    for email in emails:
        print(email)


class TestFindEmails(unittest.TestCase):
    def test_find_emails_in_string(self):
        text = "Контакты: test.email@example.com, info@domain.org, fake-email@fake."
        result = find_emails(text)
        expected = ["test.email@example.com", "info@domain.org"]
        self.assertEqual(result, expected)

    def test_find_emails_in_file(self):
        temp_file = "test_file.txt"
        with open(temp_file, "w", encoding="utf-8") as file:
            file.write("Email: example@mail.com and admin@site.net.")
        try:
            result = find_emails(temp_file, from_file=True)
            expected = ["example@mail.com", "admin@site.net"]
            self.assertEqual(result, expected)
        finally:
            os.remove(temp_file)


if __name__ == "__main__":
    unittest.main()
