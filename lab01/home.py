import dotenv
import os
import streamlit as st

from API.DeepTranslate import DeepTranslate
from API.GoogleTranslate import GoogleTranslate
from API.TranslatePlus import TranslatePlus
from API.MicrosoftTranslate import MicrosoftTranslate

def on_change_text_field(**kwargs):
    translate_obj = kwargs.get('translate_obj')

    input_text = st.session_state.get("input_text")
    input_lang = st.session_state.get("input_lang")
    output_lang = st.session_state.get("output_lang")
    translate_text = translate_obj.translate(input_text, input_lang, output_lang)
    st.session_state["translate_text"] = translate_text

def on_change_services():
    st.session_state["translate_text"] = ""
    st.session_state["input_text"] = ""

def main():
    gt = GoogleTranslate(token=os.getenv("TOKEN"))
    dt = DeepTranslate(token=os.getenv("TOKEN"))
    tp = TranslatePlus(token=os.getenv("TOKEN"))
    mt = MicrosoftTranslate(token=os.getenv("TOKEN"))

    translate_object = {
        "Google Translate": gt,
        "Deep Translate": dt,
        "Translate Plus": tp,
        "Microsoft Translate": mt,
    }
    st.session_state.setdefault("translate_text", "")
    st.session_state.setdefault("input_text", "")

    st.markdown("""<style>
                              .st-emotion-cache-183lzff {
                                word-wrap: break-word;
                                white-space: normal;
                                }
                        </style>""", unsafe_allow_html=True)

    with st.sidebar:
        sb_translate = st.selectbox("Выберете переводчик", translate_object, key="service", on_change=on_change_services)
        if sb_translate is not None:
            list_language = translate_object[sb_translate].language()
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("Исходный язык:", list_language, key="input_lang", index=None)
            with col2:
                st.selectbox("Язык перевода:", [item for item in list_language if item != 'auto'], key="output_lang", index=None)

    st.header(st.session_state.get("service"))
    with st.container(border=True, height= 200):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Изначальный текст")
            st.text(st.session_state.get("input_text"))
        with col2:
            st.subheader("Перевод")
            st.text(st.session_state.get("translate_text"))

    st.write("")

    flag = st.session_state["input_lang"] is None or st.session_state["output_lang"] is None

    st.text_input("Введите текст для перевода:", "", key="input_text", placeholder="Введите текст здесь...", on_change=on_change_text_field, disabled = flag, kwargs={"translate_obj":translate_object[sb_translate]})


if __name__ == '__main__':
    dotenv.load_dotenv()
    main()