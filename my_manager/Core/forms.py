# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from .models import Question, Answer

class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question = question
        choices = [(answer.id, answer.text) for answer in question.answers.all()]
        self.fields['answer'] = forms.ChoiceField(
            label=question.text,
            choices=choices,
            widget=forms.RadioSelect
        )

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    email = forms.EmailField(max_length=254, required=True, label='Email Address')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
        }
