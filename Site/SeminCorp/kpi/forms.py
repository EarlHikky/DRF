from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class AddStaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'photo']
        # fields = '__all__'


# class AddSellForm(forms.Form):
#     fio = forms.ModelChoiceField(queryset=Staff.objects.all(), label="ФИО", required=False)
#     extradition = forms.IntegerField(label="Выдачи", required=False)
#     ti = forms.DecimalField(max_digits=5, decimal_places=2, label="ТИ", required=False)
#     kis = forms.DecimalField(max_digits=5, decimal_places=2, label="КИС", required=False)
#     trener = forms.DecimalField(max_digits=5, decimal_places=2, label="Тренер", required=False)
#     client = forms.DecimalField(max_digits=5, decimal_places=2, label="Клиент", required=False)


class AddSaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fio'].empty_label = "Выбери сотрудника"

    class Meta:
        model = Sales
        # fields = ['fio', 'extradition', 'ti', 'kis', 'trener', 'client']
        fields = '__all__'
        # widgets = {'fio': forms.ModelChoiceField(queryset=Staff.objects.all(), required=False),
        #            'extradition': forms.IntegerField(required=False),
        #            'ti': forms.DecimalField(required=False),
        #            'kis': forms.DecimalField(required=False),
        #            'trener': forms.DecimalField(required=False),
        #            'client': forms.DecimalField(required=False),
        #            }
