"""Модуль для работы с моделями (например, GPT, Llama)"""
import json

from transformers import AutoTokenizer, LlamaForCausalLM, AutoModelForCausalLM


class BaseModel:
    def __init__(self, model_name: str, config_file: str = "./Models/model_params.json"):
        """Инициализация модели: загрузка токенизатора и модели.
        Args:
            model_name (str): Имя модели (например, "ai-forever/rugpt3medium_based_on_gpt2" или "Vikhrmodels/Vikhr-Llama-3.2-1B-Instruct").
            config_file (str): Путь к конфигурационному файлу для загрузки параметров модели (по умолчанию "./Models/model_params.json")."""
        self.model_name = model_name

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        if "Llama" in model_name.lower():
            self.model = LlamaForCausalLM.from_pretrained(self.model_name, device_map="sequential")
        else:
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name, device_map="sequential")

        self.model_params = self.load_model_params(config_file)

    def load_model_params(self, config_file: str) -> dict:
        """
        Загрузка параметров модели из конфигурационного файла.

        Читает конфигурационный файл JSON и извлекает параметры для конкретной модели.
        Если файл не существует или возникает ошибка, возвращается пустой словарь.

        Args:
            config_file (str): Путь к JSON-файлу с параметрами модели (по умолчанию "./Models/model_params.json").

        Returns:
            dict: Параметры для конкретной модели, извлеченные из файла. Если произошла ошибка, возвращается пустой словарь.
        """
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                params = json.load(f).get(self.model_name, {})
            return params
        except Exception as e:
            print(f"Ошибка загрузки параметров модели: {e}")
            return {}

    def generate_response(self, prompt: str) -> str:
        """
        Генерация ответа с использованием модели.
        Args:
            prompt (str): Текстовая подсказка, на основе которой будет сгенерирован ответ.

        Returns:
            str: Сгенерированный ответ, который декодируется из тензора в текст."""
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

        generate_ids = self.model.generate(
            inputs.input_ids,
            **self.model_params
        )

        output = self.tokenizer.batch_decode(generate_ids, skip_special_tokens=True)[0]
        return output
