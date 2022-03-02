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
            return HttpResponse("Permission denied.", status=403)
        
        sha_name, signature = receivedSignature.split('=', 1)
        if sha_name != 'sha256':
            return HttpResponse("Operation not supported.", status=501)

        is_valid = verifySignature(signature, raw)
        if(is_valid != True):
            return HttpResponse("Invalid signature. Permission Denied.", status=403)
        
        print("\nsignature Verified")

        print("\nTypeform webhook", request_body)

        return JsonResponse({"status":True,"message":"success"})

    return JsonResponse({"status":False,"message":"post request accepted"})