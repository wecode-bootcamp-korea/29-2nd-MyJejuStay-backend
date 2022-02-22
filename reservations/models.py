import uuid

from django.db import models
from django.forms import DateTimeField

from users.models import Base, User
from accommodations.models import Accommodation

class Reservation(Base):
    user               = models.ForeignKey(User, on_delete=models.CASCADE)
    accommodation      = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    check_in           = models.DateTimeField(null=True)
    check_out          = models.DateTimeField(null=True)
    number_of_adults   = models.PositiveIntegerField(default=1)
    number_of_children = models.IntegerField(default=0)
    reservation_code   = models.UUIDField(primary_key=True, default=uuid.uuid4)
    total_price        = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    class Meta:
        db_table = 'reservations'
