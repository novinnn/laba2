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

# Пример использования
if __name__ == "__main__":
    user_input = input("Введите текст, URL или путь к файлу: ")
    mode = input("Выберите режим (string/file/url): ").strip().lower()

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
        with open("test_file.txt", "w", encoding="utf-8") as file:
            file.write("Email: example@mail.com and admin@site.net.")
        result = find_emails("test_file.txt", from_file=True)
        expected = ["example@mail.com", "admin@site.net"]
        self.assertEqual(result, expected)

    def test_find_emails_on_webpage(self):
        url = "https://www.example.com"
        mock_html = "<html><body>Email: contact@website.com</body></html>"

        # Мокирование запроса
        def mock_get(*args, **kwargs):
            class MockResponse:
                def __init__(self, text):
                    self.text = text

                def raise_for_status(self):
                    pass

            return MockResponse(mock_html)

        requests.get = mock_get
        result = find_emails(url, from_url=True)
        expected = ["contact@website.com"]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
