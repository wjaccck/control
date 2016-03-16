# Create your views here.
from django.shortcuts import render
from rest_framework import permissions
import django_filters
from salt_api.models import Master,Minion,Module,Log
from salt_api.serializers import MasterSerializer,MinionSerializer,ModuleSerializer,LogSerializer
from rest_framework import viewsets
from rest_framework import filters


class MasterViewSet(viewsets.ModelViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name','ip',)
    permission_classes = (permissions.DjangoModelPermissions,)
    def perform_create(self, serializer):
        return super(MasterViewSet, self).perform_create(serializer)

class MinionViewSet(viewsets.ModelViewSet):
    queryset = Minion.objects.all()
    serializer_class = MinionSerializer
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter)
    filter_fields = ('ip','name',)
    search_fields = ('ip','name')
    permission_classes = (permissions.DjangoModelPermissions,)
    def perform_create(self, serializer):
        return super(MinionViewSet, self).perform_create(serializer)

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name',)
    permission_classes = (permissions.DjangoModelPermissions,)
    def perform_create(self, serializer):
        return super(ModuleViewSet, self).perform_create(serializer)

class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('host',)
    permission_classes = (permissions.DjangoModelPermissions,)
    def perform_create(self, serializer):
        return super(LogViewSet, self).perform_create(serializer)