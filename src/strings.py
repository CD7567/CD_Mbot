"""This file contains string sources of CD_MBot"""


class StringsLang:
    str_greeting = ''
    str_greeting_lang = ''

    str_search_request = ''
    str_search_start = ''
    str_search_end = ''
    str_search = ''

    str_error_internal = ''
    str_error_internal_start = ''
    str_error_not_found = ''
    str_error_not_found_help = ''

    str_help = ''
    str_help_content = ''

    str_lang = ''
    str_lang_choose = ''

    str_en = '\U0001F1EC\U0001F1E7'
    str_ru = '\U0001F1F7\U0001F1FA'


class StringsRu(StringsLang):
    str_greeting = 'Привет! \U0000270B \nЯ умею искать музыку на Youtube \U0001F60E \nДавай выберем язык'
    str_greeting_lang = 'Замечательно \U0001F609 \nДавай начнем!'

    str_search_request = '\U0001F50D Напиши название трека, который хочешь найти'
    str_search_start = '\U0001F50D Уже ищу нужный тебе трек \nПодожди немного... \U0001f4a4'
    str_search_end = '\U00002705 Нашел нужный тебе трек \nСпасибо за твой интерес \U0001F49E'
    str_search = '\U0001F50D Искать'

    str_error_internal = 'Что-то пошло не так... \U0001F614 \nВозвращаемся в основное меню'
    str_error_internal_start = 'Что-то пошло не так... \U0001F614'
    str_error_not_found = 'Я не понял твою команду \U0001F614'
    str_error_not_found_help = 'Я не понял твою команду \U0001F614 \nКоманды можно посмотреть по /help'

    str_help = '\U00002753 Помощь'
    str_help_content = '/help -- помощь по командам \n/search -- искать трек \n/lang -- изменить язык'

    str_lang = '\U0001F1F7\U0001F1FA Язык'
    str_lang_choose = 'Давай выберем язык'


class StringsEn(StringsLang):
    str_greeting = 'Hello! \U0000270B \nI can look for music on Youtube \U0001F60E \nLet\'s choose a language'
    str_greeting_lang = 'Great \U0001F609 \nLet\'s start!'

    str_search_request = '\U0001F50D Type name of the track you\'re looking for'
    str_search_start = '\U0001F50D Looking for a track \nWait for a while... \U0001f4a4'
    str_search_end = '\U00002705 I found the track for you \nThanks for your interest \U0001F49E'
    str_search = '\U0001F50D Search'

    str_error_internal = 'Something went wrong... \U0001F614 \nReturning to main menu...'
    str_error_internal_start = 'Something went wrong... \U0001F614'
    str_error_not_found = 'I didn\'t understand you \U0001F614'
    str_error_not_found_help = 'I didn\'t understand you \U0001F614 \nYou can check out command by /help'

    str_help = '\U00002753 Help'
    str_help_content = '/help -- command help \n/search -- look for a track \n/lang -- change language'

    str_lang = '\U0001F1EC\U0001F1E7 Language'
    str_lang_choose = 'Let\'s choose a language'


locales = {StringsLang.str_en: StringsEn, StringsLang.str_ru: StringsRu}
