import io

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile


class WEBPFieldFile(ImageFieldFile):
    """
    Convertor to WEBP
    """

    def save(self, name, content, save=True):
        content.file.seek(0)
        image = Image.open(content.file)
        image_bytes = io.BytesIO()
        image.save(fp=image_bytes, format="WEBP")
        image_content_file = ContentFile(content=image_bytes.getvalue())  # Getting data from BytesIO object
        super().save(name, image_content_file, save)


class WEBPField(models.ImageField):
    """
    Custom image field(CONVERTOR)
    """
    attr_class = WEBPFieldFile
