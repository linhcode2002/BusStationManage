from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics
from rest_framework.parsers import MultiPartParser
from .models import *
from .serializer import BusCompanySerializer, UserSerializer


class BusCompanyViewSet(viewsets.ModelViewSet):
    queryset = BusCompany.objects.filter(active=True)
    serializer_class = BusCompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser]

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         return [permissions.IsAuthenticated]
    #
    #     return [permissions.AllowAny]

    # #user/current_user/
    # @action(methods=['get'], url_name='current', detail=False)
    # def current_user(self, request):
    #     return Response(serializer.UserSerializer(request.user).data)