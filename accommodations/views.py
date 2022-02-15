import datetime

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.db.models import Q, Prefetch
from .models import Accommodation

class AccommodationListView(View):
    def get(self, request, *args, **kwargs):
        try:
            accommodations = Accommodation.objects.all()
            thema_group    = request.GET.getlist('themaGroup', None)
            region         = request.GET.get('region', None)
            is_verified    = request.GET.get('isVerified', None)
            people         = request.GET.get('people', 1)
            sort           = request.GET.get('sort', None)
            search         = request.GET.get('search', None)
            check_in_date  = request.GET.get('checkInDate', None)
            check_out_date = request.GET.get('checkOutDate', None)

            q = Q()
   
            if check_in_date and check_out_date:
                check_in_date  = datetime.datetime.strptime(check_in_date, "%a %b %d %Y %H:%M:%S %Z 0900 (한국 표준시)")
                check_out_date = datetime.datetime.strptime(check_out_date, "%a %b %d %Y %H:%M:%S %Z 0900 (한국 표준시)")

                for accommodation in accommodations:
                    if accommodation.check_in_date != None and accommodation.check_out_date != None:
                        reserved_check_in_date  = accommodation.check_in_date
                        reserved_check_out_date = accommodation.check_out_date

                        if check_in_date >= reserved_check_in_date and check_in_date <= reserved_check_out_date:
                            print(accommodation.name)
                            q.add(~Q(id=accommodation.id), q.AND)

            if thema_group:
                q.add(Q(themagroup__name__in = thema_group), q.AND)

            if region:
                q.add(Q(region = region), q.AND)

            if is_verified:
                q.add(Q(is_verified = is_verified), q.AND)
   
            accommodations = Accommodation.objects.filter(q, available_people__range=[people,30])
        
            if search:
                accommodations = accommodations.filter(
                    name__icontains = search
            )

            if sort:
                if sort == 'newest':
                    accommodations = accommodations.order_by('created_at')
                elif sort == "highest":
                    accommodations = accommodations.order_by('-price')
                elif sort == "lowest":
                    accommodations = accommodations.order_by('price')

            accommodation_information = [
                {   
                    "id"                     : accommodation.id,
                    "name"                   : accommodation.name,
                    "description"            : accommodation.description,
                    "detail_description"     : accommodation.detail_description,
                    "price"                  : accommodation.price,
                    "address"                : accommodation.address,
                    "region"                 : accommodation.region,
                    "is_verified"            : accommodation.is_verified,
                    "latitude"               : accommodation.latitude,
                    "longtitude"             : accommodation.longtitude,
                    "check_in_time"          : accommodation.check_in_time,
                    "check_out_time"         : accommodation.check_out_time,
                    "available_people"       : accommodation.available_people,
                    "reserved_check_in_date" : accommodation.check_in_date,
                    "reserved_check_out_date": accommodation.check_out_date,                 
                    "image_url"              : [images.image_url for images in accommodation.accommodationimage_set.all()],
                    "thema_group"            : [thema.name for thema in accommodation.themagroup_set.all()],
                } for accommodation in accommodations]

            return JsonResponse({"message": accommodation_information}, status=200)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)
