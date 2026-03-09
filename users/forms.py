from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, get_user_model, authenticate
from django.utils.html import strip_tags
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from .models import CustomUser

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=254)
    first_name = forms.CharField(label=_("Имя"), max_length=30, required=True)
    last_name = forms.CharField(label=_("Фамилия"), max_length=30, required=True)
    city = forms.CharField(label=_("Город"), max_length=100, required=True)
    phone = forms.CharField(label=_("Телефон"), max_length=18, required=True, validators=[RegexValidator(r'^(?:\+7|8)7\d{9}$', _('Введите корректный номер телефона.'))])
    iin = forms.CharField(label=_("ИИН"), max_length=12, validators=[RegexValidator(r'^\d{12}$', _('Введите корректный ИИН.'))], required=False)
    work_place = forms.CharField(label=_("Место работы"), max_length=254, required=True)
    specialty = forms.CharField(label=_("Специальность"), max_length=200, required=True)
    password1 = forms.CharField(label=_("Пароль"), required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Подтвердите пароль"), required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "city", "phone", "iin", "work_place", "specialty", "password1", "password2")

    def clean_email(self):
      email = self.cleaned_data.get("email")
      if User.objects.filter(email=email).exists():
          raise forms.ValidationError(_("Пользователь с таким email уже зарегестрирован."))
      return email

    def save(self, commit = True):
        user = super().save(commit=False)
        user.username = None
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        for field in ["first_name", "last_name", "city", "work_place", "specialty"]:
            value = cleaned_data.get(field, "")
            if value:
                cleaned_data[field] = strip_tags(value)
        return cleaned_data
    
class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label=_("Email"), max_length=254, required=True, widget=forms.EmailInput(attrs={"autofocus":True}))
    password = forms.CharField(label=_("Пароль"), widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Неверный email или пароль."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("Этот аккаунт неактивен."))
        return cleaned_data
    
class CustomUserEditForm(UserEditForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    city = forms.CharField(max_length=100, required=True, label=_("Город"))
    phone = forms.CharField(max_length=12, required=True, validators=[RegexValidator(r'^\+\d{10,12}$', _('Введите корректный номер телефона.'))], label=_("Телефон"))
    work_place = forms.CharField(max_length=254, required=True, label=_("Место работы"))
    specialty = forms.CharField(max_length=200, required=True, label=_("Специальность"))

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "city", "phone", "iin", "work_place", "specialty")
        widgets = {
            "email": forms.EmailInput(attrs={"readonly": "readonly"}),
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
            "city": forms.TextInput(),
            "phone": forms.TextInput(),
            "iin": forms.TextInput(attrs={"readonly": "readonly"}),
            "work_place": forms.TextInput(),
            "specialty": forms.TextInput(),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        for field in ["first_name", "last_name", "city", "work_place", "specialty"]:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])
        return cleaned_data