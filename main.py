import sys
import os
import openai
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup


load_dotenv()
# Ваш API KEY от OpenAI.
openai.api_key = os.getenv("OPENAI_API_KEY")

DEFAULT_URL = 'https://kino.kz/'


class WebSiteAssistant:
    """
    Класс для создания ассистента, который изучает текст с целью составить краткое резюме из его основных идей на русском языке.
    """

    def __init__(self, url: str) -> None:
        """
        Конструктор класса Assistant.

        Args:
            url (str): URL-адрес веб-страницы для парсинга.
        """
        self.url = url

    @property
    def summary(self) -> str:
        """Метод для создания краткого резюме из основных идей веб-страницы."""
        parsed_data = self._parse_data(self._get_html())
        summary = self._send_message_to_openai(parsed_data)
        return summary

    def _send_message_to_openai(self, cleaned_html_text: str) -> str:
        """
        Метод для отправки очищенного текста веб-страницы модели OpenAI.

        Args:
            cleaned_html_text (str): Очищенный текст веб-страницы.
        """
        messages = [
            {
                "role": "system", "content": "Ты - асистент, который изучает текст с целью составить краткое резюме из его основных идей на русском языке"
            },
        ]
        messages.append({"role": "user", "content": cleaned_html_text})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages)
        return response.choices[0].message.content

    def _get_html(self) -> bytes:
        """
        Внутренний метод для получения HTML-кода веб-страницы.
        """
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }
        response = requests.get(self.url, headers=headers)
        return response.content

    def _parse_data(self, html: str) -> str:
        """
        Внутренний метод для парсинга HTML-кода веб-страницы.

        Args:
            html (str): HTML-код веб-страницы.

        Returns:
            str: Текстовое содержимое веб-страницы без тегов и лишних пробелов.
        """
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text().strip()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        if not url.startswith('http'):
            url = 'https://' + url
    else:
        url = DEFAULT_URL
    assistant = WebSiteAssistant(url)
    print(assistant.summary)
