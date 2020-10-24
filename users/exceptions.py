from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status


class PasswordConfirmationFailedException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Those passwords didn't match.")
    default_code = "password_confirmation_failed"


class PasswordTooWeakException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("The password you typed does not meet the password requirements.")
    default_code = "password_too_weak"


class InvalidCredentialsException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("You have entered an invalid username or password")
    default_code = "invalid_credentials"
