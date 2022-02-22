import datetime, json

from decimal import Decimal

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.db.models import Q, Prefetch
from django.core.exceptions import ObjectDoesNotExist

from .models import Accommodation
from reservations.models import Reservation

class AccommodationListView(View):
    def get(self, request, *args, **kwargs):
        try:
            # :8000/accommodations?sort=created_at
            # :8000/accommodations?sort=-price
            # request.GET => QueryDict

            print(request.GET)
            print(type(request.GET))
#             accommodations = Accommodation.objects.all()
            thema_group    = request.GET.getlist('themaGroup', None)
            region         = request.GET.get('region', None)
            is_verified    = request.GET.get('isVerified', None)
            people         = request.GET.get('people', 1)
            sort           = request.GET.get('sort', "created_at")
            search         = request.GET.get('search', None)
            check_in_date  = request.GET.get('checkInDate', None)
            check_out_date = request.GET.get('checkOutDate', None)

            # 체크인 체크아웃 기간에 예약들을 필터링
            # 그 예약들을 가진 accommodations exclude
            
            # reservations 필터링 => 체크인 체크아웃 사이에 포함된
            # Accommodation.objects.exclude(reservation__in=reservations)


   
#             if check_in_date and check_out_date:
#                 check_in_date  = datetime.datetime.strptime(check_in_date, "%a %b %d %Y %H:%M:%S %Z 0900 (한국 표준시)")
#                 check_out_date = datetime.datetime.strptime(check_out_date, "%a %b %d %Y %H:%M:%S %Z 0900 (한국 표준시)")
# 
#                 for accommodation in accommodations:
#                     if accommodation.check_in_date != None and accommodation.check_out_date != None:
#                         reserved_check_in_date  = accommodation.check_in_date
#                         reserved_check_out_date = accommodation.check_out_date
# 
#                         if check_in_date >= reserved_check_in_date and check_in_date <= reserved_check_out_date:
#                             print(accommodation.name)
#                             q.add(~Q(id=accommodation.id), q.AND)

            # :8000/accommodations/thema_group=city

            filters = {
                "thema_group" : "themagroup__name__in",
                "region"      : "region"
            }
            
            filter_set = {
                filters.get(key) : value for (key, value) in dict(request.GET).items() if filters.get(key)
                # "themagroup__name__in" : "city" 
                # "region" : "region"
            }

            print(filter_set)

            if search:
                filter_set["name__icontains"] = search

            q = Q()

            if check_in_date and check_out_date:
                q |= Q(check_in_date__range = [check_in_date, check_out_date - datetime.timedelta(days=1)])
                q |= Q(check_out_date__range = [check_in_date + datetime.timedelta(days=1), check_out_date])


            accommodations = Accommodation.objects.filter(**filter_set, available_people__gte=people) \
                                                  .exclude(q) \
                                                  .order_by(sort)


#             if thema_group:
#                 q.add(Q(themagroup__name__in = thema_group), q.AND)
# 
#             if region:
#                 q.add(Q(region = region), q.AND)
# 
#             if is_verified:
#                 q.add(Q(is_verified = is_verified), q.AND)
   
#             accommodations = Accommodation.objects.filter(q, available_people__range=[people,30])

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

class AccommodationView(View):
    def get(self, request, accommodation_id, *args, **kwargs):
        try:
            accommodation             = Accommodation.objects.get(id=accommodation_id)
