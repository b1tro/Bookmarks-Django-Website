from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, password_validation, SetPasswordForm
from .utils import AuthenticationErrorList, PasswordChangeErrorList, PasswordResetErrorList, RegistrationErrorList
from django.contrib.auth.models import User
from django.forms import ValidationError
from .models import Profile
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class NewAuthenticationForm(AuthenticationForm):

    username =UsernameField(widget=forms.TextInput(attrs={"autofocus": True}), label="Логин")
    password = forms.CharField(
        label= ("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(error_class = AuthenticationErrorList, *args, **kwargs)

    error_messages = {
        "invalid_login": (
            "Неправильный логин или пароль"
        ),
        "inactive": ("Учетная запись заблокирована"),
    }

class NewPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(error_class=PasswordChangeErrorList, *args, **kwargs)

    error_messages = {
        "password_mismatch": ("Новые пароли не совпадают"),
        "password_incorrect": (
            "Прошлый пароль введен неверно"
        ),
    }
    old_password = forms.CharField(
        label= ("Старый пароль"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
    new_password1 = forms.CharField(
        label= ("Новый пароль"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label= ("Подтверждение пароля"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

class NewPasswordResetForm(SetPasswordForm):


    error_messages = {
        "password_mismatch": ("Пароли не совпадают"),
    }
    new_password1 = forms.CharField(
        label=("Новый пароль"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=("Подтверждение пароля"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(error_class=PasswordResetErrorList, *args, **kwargs)
        print(self.error_class.template_name_ul)

class UserRegistrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(error_class = RegistrationErrorList, *args, **kwargs)

    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {"username": "Логин",
                  "email": "Email"}
        help_texts = {"username": None}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError("Пароли не совпадают")
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd["username"]):
            raise ValidationError("Пользователь с таким логином уже существует")
        return cd['username']

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd["email"]):
            raise ValidationError("Пользователь с такой почтой уже существует")
        return cd['email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
        labels = {"date_of_birth": "Дата рождения",
                  "photo": "Фото"}
        widgets = {"photo": forms.FileInput}

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']