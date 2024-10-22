"""
Модуль для работы с моделью RuGPT-3.

Этот модуль содержит класс RuGPT3, который предоставляет интерфейс
для генерации текстов на русском языке с использованием модели RuGPT-3.
"""
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import yaml


class RuGPT3:
    """
    Класс, представляющий небольшую модель RuGPT-3 для генерации текстов на русском языке.

    Этот класс используется для взаимодействия с моделью RuGPT-3, которая способна генерировать
    ответы на основе введенного текста.

    Основная функция класса включает генерацию текста на основе входного текста от пользователя.
    """

    def __init__(self, config_path: str = "./Model/config.yaml") -> None:
        """
        Создает и инициализирует экземпляр класса RuGPT3.

        Args:
            config_path (str): Путь к конфигурационному файлу.
            По умолчанию используется "./Model/config.yaml".

        Returns:
            None
        """

        # Загрузка конфиг файла
        with open(config_path, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)

        self.name = self.config['model']['name']

        # Извлекаем параметры модели
        self.tokenizer_path = self.config['model']['tokenizer_path']
        self.model_path = self.config['model']['model_path']
        self.max_length = self.config['generation_params']['max_length']
        self.min_length = self.config['generation_params']['min_length']
        self.num_beams = self.config['generation_params']['num_beams']
        self.num_return_sequences = self.config['generation_params']['num_return_sequences']
        self.no_repeat_ngram_size = self.config['generation_params']['no_repeat_ngram_size']
        self.do_sample = self.config['generation_params']['do_sample']
        self.top_k = self.config['generation_params']['top_k']
        self.top_p = self.config['generation_params']['top_p']
        self.temperature = self.config['generation_params']['temperature']

        # Загружаем модель и токенизатор
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.tokenizer_path)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_path)

    def generate_text(self, input_text: str) -> str:
        """
        Генерирует ответ с помощью модели GPT на основе переданного текста.
        Args:
            input_text (str): Пользовательский текст
        Returns:
            str: Сгенерированный ответ от модели GPT
        """

        # Токенизация входного текста
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt")

        # Генерация текста с параметрами
        output = self.model.generate(
            input_ids,
            max_length=self.max_length,
            min_length=self.min_length,
            num_beams=self.num_beams,
            num_return_sequences=self.num_return_sequences,
            no_repeat_ngram_size=self.no_repeat_ngram_size,
            do_sample=self.do_sample,
            top_k=self.top_k,
            top_p=self.top_p,
            temperature=self.temperature,
        )

        # Декодируем и возвращаем сгенерированный текст
        return self.tokenizer.decode(output[0], skip_special_tokens=True)
