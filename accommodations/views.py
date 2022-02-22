import datetime, json, uuid

from django.http import JsonResponse
from django.db.models import Q, Prefetch
from django.core.exceptions import ObjectDoesNotExist
from django.views           import View
from decimal import Decimal

from .models import Accommodation, Review
from reservations.models import Reservation
from users.models import User
from users.utils import login_decorator

class AccommodationListView(View):
    def get(self, request, *args, **kwargs):
        try:
            accommodations = Accommodation.objects.all()
            thema_group    = request.GET.getlist('themaGroup', None)
            region         = request.GET.get('region', None)
            is_verified    = request.GET.get('isVerified', None)
            people         = request.GET.get('people', 1)
            sort           = request.GET.get('sort', 'created_at')
            search         = request.GET.get('search', None)
            check_in_date  = request.GET.get('checkInDate', None)
            check_out_date = request.GET.get('checkOutDate', None)

            q = Q()

            if check_in_date and check_out_date:
                check_in_date  = datetime.datetime.strptime(check_in_date, "%a %b %d %Y %H:%M:%S %Z+0900 (한국 표준시)")
                check_out_date = datetime.datetime.strptime(check_out_date, "%a %b %d %Y %H:%M:%S %Z+0900 (한국 표준시)")

            reservations = Reservation.objects.all()

            for reservation in reservations:
                q.add(~Q(check_in_date__range = [reservation.check_in, reservation.check_out]), q.AND)
                q.add(~Q(check_out_date__range = [reservation.check_in, reservation.check_out]), q.AND)

            filters = {
                "thema_group": "themagroup__name__in",
                "region"     : "region",
                "is_verified": "is_verified"
            }
            
            filter_set = {
                filters.get(key) : value[0] for (key, value) in dict(request.GET).items() if filters.get(key)
            }

            if search:
                filter_set["name__icontains"] = search
            accommodations = Accommodation.objects.filter(q, **filter_set, available_people__gte=people).order_by(sort)

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
            review_sort   = request.GET.get('reviewSort', 'created_at')
            accommodation = Accommodation.objects.get(id=accommodation_id)

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
                    "minimum_stay"           : accommodation.minimum_stay,
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
                        "image_url": [review_image.image_url for review_image in review.reviewimage_set.all()],
                        "review_id": review.id,
                    } for review in accommodation.review_set.all().order_by(review_sort)],
                }
            ]
            return JsonResponse({"message": accommodation_information}, status=200)
        except:
            return KeyError({"message":"KEY_ERROR"}, status=400)

    @login_decorator
    def post(self, request, accommodation_id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_id            = request.user.id
            id                 = accommodation_id
            number_of_adults   = int(data["numberOfAdult"])
            number_of_children = int(data["numberOfChildren"])
            check_in_date      = data["checkInDate"]
            check_out_date     = data["checkOutDate"]

            gmt_9              = datetime.timedelta(hours=9)
            check_in_date      = datetime.datetime.strptime(check_in_date, "%Y-%m-%dT%H:%M:%S.%fZ") + gmt_9
            check_out_date     = datetime.datetime.strptime(check_out_date, "%Y-%m-%dT%H:%M:%S.%fZ") + gmt_9

            accommodation      = Accommodation.objects.get(id=id)
            minimum_stay       = accommodation.minimum_stay
            available_poeple   = accommodation.available_people
            booking_days       = (check_out_date - check_in_date).days
            price              = accommodation.price
            total_price        = int(price * ((number_of_adults -1) * Decimal(1.2) + number_of_children * Decimal(0.5))) * booking_days
            discounted_price   = total_price * 0.7
            final_price        = discounted_price * 1.1

            if number_of_adults > available_poeple:
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
                reservation_code = uuid.uuid4()

                Reservation.objects.create(
                    user_id            = user_id,
                    accommodation_id   = id,
                    check_in           = check_in_date,
                    check_out          = check_out_date,
                    number_of_adults   = number_of_adults,
                    number_of_children = number_of_children,
                    reservation_code   = reservation_code,
                    total_price        = float(final_price)
                )

            if accommodation.check_in_date:
                accommodation.check_in_date  = check_in_date
                accommodation.check_out_date = check_out_date

                Accommodation.objects.filter(id=id).update(check_in_date=check_in_date, check_out_date=check_out_date)
                reservation_code = uuid.uuid4()
                Reservation.objects.create(
                    user_id = user_id,
                    accommodation_id   = id,
                    check_in           = check_in_date,
                    check_out          = check_out_date,
                    number_of_adults   = number_of_adults,
                    number_of_children = number_of_children,
                    reservation_code   = reservation_code,
                    total_price        = float(final_price)
                )
            reservation_information = {
                "user_id"           : user_id,
                "accommodations_id" : id,
                "number_of_adults"  : number_of_adults,
                "number_of_children": number_of_children,
                "check_in_date"     : accommodation.check_in_date,
                "check_out_date"    : accommodation.check_out_date,
                "booking_days"      : booking_days,
                "minimum_stay"      : minimum_stay,
                "total_price"       : total_price,
                "discounted_price"  : discounted_price,
                "reservation_code"  : reservation_code,
                "final_price"       : float(final_price),
            }
            return JsonResponse({"message": reservation_information}, status=201)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except ValueError:
            return JsonResponse({"message": "INVALID_VALUE"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "NO_ACCOMMODATION"}, status=400)
