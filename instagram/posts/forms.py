from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.Form):
    name = forms.CharField(
        label="Название",
        max_length=80,
        required=True,
    )

    image = forms.ImageField(label="Картинка", required=True)
    description = forms.CharField(label="Описание", max_length=1000)


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'image', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name', None)
        if name:
            if len(name) < 4 or len(name) > 50:
                raise ValidationError('Название должно быть нормальной длины (от 4 до 50)')
            if not name[0].isupper:
                raise ValidationError('Название должно начинаться с заглавной буквы')
            return name
        else:
            raise ValidationError('Название обязательно!')

    def clean_image(self):
        image = self.cleaned_data.get('image', None)
        if image:
            if image.size > 5242880:
                raise ValidationError('Слишком большой размер')
            return image
        else:
            raise ValidationError('Картинка обязательна!')
