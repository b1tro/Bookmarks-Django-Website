from gettext import ngettext

from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator
from django.core.exceptions import ValidationError


class CustomMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "Пароль слишком короткий. Он должен содержать минимум "
                    "%(min_length)d символов.",
                    "Пароль слишком короткий. Он должен содержать минимум "
                    "%(min_length)d символов.",
                    self.min_length,
                ),
                code="password_too_short",
                params={"min_length": self.min_length},
            )


class CustomNumericPasswordValidator(NumericPasswordValidator):
        def validate(self, password, user=None):
            if password.isdigit():
                raise ValidationError(
                    ("Пароль не может состоять только из цифр."),
                    code="password_entirely_numeric",
                )