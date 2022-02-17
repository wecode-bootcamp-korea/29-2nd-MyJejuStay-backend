from django.http            import JsonResponse
from django.views           import View

class MainPageView(View):
  def get(self,request):
    mainvideo = '/images/Main/MyJejuStay.mp4'
    return JsonResponse({'mainvideo': mainvideo}, status=200)
