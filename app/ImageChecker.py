# Django
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.conf import settings

def check_image(image):
    """Проверка фото по размеру и формату"""
    max_upload_size_kb = settings.MAX_IMAGE_SIZE_MB * 2**20
    try:
        if image.content_type in settings.IMAGE_TYPE.values():
            if image.size > max_upload_size_kb:
                raise forms.ValidationError(
                    ('Please keep filesize under %s MB. Current filesize %s') %
                    (settings.MAX_IMAGE_SIZE_MB, filesizeformat(image.size))
                )
        else:
            raise forms.ValidationError(
                ('Тип файла не поддерживается. Загрузите %s') %
                ([key for key in settings.IMAGE_TYPE])
            )
    except AttributeError:
        pass
    return image
