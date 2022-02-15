from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .models import Accommodation

class AccommodationListView(View):
    def get(self, request):
        accommodations = Accommodation.objects.all()
        try:
            accommodationList = [
                {   
                    "id": accommodation.id,
                    "name": accommodation.name,
                    "description": accommodation.description,
                    "price": accommodation.price,
                    "address": accommodation.address,
                    "region": accommodation.region,
                    "is_verifeid": accommodation.is_verified,
                    "latitude": accommodation.latitude,
                    "longtitude": accommodation.longtitude,
                    "check_in_time": accommodation.check_in_time,
                    "check_out_time": accommodation.check_out_time,
                    "image_url": [images.image_url for images in accommodation.accommodationimage_set.all()],
                    "thema_group": [thema.type for thema in accommodation.themagroup_set.all()]
                } for accommodation in accommodations]

            return JsonResponse({"message": accommodationList}, status=200)
        except:
            return KeyError({"message":"KEY_ERROR"}, status=400)
