from django.db import models

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(Base):
    name       = models.CharField(max_length=30)
    email      = models.EmailField(max_length=250)
    password   = models.CharField(max_length=250, null=True)
    has_agreed = models.BooleanField(default=False)
    kakao_id   = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = 'users'
