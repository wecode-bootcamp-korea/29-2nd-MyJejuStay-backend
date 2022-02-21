from django.http            import JsonResponse
from django.views           import View

from accommodations.models import MainPageVideo

class PageVideoView(View):
  def get(self,request):
    try:
      video_id = request.GET.get('video_id', 1)
      video_url = MainPageVideo.objects.get(id=video_id).video_url
      return JsonResponse({'video_url': video_url}, status=200)

    except KeyError:
      return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    except MainPageVideo.DoesNotExist:
      return JsonResponse({'message': 'INVALID_VIDEO'}, status=401)

  
