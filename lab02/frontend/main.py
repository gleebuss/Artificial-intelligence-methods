"""
Этот модуль является точкой входа в программу.
"""
import os
import sys

import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Model.ru_gpt3 import RuGPT3 # pylint: disable=import-error, wrong-import-position
from ChatLogger.chat_logger import ChatLogger # pylint: disable=import-error, wrong-import-position


def main():
    """
    Основная функция, запускающая чат с моделью RuGPT3Small.

    Эта функция инициализирует модель, отображает информацию о ней в боковой панели,
    обрабатывает ввод пользователя и генерирует ответы от модели.

    Взаимодействие с пользователем происходит через интерфейс Streamlit.
    """
    gpt = RuGPT3()
    logger = ChatLogger()

    st.header(f'Чат с {gpt.name}')

    with st.sidebar:
        st.subheader("О модели")
        st.text(f'Название: {gpt.name}')
        st.text(f'Путь к модели: {gpt.model_path}')
        st.text(f'Путь к токенизатору: {gpt.tokenizer_path}')

        st.subheader("Параметры модели")
        st.text(f'min_length: {gpt.min_length}')
        st.text(f'max_length: {gpt.max_length}')
        st.text(f'num_beams: {gpt.num_beams}')
        st.text(f'num_return_sequences: {gpt.num_return_sequences}')
        st.text(f'no_repeat_ngram_size: {gpt.no_repeat_ngram_size}')
        st.text(f'do_sample: {gpt.do_sample}')
        st.text(f'top_k: {gpt.top_k}')
        st.text(f'top_p: {gpt.top_p}')
        st.text(f'temperature: {gpt.temperature}')

        if st.button("Сохранить чат"):
            logger.save_to_file(st.session_state.messages)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Введите текст"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response = gpt.generate_text(prompt)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
