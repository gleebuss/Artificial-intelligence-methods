from API.Model.BaseTranslate import BaseTranslate
import requests

class MicrosoftTranslate(BaseTranslate):
    def __init__(self, token):
        self.token = token

    def translate(self, input_text, input_lang, output_lang) -> str:
        url = "https://microsoft-translator-text-api3.p.rapidapi.com/translate"

        querystring = {"to": output_lang, "from": input_lang, "textType": "plain"}

        payload = [{"text": input_text}]
        headers = {
            "x-rapidapi-key": self.token,
            "x-rapidapi-host": "microsoft-translator-text-api3.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers, params=querystring)
        if response.status_code == 200:
            result_json = response.json()
            ans = result_json[0]["translations"][0]['text']
            return ans
        return ""



    def language(self) -> list[str]:
        url = "https://microsoft-translator-text-api3.p.rapidapi.com/languages"

        headers = {
            "x-rapidapi-key": "d7ca69bf5fmshed633ddb4e6fde7p184a9djsnad8a97cba009",
            "x-rapidapi-host": "microsoft-translator-text-api3.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        ans = list()
        if response.status_code == 200:
            result_json = response.json()
            ans = list(result_json["translation"].keys())
        return ans
