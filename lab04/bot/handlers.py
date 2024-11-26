"""Модуль для обработки шагов опроса и управления выбором модели в Telegram-боте."""
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram import Router

from Models.BaseModel import BaseModel
from bot.States import SurveyStates, ModelSelectionStates
from bot.utils import load_survey_data, create_buttons

router = Router()
model: BaseModel = None
survey_data = load_survey_data()


async def handle_survey_step(message: types.Message, state: FSMContext, step: str):
    """
        Обрабатывает текущий шаг опроса, выводя текст и кнопки для пользователя.
        Также генерирует ответ с помощью модели, если это указано в данных шага.

        Args:
            message (types.Message): Сообщение от пользователя.
            state (FSMContext): Контекст состояния FSM.
            step (str): Ключ для шага опроса в данных опроса.
        """
    text = survey_data[step].get("text", "Ошибка: нет текста для этого шага")
    buttons = survey_data[step].get("buttons", [])
    prompt = survey_data[step].get("prompt", None)

    if prompt and model:
        text = model.generate_response(prompt)

    await message.answer(
        text,
        reply_markup=ReplyKeyboardRemove() if not buttons else create_buttons(buttons)
    )


@router.message(Command('model'))
async def choose_model(message: types.Message, state: FSMContext):
    """
        Обрабатывает команду /model для выбора модели.
        Args:
            message (types.Message): Сообщение от пользователя.
            state (FSMContext): Контекст состояния FSM.
        """
    model_buttons = ["ai-forever/rugpt3medium_based_on_gpt2", "Vikhrmodels/Vikhr-Llama-3.2-1B-Instruct"]
    markup = create_buttons(model_buttons)
    text = "Выберите модель"

    await message.answer(text, reply_markup=markup)
    await state.set_state(ModelSelectionStates.model_selection)


@router.message(ModelSelectionStates.model_selection)
async def model_selection(message: types.Message, state: FSMContext):
    """
        Обрабатывает выбор модели и устанавливает её для использования.
        Args:
            message (types.Message): Сообщение от пользователя.
            state (FSMContext): Контекст состояния FSM.
        """
    global model
    model = BaseModel(message.text.lower())

    await message.answer(
        f"Вы выбрали модель - {message.text.lower()}",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()


@router.message(Command('start'), StateFilter(None))
async def start_survey(message: types.Message, state: FSMContext):
    """
        Начинает опрос и задает вопрос о частоте заказов.
        Args:
            message (types.Message): Сообщение от пользователя.
            state (FSMContext): Контекст состояния FSM.
        """
    await handle_survey_step(message, state, "intro")
    await state.set_state(SurveyStates.order_frequency)
    await handle_survey_step(message, state, "order_frequency")


@router.message(SurveyStates.order_frequency)
async def process_order_frequency(message: types.Message, state: FSMContext):
    """
        Обрабатывает ответ на вопрос и переходит к следующему вопросу об удобстве оформления заказа.
        Args:
            message (types.Message): Сообщение от пользователя.
            state (FSMContext): Контекст состояния FSM."""
    await state.update_data(order_frequency=message.text.lower())
    await state.set_state(SurveyStates.order_process)
    await handle_survey_step(message, state, "order_process")


@router.message(SurveyStates.order_process)
async def process_order_process(message: types.Message, state: FSMContext):
    """
        Обрабатывает ответ на вопрос и переходит к следующему вопросу о скорости доставки.
        Args:
            message (types.Message): Сообщение от пользователя.
            state (FSMContext): Контекст состояния FSM."""
    await state.update_data(order_process=message.text.lower())
    await state.set_state(SurveyStates.delivery_speed)
    await handle_survey_step(message, state, "delivery_speed")


@router.message(SurveyStates.delivery_speed)
async def process_delivery_speed(message: types.Message, state: FSMContext):
    """
        Обрабатывает ответ на вопрос и переходит к следующему вопросу об состоянии товаров после доставки.
        Args:
            message (types.Message): Сообщение от пользователя.
            state (FSMContext): Контекст состояния FSM."""

    await state.update_data(delivery_speed=message.text.lower())
    await state.set_state(SurveyStates.delivery_quality)
    await handle_survey_step(message, state, "delivery_quality")


@router.message(SurveyStates.delivery_quality)
async def process_delivery_quality(message: types.Message, state: FSMContext):
    """
        Обрабатывает ответ на вопрос и переходит к следующему вопросу о качестве доставки
        Args:
            message (types.Message): Сообщение от пользователя.
            state (FSMContext): Контекст состояния FSM."""
    await state.update_data(delivery_quality=message.text.lower())
    await state.set_state(SurveyStates.overall_satisfaction)
    await handle_survey_step(message, state, "overall_satisfaction")


@router.message(SurveyStates.overall_satisfaction)
async def process_overall_satisfaction(message: types.Message, state: FSMContext):
    """
        Обрабатывает ответ на вопрос и переходит к следующему вопросу о дополнительных комментариях.
        Args:
            message (types.Message): Сообщение от пользователя.
            state (FSMContext): Контекст состояния FSM."""
    await state.update_data(overall_satisfaction=message.text.lower())
    await state.set_state(SurveyStates.additional_comments)
    await handle_survey_step(message, state, "additional_comments")


@router.message(SurveyStates.additional_comments)
async def process_additional_comments(message: types.Message, state: FSMContext):
    """
        Обрабатывает дополнительные комментарии пользователя и завершает опрос.
        Args:
            message (types.Message): Сообщение от пользователя.
            state (FSMContext): Контекст состояния FSM."""
    await state.update_data(additional_comments=message.text.lower())
    user_data = await state.get_data()

    await message.answer(
        "Вот ваши ответы:\n\n"
        f"Частота заказов: {user_data['order_frequency']}\n"
        f"Удобство оформления: {user_data['order_process']}\n"
        f"Скорость доставки: {user_data['delivery_speed']}\n"
        f"Качество доставки: {user_data['delivery_quality']}\n"
        f"Общая удовлетворенность: {user_data['overall_satisfaction']}\n"
        f"Комментарии: {user_data['additional_comments']}")
    await handle_survey_step(message, state, "thank_you")
    await state.clear()
