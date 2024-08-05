from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    username = models.CharField('社員ID', 
                    max_length=8, 
                    unique=True, 
                    null=False,
                    validators=[RegexValidator(r'^[0-9]{8}$')],
                )
    email = models.EmailField('メールアドレス', max_length=254, unique=True, null=False)
    first_name = models.CharField('名前', max_length=30, blank=False, null=False)
    last_name = models.CharField('苗字', max_length=30, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    division = models.CharField('部門', max_length=40, blank=False, null=False)
    

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    class Meta:
        db_table = 'CustomUsers'



class DivisionModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Divisions'