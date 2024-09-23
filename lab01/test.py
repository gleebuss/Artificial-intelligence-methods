import requests
import json
import os
from bs4 import BeautifulSoup
import dotenv

from API.DeepTranslate import DeepTranslate
from API.GoogleTranslate import GoogleTranslate
from API.MicrosoftTranslate import MicrosoftTranslate
from API.TranslatePlus import TranslatePlus


def translate(text: str, input_lang: str = "en", output_lang: str = "ru") -> dict[str, str]:
    gt = GoogleTranslate(token=os.getenv("TOKEN"))
    dt = DeepTranslate(token=os.getenv("TOKEN"))
    tp = TranslatePlus(token=os.getenv("TOKEN"))
    mt = MicrosoftTranslate(token=os.getenv("TOKEN"))

    translation = {
        "GoogleTranslate": gt.translate(text, input_lang=input_lang, output_lang=output_lang),
        "DeepTranslate": dt.translate(text, input_lang=input_lang, output_lang=output_lang),
        "TranslatePlus": tp.translate(text, input_lang=input_lang, output_lang=output_lang),
        "MicrosoftTranslate": mt.translate(text, input_lang=input_lang, output_lang=output_lang),
    }

    return translation



def main():
    main_url = "https://www.native-english.ru/idioms"
    url = "https://www.native-english.ru/"
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, "html.parser")

    div_idioms = soup.find('div', class_='stack__primary')
    li_elements = div_idioms.find_all('li')
    ans = []
    for i in li_elements:
        idiom, desc = i.text.strip(), i.find("meta").get("content")
        link = i.find('a').get("href")

        response = requests.get(f"{url}/{link}")
        soup = BeautifulSoup(response.text, "html.parser")
        div_sentences = soup.find('div', class_='example dtext')
        sentences = div_sentences.text.strip()

        tmp = {
            "idiom": idiom,
            "desc": desc,
            "sentence": sentences,
            "translation": translate(sentences),
        }

        ans.append(tmp)

    with open('idioms.json', 'w', encoding='utf-8') as f:
        json.dump(ans, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    dotenv.load_dotenv()
    main()