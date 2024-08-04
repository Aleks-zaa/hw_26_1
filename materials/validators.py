from rest_framework.serializers import ValidationError


class UrlValidator:
    """ Проверка  youtube.com"""
    def __init__(self, field):
        self.field = field

    def __call__(self, url):
        tmp_url = dict(url).get(self.field)
        if not(tmp_url is None or 'youtube.com' in tmp_url):
            raise ValidationError('Ссылка не может использоваться')



# from rest_framework.serializers import ValidationError
#
# url_word = ['youtube.com']
#
#
# def url_validator(value):
#     if value.lower() not in url_word:
#         raise ValidationError('Некорректная ссылка.')
