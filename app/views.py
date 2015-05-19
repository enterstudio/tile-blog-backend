from django.shortcuts import render
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status, renderers, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FileUploadParser
from app.models import Blogger
import time, os, json, base64, hmac, urllib, boto, sys, string, random
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

class UpdateUsernameView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        if request.auth:
            new_name = request.POST.get('new_name')
            if new_name:
                request.user.username = new_name
                request.user.save
                return Response({"username": request.user.username}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You need to be logged in to do that..."}, status=status.HTTP_403_FORBIDDEN)


class UploadImageView(APIView):
    authentication_classes = (TokenAuthentication,)
    parser_classes = (FileUploadParser,)

    def post(self, request):
        # Grab the uploaded file
        file = request.data['file']

        # Grab AWS creds
        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')
        BUCKET_NAME = os.environ.get('S3_BUCKET')

        # Connect to AWS and grab our bucket
        conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(BUCKET_NAME)

        # Generate new filename and upload to s3
        filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        k = Key(bucket)
        k.key = "{0}.{1}".format(filename, file.name.split('.')[1])
        k.set_contents_from_file(file)
        k.make_public()
        http_url = "http://{0}.{1}/{2}".format(BUCKET_NAME, conn.server_name(), k.key)

        # Return the location to ember
        return Response({"url": http_url}, status=status.HTTP_200_OK)