#             accommodation_information = [
#                 {   
#                     "id"                     : accommodation.id,
#                     "name"                   : accommodation.name,
#                     "description"            : accommodation.description,
#                     "detail_description"     : accommodation.detail_description,
#                     "price"                  : accommodation.price,
#                     "address"                : accommodation.address,
#                     "region"                 : accommodation.region,
#                     "is_verified"            : accommodation.is_verified,
#                     "latitude"               : accommodation.latitude,
#                     "longtitude"             : accommodation.longtitude,
#                     "check_in_time"          : accommodation.check_in_time,
#                     "check_out_time"         : accommodation.check_out_time,
#                     "available_people"       : accommodation.available_people,
#                     "reserved_check_in_date" : accommodation.check_in_date,
#                     "reserved_check_out_date": accommodation.check_out_date,
#                     "image_url"              : [images.image_url for images in accommodation.accommodationimage_set.all()],
#                     "thema_group"            : [thema.name for thema in accommodation.themagroup_set.all()],
#                     "reviews"                : [{
#                         "user_name": review.user.name,
#                         "comment"  : review.comment,
#                         "rate"     : review.score,
#                         "image_url": review_images.image_url,
#                         "review_id": review.id,
#                     }
#                     for review in accommodation.review_set.all()
#                     for review_images in review.reviewimage_set.all()
#                     ]
#                 }
#             ]

            accommodation_information = {   
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
                "reviews"                : [{
                    "user_name": review.user.name,
                    "comment"  : review.comment,
                    "rate"     : review.score,
                    "images": [{
                        'image_url' : image.image_url
                    } for image in review.reviewimage_set.all()],
                    "review_id": review.id,
                } for review in accommodation.review_set.all() ]
            }

            return JsonResponse({"message": accommodation_information}, status=200)
        except:
            return KeyError({"message":"KEY_ERROR"}, status=400)

    def post(self, request, accommodation_id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            id                 = accommodation_id
            number_of_adult    = int(data["numberOfAdult"])
            number_of_children = int(data["numberOfChildren"])
            check_in_date      = data["checkInDate"]
            check_out_date     = data["checkOutDate"]
            gmt_9              = datetime.timedelta(hours=9)
            check_in_date      = datetime.datetime.strptime(check_in_date, "%a %b %d %Y %H:%M:%S %Z 0900 (한국 표준시)")  + gmt_9
            check_out_date     = datetime.datetime.strptime(check_out_date, "%a %b %d %Y %H:%M:%S %Z 0900 (한국 표준시)") + gmt_9

            accommodation    = Accommodation.objects.get(id=id)
            minimum_stay     = accommodation.minimum_stay
            available_poeple = accommodation.available_people
            booking_days     = (check_out_date - check_in_date).days
            price            = accommodation.price
            total_price      = int(price * ((number_of_adult -1) * Decimal(1.02) + number_of_children * Decimal(0.5)))
            discounted_price = total_price*0.7

            if number_of_adult > available_poeple:
                raise ValueError

            if check_in_date > check_out_date:
                return JsonResponse({"message": "CHECK_IN_DATE_ERROR"}, status=400)

            if booking_days <= minimum_stay:
                return JsonResponse({"message": f"MINIMUM_STAY: {minimum_stay}"}, status=400)

            if check_in_date and check_out_date:
                if accommodation.check_in_date != None and accommodation.check_out_date != None:
                    reserved_check_in_date  = accommodation.check_in_date
                    reserved_check_out_date = accommodation.check_out_date

                    if check_in_date >= reserved_check_in_date and check_in_date <= reserved_check_out_date:
                        return JsonResponse({"message": "ROOM_IS_FULL"}, status=400)

            if not accommodation.check_in_date:
                accommodation.check_in_date  = check_in_date
                accommodation.check_out_date = check_out_date
                accommodation.save()

            if accommodation.check_in_date:
                accommodation.check_in_date  = check_in_date
                accommodation.check_out_date = check_out_date
                Accommodation.objects.filter(id=id).update(check_in_date=check_in_date, check_out_date=check_out_date)

            reservation_information = {
                "accommodations_id" : id,
                "number_of_adults"  : number_of_adult,
                "number_of_children": number_of_children,
                "check_in_date"     : accommodation.check_in_date,
                "check_out_date"    : accommodation.check_out_date,
                "booking_days"      : booking_days,
                "minimum_stay"      : minimum_stay, 
                "total_price"       : total_price,
                "discounted_price"  : discounted_price,
            }

            return JsonResponse({"message": reservation_information}, status=201)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except ValueError:
            return JsonResponse({"message": "INVALID_VALUE"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "NO_ACCOMMODATION"}, status=400)
