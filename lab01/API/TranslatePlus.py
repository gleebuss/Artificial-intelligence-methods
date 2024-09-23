from API.Model.BaseTranslate import BaseTranslate
import requests


class TranslatePlus(BaseTranslate):

    def __init__(self, token):
        self.token = token

    def translate(self, input_text, input_lang, output_lang) -> str:
        url = "https://translate-plus.p.rapidapi.com/translate"
        payload_plus = {
            "text": input_text,
            "source": input_lang,
            "target": output_lang
        }

        headers_plus = {
            "x-rapidapi-key": self.token,
            "x-rapidapi-host": "translate-plus.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload_plus, headers=headers_plus)
        if response.status_code == 200:
            result_json = response.json()
            output = result_json['translations']['translation']
            return output
        return ""

    def language(self) -> list[str]:
        url = "https://translate-plus.p.rapidapi.com/"

        headers = {
            "x-rapidapi-key": self.token,
            "x-rapidapi-host": "translate-plus.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        ans = list()
        if response.status_code == 200:
            result_json = response.json()
            ans = list(result_json['supported_languages'].values())
        return ans
