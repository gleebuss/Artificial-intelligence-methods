"""
Модуль для создания кнопок Telegram и загрузки данных опроса.
"""
import json

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def create_buttons(options: list) -> ReplyKeyboardMarkup:
    """
        Создает клавиатуру Telegram с кнопками на основе переданных опций.

        Args:
            options (list): Список строк, который будет использоваться для создания кнопок.

        Returns:
            ReplyKeyboardMarkup: Объект клавиатуры Telegram с кнопками, соответствующими списку опций.
    """
    buttons = [[KeyboardButton(text=option, callback_data=option) for option in options]]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons)
    return keyboard


def load_survey_data(survey_path: str = "./bot/survey_data.json") -> dict:
    """
        Загружает данные опроса из JSON файла.

        Args:
            survey_path (str): Путь к JSON файлу с данными опроса. По умолчанию используется
                               путь "./bot/survey_data.json".
    """
    with open(survey_path, "r", encoding="utf-8") as f:
        return json.load(f)