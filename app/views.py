from django.shortcuts import render
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status, renderers, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from app.models import Blogger


__author__ = 'fuiste'


class EmailUserAuthSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
                attrs['user'] = user
                return user
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "email" and "password"')
            raise serializers.ValidationError(msg)


class UserAuthenticationView(APIView):
    serializer_class = EmailUserAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        user = serializer.validate(request.DATA.copy())
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": user.id, "email": user.email}, status=status.HTTP_200_OK)


class UploadAuthenticationView(APIView):

    def post(self,request):
        return Response({"success": "OK"}, status=status.HTTP_200_OK)
