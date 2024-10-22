"""
Модуль для логирования чатов в JSON файл.

Этот модуль содержит класс ChatLogger, который позволяет сохранять
данные чатов в формате JSON.
"""
import json


class ChatLogger:
    """
    Класс для логирования чатов в JSON файл.
    """

    def __init__(self, filename:str = "logger.json") -> None:
        """
        Инициализация экземпляра класса ChatLogger.

        Args:
            filename (str): Имя файла для записи JSON данных.
            По умолчанию используется "logger.json".
        Returns:
            None
        """

        self.filename = filename

    def save_to_file(self, data:list[dict[str:str]]) -> None:
        """
        Сохраняет массив словарей в JSON файл.

        Args:
            data (list[dict[str, str]]): Список словарей, содержащих данные чатов для записи в файл.
        """

        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
