from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm

from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "placeholder": "Имя пользователя",
        "class": "form-control",
    }))
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "class": "form-control",
        }),
    )


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "avatar", "about")


class UserEditForm(forms.ModelForm):
    birth_date = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name',
            'email', 'phone_number',
            'birth_date', 'about',
            'avatar'
        )
