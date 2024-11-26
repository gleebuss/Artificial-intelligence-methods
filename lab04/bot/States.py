"""Модуль для определения состояний опроса и выбора модели в Telegram-боте."""
from aiogram.fsm.state import StatesGroup, State


class SurveyStates(StatesGroup):
    """
        Класс состояний для этапов опроса.

        Состояния:
            - order_frequency: Частота заказов (первый вопрос опроса).
            - order_process: Удобство процесса оформления заказа.
            - delivery_speed: Оценка скорости доставки.
            - delivery_quality: Оценка качества доставки.
            - overall_satisfaction: Оценка общей удовлетворенности.
            - additional_comments: Дополнительные комментарии пользователя.
        """
    order_frequency = State()
    order_process = State()
    delivery_speed = State()
    delivery_quality = State()
    overall_satisfaction = State()
    additional_comments = State()


class ModelSelectionStates(StatesGroup):
    """
        Класс состояний для выбора модели.

        Состояния:
            - model_selection: Выбор модели для генерации текста.
        """
    model_selection = State()
