from django.shortcuts import render
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status, renderers, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from app.models import Blogger
import time, os, json, base64, hmac, urllib, boto, sys
from hashlib import sha1
import boto.s3
from boto.s3.key import Key


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


class UploadImageView(APIView):

    def post(self,request):
        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')

        bucket_name = os.environ.get('S3_BUCKET')
        conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket('tile-blog')
        print request.FILES.get('file')
        return Response({"token": "YOYOYO"}, status=status.HTTP_200_OK)
