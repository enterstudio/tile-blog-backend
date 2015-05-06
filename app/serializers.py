from django.http import Http404
from django.contrib.auth import authenticate
from rest_framework import serializers, status, renderers, parsers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Post, Image, Blogger
from django.utils import timezone
import urllib2
import json


__author__ = 'fuiste'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image


class BloggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogger


class PostList(APIView):
    model = Post
    serializer_class = PostSerializer

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.DATA)
        if serializer.is_valid():
            post = serializer.save()
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageList(APIView):
    model = Image
    serializer_class = ImageSerializer

    def get(self, request, format=None):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.DATA)
        if serializer.is_valid():
            post = serializer.save()
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BloggerDetail(APIView):
    model = Blogger
    serializer_class = BloggerSerializer

    def get_object(self, pk):
        try:
            return Blogger.objects.get(pk=pk)
        except Blogger.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tgt = self.get_object(pk)
        serializer = BloggerSerializer(tgt)
        return Response(serializer.data)


class PostDetail(APIView):
    model = Post
    serializer_class = PostSerializer

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tgt = self.get_object(pk)
        serializer = PostSerializer(tgt)
        return Response(serializer.data)

    def put( self, request, pk, format=None):
        tgt = self.get_object(pk)
        serializer = PostSerializer(tgt, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class ImageDetail(APIView):
    model = Image
    serializer_class = ImageSerializer

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tgt = self.get_object(pk)
        serializer = ImageSerializer(tgt)
        return Response(serializer.data)
