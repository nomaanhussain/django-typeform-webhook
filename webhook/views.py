from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



@csrf_exempt
def index(request):

    # return HttpResponse("Hello, world. You're at the polls index.")
    if request.method == 'POST':
            
        request_body = json.loads(request.body)

        print("Typeform webhook", request_body)

        return JsonResponse({"status":True,"message":"success"})

    return JsonResponse({"status":False,"message":"post request accepted"})