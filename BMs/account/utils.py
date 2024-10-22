from django.forms.utils import ErrorList

class AuthenticationErrorList (ErrorList):
    template_name = 'errors/list/authentication/default.html'
    template_name_text = "errors/list/authentication/text.txt"
    template_name_ul = 'errors/list/authentication/ul.html'

class PasswordChangeErrorList (ErrorList):
    template_name = 'errors/list/password_change/default.html'
    template_name_text = "errors/list/password_change/text.txt"
    template_name_ul = 'errors/list/password_change/ul.html'

class PasswordResetErrorList (ErrorList):
    template_name = "errors/list/password_reset/default.html"
    template_name_text = "errors/list/password_reset/text.txt"
    template_name_ul = "errors/list/password_reset/ul.html"

class RegistrationErrorList (ErrorList):
    template_name = "errors/list/registration/default.html"
    template_name_text = "errors/list/registration/text.txt"
    template_name_ul = "errors/list/registration/ul.html"