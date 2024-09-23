from abc import ABC, abstractmethod

class BaseTranslate(ABC):

    @abstractmethod
    def translate(self, input_text, input_lang, output_lang) -> str:
        pass

    @abstractmethod
    def language(self) -> list[str]:
        pass
