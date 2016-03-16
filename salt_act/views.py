from django.shortcuts import render
#coding=utf-8
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from act import exec_cmd,exec_cmd_salt,salt_key,salt_key_accept,salt_key_delete,salt_minion_init,salt_module_name

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
@csrf_exempt
def Cmd_saltViewSet(request):
    host=request.POST.get('host')
    module_name=request.POST.get('module_name')
    arg=request.POST.get('arg')

    result=exec_cmd_salt(host,module_name,arg)
    return HttpResponse(result)

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
@csrf_exempt
def CmdViewSet(request):
    host=request.POST.get('host')
    module_name=request.POST.get('module_name')
    if request.POST.has_key('arg'):
        arg=request.POST.get('arg').split('#')
        n_arg=tuple(arg)
    else:
        n_arg=()
    result=exec_cmd(host,module_name,n_arg)
    return HttpResponse(json.dumps(result))

@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def Salt_key_all_ViewSet(request):
    result=salt_key()
    return HttpResponse(json.dumps(result))

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
@csrf_exempt
def Salt_key_accept_ViewSet(request):
    master=request.POST.get('master')
    host=request.POST.get('minion')
    result=salt_key_accept(master,host)
    return HttpResponse(json.dumps(result))

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
@csrf_exempt
def Salt_key_delete_ViewSet(request):
    master=request.POST.get('master')
    host=request.POST.get('minion')
    result=salt_key_delete(master,host)
    return HttpResponse(json.dumps(result))

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
@csrf_exempt
def Salt_minion_init_ViewSet(request):
    master=request.POST.get('master')
    host=request.POST.get('minion')
    result=salt_minion_init(master,host)
    return HttpResponse(json.dumps(result))

@api_view(['GET',])
@permission_classes([IsAuthenticated,])
@csrf_exempt
def Salt_module_name_ViewSet(request):
    result=salt_module_name()
    return HttpResponse(json.dumps(result))