from django.core.exceptions import ValidationError
import os


def allow_only_images(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_exts = ["jpg", "png", "jpeg"]
    if not ext in valid_exts:
        raise ValidationError(
            "Image Unsupported allowed Extensions are: " + str(valid_exts)
        )
