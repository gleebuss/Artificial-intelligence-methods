"""
Модуль предназначен для тестирования RuGPT, позволяя варьировать различные параметры
генерации текста и применять различные промты.
"""
import json

from transformers import GPT2LMHeadModel, GPT2Tokenizer, PreTrainedModel


def create_parameter_combinations() -> list[dict[str, str | int | bool]]:
    """
    Создает список комбинаций параметров для генерации текста с использованием языковой модели.

    Функция генерирует различные комбинации параметров генерации, учитывая вариации
    максимальной длины текста, режима выборки (sampling), и температуры.
    Если выборка включена (`do_sample=True`), то также используются параметры `temperature`,
    `top_k` и `top_p`. Для выборки `do_sample=False` эти параметры игнорируются.

    Returns:
        list[dict[str, str | int | bool]]: Список словарей, где
        каждый словарь содержит комбинацию параметров для генерации текста.
        Ключи словаря:
        - "max_length" (int): Максимальная длина сгенерированного текста.
        - "temperature" (float): Параметр температуры для модели
        (используется, если `do_sample=True`).
        - "do_sample" (bool): Флаг, указывающий, используется ли выборка.
        - "num_beams" (int): Количество лучей для beam search.
        - "num_return_sequences" (int): Количество возвращаемых последовательностей.
        - "no_repeat_ngram_size" (int): Размер n-грамм для предотвращения повторений.
        - "top_k" (int): Параметр для top-k sampling (используется, если `do_sample=True`).
        - "top_p" (float): Параметр для top-p sampling (используется, если `do_sample=True`).
    """
    max_length = [100, 150, 200]
    temperature = [0.8, 1.3, 2.0]
    do_sample = [True, False]
    num_beams = 3
    num_return_sequences = 1
    no_repeat_ngram_size = 2
    top_k = 20
    top_p = 0.8

    result = []

    for ml in max_length:
        for sample in do_sample:
            if sample:
                # Если do_sample=True, то используем temperature, top_k и top_p
                for temp in temperature:
                    param_dict = {
                        "max_length": ml,
                        "temperature": temp,
                        "do_sample": sample,
                        "num_beams": num_beams,
                        "num_return_sequences": num_return_sequences,
                        "no_repeat_ngram_size": no_repeat_ngram_size,
                        "top_k": top_k,
                        "top_p": top_p
                    }
                    result.append(param_dict)
            else:
                # Если do_sample=False, то игнорируем temperature, top_k и top_p
                param_dict = {
                    "max_length": ml,
                    "do_sample": sample,
                    "num_beams": num_beams,
                    "num_return_sequences": num_return_sequences,
                    "no_repeat_ngram_size": no_repeat_ngram_size
                }
                result.append(param_dict)

    return result


def save_results_to_json(results, file_name:str ="results.json") -> None:
    """
       Сохраняет результаты генерации текста в JSON-файл.

       Args:
           results (list[dict]): Список словарей, содержащих результаты генерации текста
           и параметры генерации.
           file_name (str, optional): Имя файла для сохранения результатов в формате JSON.
           По умолчанию используется "results.json".

       Returns:
           None:
    """
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)


def generate_text_from_params(params:dict[str, str | int | bool], model:PreTrainedModel,
                              tokenizer:bool|GPT2Tokenizer, prompt:str) -> str:
    """
    Генерирует текст на основе переданных параметров, модели и токенизатора.

    Args:
        params (dict[str, str | int | bool]): Словарь с параметрами генерации текста,
        такими как `max_length`, `temperature`, `do_sample` и т.д.
        model (PreTrainedModel): Предварительно обученная модель,
        которая используется для генерации текста.
        tokenizer (bool | GPT2Tokenizer): Токенизатор для преобразования текста в
        входные идентификаторы и декодирования результата.
        prompt (str): Начальный текст (промт) для генерации.

    Returns:
        str: Сгенерированный текст, полученный на основе модели и параметров генерации.
    """
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    if params.get("do_sample"):
        output = model.generate(input_ids,
                                max_length=params["max_length"],
                                temperature=params.get("temperature"),
                                do_sample=params["do_sample"],
                                num_beams=params["num_beams"],
                                num_return_sequences=params["num_return_sequences"],
                                no_repeat_ngram_size=params["no_repeat_ngram_size"],
                                top_k=params.get("top_k"),
                                top_p=params.get("top_p"))
    else:
        output = model.generate(input_ids,
                                max_length=params["max_length"],
                                do_sample=params["do_sample"],
                                num_beams=params["num_beams"],
                                num_return_sequences=params["num_return_sequences"],
                                no_repeat_ngram_size=params["no_repeat_ngram_size"])

    return tokenizer.decode(output[0], skip_special_tokens=True)


def main():
    """
    Основная функция для генерации текстов с использованием модели GPT-3
    и различных комбинаций параметров.
    """
    params_list = create_parameter_combinations()
    model_name = "sberbank-ai/rugpt3small_based_on_gpt2"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    prompts = [
        "Системы обнаружения мошенничества с кредитными картами приобретают все большее значение",
        "Чтобы защититься от кражи банковских карт",
        "Банковские карты имеют широкий спектр применения в различных областях"]

    results = []
    count = 0
    for params in params_list:
        tmp = {
            "Параметры": params
        }
        details_list = []
        for prompt in prompts:
            generated_text = generate_text_from_params(params=params, prompt=prompt,
                                                       model=model, tokenizer=tokenizer)
            detail = {
                "Текст": prompt,
                "Ответ": generated_text.replace("\xa0", " ")
            }
            details_list.append(detail)

        tmp["Детали"] = details_list
        results.append(tmp)
        count += 1
        print(f"Готов {count} из {len(params_list)}")

    save_results_to_json(results, file_name="generated_texts.json")


if __name__ == '__main__':
    main()
