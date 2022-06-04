from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput, TextInput, ClearableFileInput, Textarea
from .models import Profile, Post


class UserRegistrationForm(ModelForm):
    password = CharField(label='Password', widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = CharField(label='Repeat password', widget=PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
        }


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароль не совпадает')
        return cd['password2']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic', 'first_name', 'last_name', 'bio')

        widgets = {
            'profile_pic': ClearableFileInput(),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'bio': Textarea(attrs={'class': 'form-control'}),
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('head', 'text')

        widgets = {
            'head': TextInput(attrs={'class': 'form-control'}),
            'text': Textarea(attrs={'class': 'form-control'}),
        }