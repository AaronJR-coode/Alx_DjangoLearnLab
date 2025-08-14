from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post, Comment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

class CommentForm(forms.ModelForm):
    MIN_LEN = 5


    class Meta:
        model = Comment
        fields = ['content']
        widget = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a commnet here'})
        }
        help_texts = {
            'content': 'Make Peace Bro!'
        }

    def clean_ontent(self):
        content = self.cleaned_data.get('content', '')
        if len(content.strip()) < self.MIN_LEN:
            raise forms.ValidationError(f'Comment too long, must be {self.MIN_LEN}.')
        return content