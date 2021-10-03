"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from .models import Comment
from .models import Blog
from .models import Orders
from .models import Catalog


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Логин'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': ""}
  
class AnketaForm(forms.Form):
    name = forms.CharField(label='Имя', min_length=2, max_length=100)
    gender = forms.CharField(label='Что случилось?', widget=forms.RadioSelect(choices=[('1', 'Вопрос о товаре'), ('2', 'У меня проблема')]), initial=1)
    internet = forms.ChoiceField(label='Кем Вы являетесь?', choices=[('1', 'Физ. лицо'), ('2', 'Юр. Лицо')], initial=1)
    notice = forms.BooleanField(label='Продублировать ваш запрос на почту?', required=False)
    email = forms.EmailField(label='E-mail', min_length=7)
    message = forms.CharField(label='Суть обращения',
                                widget=forms.Textarea(attrs={'rows':12,'cols':20}))

class RequisitesForm(forms.Form):
    bank = forms.CharField(label='Банк', min_length=2, max_length=100)
    bik = forms.CharField(label='БИК',  min_length=2, max_length=100)
    kpp = forms.CharField(label='КПП',  min_length=2, max_length=100)
    account = forms.CharField(label='Счет',  min_length=2, max_length=100)

class EmailForm(forms.Form):
    email = forms.EmailField(label='E-mail', min_length=7)
class BlogForm (forms.ModelForm):
    class Meta:
        model = Blog        
        fields = ('title','content','description','image')
        labels = {'title': "Заголовок",'content': "Полное содержание",'description': "Краткое содержание",'image': "Изображение"}

class OrderForm (forms.ModelForm): 
    class Meta: 
        model = Orders 
        fields = ()

class ProductForm (forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ('title','description','quantity','image','price')
        labels = {'title': "Заголовок",'description': "Краткое содержание",'quantity': "Количество",'price': "Цена",'image': "Изображение"}