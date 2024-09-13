import re
import json
from django import template

register = template.Library()
with open('news/templatetags/filter_words.json', 'r', encoding='utf-8') as file: WORDS = json.load(file)


@register.filter()
def censor(text):
    """
    Фильтр censor, который заменяет буквы нежелательных слов в заголовках и текстах статей на символ «*».
    value: значение, к которому нужно применить фильтр
    code: код валюты
    """

    for word in WORDS['words']:
        text = re.sub(f'\\b{word}\\b', f"{word[0]}{word[1:].__len__() * '*'}", text, flags=re.I)
    return text
