from django.db import models

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(Base):
<<<<<<< HEAD
    name       = models.CharField(max_length=30)
    email      = models.EmailField(max_length=250)
    password   = models.CharField(max_length=250, null=True)
    has_agreed = models.BooleanField(default=False)
    kakao_id   = models.PositiveIntegerField()

    class Meta:
        db_table = 'users'
=======
    name                 = models.CharField(max_length=30)
    email                = models.EmailField(max_length=250)
    password             = models.CharField(max_length=250, null=True)
    has_agreed           = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

class Social(Base):
    user                 = models.ForeignKey(User, on_delete=models.CASCADE)
    social_platform_name = models.CharField(max_length=250) 

    class Meta:
        db_table = 'socials'
>>>>>>> a3c41a7 (Add: Initial Models)
