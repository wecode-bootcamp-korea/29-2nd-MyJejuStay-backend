from django.db import models

from users.models import Base, User

class Accommodation(Base):
    name           = models.CharField(max_length=250)
    description    = models.CharField(max_length=250)
    price          = models.DecimalField(decimal_places=2, max_digits=10)
    address        = models.CharField(max_length=250)
    region         = models.CharField(max_length=30)
    is_verified    = models.BooleanField(default=False)
    latitude       = models.DecimalField(decimal_places=7, max_digits=10)
    longtitude     = models.DecimalField(decimal_places=7, max_digits=10)
    check_in_time  = models.DateTimeField()
    check_out_time = models.DateTimeField()
    minimum_stay   = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'accommodations'

class AccommodationImage(Base):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    image_url     = models.CharField(max_length=250)

    class Meta:
        db_table = 'accommodation_images'

class ThemaGroup(Base):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    name          = models.CharField(max_length=50)

    class Meta:
        db_table = 'thema_groups'

class Review(Base):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    comment       = models.CharField(max_length=250)
    score         = models.PositiveIntegerField()

    class Meta:
        db_table = 'reviews'

class ReviewImage(Base):
    review      = models.ForeignKey(Review, on_delete=models.CASCADE)
    image_url   = models.CharField(max_length=250)

    class Meta:
        db_table = 'review_images'
