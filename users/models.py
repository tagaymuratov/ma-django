from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.html  import strip_tags

class CustomUserManager(BaseUserManager):
  def create_user(self, email, first_name, last_name, city, phone, iin, work_place, specialty, password=None, **extra_fields):
    if not email:
      raise ValueError("The Email field must be set")
    email = self.normalize_email(email)
    user = self.model(email=email, first_name=first_name, last_name=last_name, city=city, phone=phone, iin=iin, work_place=work_place, specialty=specialty,**extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, email, first_name, last_name, city, phone, iin, work_place, specialty, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)

    if extra_fields.get("is_staff") is not True:
      raise ValueError("Superuser must have is_staff=True.")
    if extra_fields.get("is_superuser") is not True:
      raise ValueError("Superuser must have is_superuser=True.")

    return self.create_user(email, first_name, last_name, city, phone, iin, work_place, specialty, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254 ,unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=12, unique=True)
    iin = models.CharField(max_length=12, unique=True)
    work_place = models.CharField(max_length=254)
    specialty = models.CharField(max_length=200)

    username = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "city", "phone", "iin", "work_place", "specialty"]

    def __str__(self):
      return self.email
    
    def clean(self):
      for field in ["first_name", "last_name", "city", "work_place", "specialty"]:
        value = getattr(self, field, "")
        if value:
          setattr(self, field, strip_tags(value))
