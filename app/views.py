from django.shortcuts import render
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status, renderers, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from app.models import Blogger
import time, os, json, base64, hmac, urllib
from hashlib import sha256


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
        AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
        AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
        S3_BUCKET = os.environ.get('S3_BUCKET')

        object_name = urllib.quote_plus(request.POST.get('file_name'))
        mime_type = request.POST.get('file_type')

        expires = int(time.time()+60*5)
        amz_headers = "x-amz-acl:public-read"

        string_to_sign = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

        signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, string_to_sign.encode('utf8'), sha256).digest()).strip()
        # signature = urllib.quote_plus(signature.strip())

        url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)

        return Response(json.dumps({'signed_request': "%s?AWSAccessKeyId=%s&Expires=%s&Signature=%s" % (url, AWS_ACCESS_KEY, expires, signature), 'url': url}), status=status.HTTP_200_OK)
