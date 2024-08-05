from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import DivisionModel
User = get_user_model()


class SignUpForm(UserCreationForm):

    division = forms.ModelChoiceField(
        queryset=DivisionModel.objects.all(),
        required=True,
        label='所属',
        to_field_name='name',
        empty_label="部門を選択してください",
    )
    
    class Meta:
        model = User
        fields = (
            "last_name", "first_name", 
            "email","division",
            "username", "password1", "password2",
            )

    def save(self, commit=True):
        # commitがFalseだと、DBに保存されないので注意
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.division = self.cleaned_data["division"]
        user.last_name = self.cleaned_data["last_name"]
        user.first_name = self.cleaned_data["first_name"]
        user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        # バリデーションメッセージをカスタマイズまたは削除
        self.fields['password1'].help_text = None