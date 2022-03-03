from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import hashlib
import hmac
import json
import base64
import os
from django.conf import settings

def verifySignature(receivedSignature: str, payload):

    
    WEBHOOK_SECRET = settings.TYPEFORM_SECRET

    digest = hmac.new(WEBHOOK_SECRET.encode('utf-8'), payload, hashlib.sha256).digest()
    
    e = base64.b64encode(digest).decode()
    
    if(e == receivedSignature):
      return True
    return False


@csrf_exempt
def index(request):

    # return HttpResponse("Hello, world. You're at the polls index.")
    if request.method == 'POST':

        raw = request.body
        request_body = json.loads(raw)
        
        receivedSignature = request.headers.get("typeform-signature")

        if receivedSignature is None:
            return JsonResponse({"status":False,"message":"Permission denied."})
        
        sha_name, signature = receivedSignature.split('=', 1)
        if sha_name != 'sha256':
            return JsonResponse({"status":False,"message":"Operation not supported."})

        is_valid = verifySignature(signature, raw)
        
        if(is_valid != True):
            return JsonResponse({"status":False,"message":"Invalid signature. Permission Denied."})
        
        elif is_valid:
            print("\nsignature Verified")

            print("\nTypeform webhook", request_body)

            return JsonResponse({"status":True,"message":"success"})
        
    if request.method == 'GET':
        return JsonResponse({"status":False,"message":"post request accepted"})
