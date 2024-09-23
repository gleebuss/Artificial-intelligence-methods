from API.Model.BaseTranslate import BaseTranslate
import requests


class GoogleTranslate(BaseTranslate):
    
    def __init__(self, token):
        self.token = token

    def translate(self, input_text, input_lang, output_lang) -> str:
        url = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"
        payload_google = {
            "from": input_lang,
            "to": output_lang,
            "text": input_text
        }

        headers_google = {
            "x-rapidapi-key": self.token,
            "x-rapidapi-host": "google-translate113.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload_google, headers=headers_google)
        if response.status_code == 200:
            result_json = response.json()
            output = result_json['trans']
            return output
        return ""
    
    def language(self) -> list[str]:
        url = "https://google-translate113.p.rapidapi.com/api/v1/translator/support-languages"

        headers = {
            "x-rapidapi-key": "d7ca69bf5fmshed633ddb4e6fde7p184a9djsnad8a97cba009",
            "x-rapidapi-host": "google-translate113.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        ans = list()
        if response.status_code == 200:
            result_json = response.json()
            for i in result_json:
                ans.append(i['code'])
        return ans