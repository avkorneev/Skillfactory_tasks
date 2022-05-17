from django import template
import re

register = template.Library()
# Наш милый список бранных слов
OBSCENE_WORDS = {
    'demons': '****s',
    'god': '***',
    'satan': '****n',
    'бог': 'Б-г'
}


@register.filter()
def obscene(value):
    text = str(value)
    for i in OBSCENE_WORDS.keys(): #поиск по всем словам
        if i in text.lower():   #текст перекидываем в нижний регистр
            # честно стырено со StackOverFlow. Это нужно, чтобы замена не чувствовала регистры.
            insensitive_word = re.compile(re.escape(i), re.IGNORECASE)
            text = insensitive_word.sub(OBSCENE_WORDS[i], text) # Готово, мы нашли и заменили нехорошие слова вне
            # зависимости от регистра, не изменив при этом регистр остального текста
    return text
