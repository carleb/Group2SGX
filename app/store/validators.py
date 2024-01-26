from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class FileNameLengthValidator:
    def __init__(self, max_length=255):
        self.max_length = max_length

    def __call__(self, value):
        if len(value.name) > self.max_length:
            raise ValidationError(f"File name cannot be longer than {self.max_length} characters.")

@deconstructible
class FileNameCharValidator:
    def __init__(self, allowed_chars=None):
        if allowed_chars is None:
            allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."
        self.allowed_chars = allowed_chars

    def __call__(self, value):
        for char in value.name:
            if char not in self.allowed_chars:
                raise ValidationError(f"File name can only contain the following characters: {self.allowed_chars}")

# @deconstructible
# class FileNameLengthValidator:
#     def __init__(self, max_length=255):
#         self.max_length = max_length

#     def __call__(self, value):
#         if len(value.name) > self.max_length:
#             raise ValidationError(f"File name cannot be longer than {self.max_length} characters.")
