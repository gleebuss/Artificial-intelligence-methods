from API.Model.BaseTranslate import BaseTranslate
import requests

class DeepTranslate(BaseTranslate):

    def __init__(self, token):
        self.token = token

    def translate(self, input_text, input_lang, output_lang) -> str:
        url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"

        payload_deep = {
            "q": input_text,
            "source": input_lang,
            "target": output_lang
        }

        headers_deep = {
            "x-rapidapi-key": self.token,
            "x-rapidapi-host": "deep-translate1.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload_deep, headers=headers_deep)
        result_json = response.json()
        if response.status_code == 200:
            output_text = result_json['data']['translations']['translatedText']
            return output_text
        return ""
    
    def language(self) -> list[str]:
        url = "https://deep-translate1.p.rapidapi.com/language/translate/v2/languages"

        headers = {
        "x-rapidapi-key": self.token,
        "x-rapidapi-host": "deep-translate1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        result_json = response.json()
        ans = list()
        if response.status_code == 200:
            for i in result_json['languages']:
                ans.append(i['language'])
        return ans