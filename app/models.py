from django.db import models
from django.utils import timezone
from custom_user.models import AbstractEmailUser

__author__ = "fuiste"

CHARFIELD_MAX_SM = 256
CHARFIELD_MAX_LG = 10000


class Blogger(AbstractEmailUser):
    username = models.CharField(max_length=CHARFIELD_MAX_SM, null=True, blank=True)

    class Meta:
        verbose_name = 'Blogger'
        verbose_name_plural = 'Bloggers'

    def __unicode__(self):
        return '{0} - {1}'.format(self.username, self.email)

    def __str__(self):
        return unicode(self)


class Image(models.Model):
    url = models.CharField(max_length=CHARFIELD_MAX_SM, null=True, blank=True)


class Post(models.Model):
    title = models.CharField(max_length=CHARFIELD_MAX_SM, null=False, default="Untitled")
    description = models.CharField(max_length=CHARFIELD_MAX_LG, null=True, blank=True)
    author = models.CharField(max_length=CHARFIELD_MAX_SM, null=False, default="Anonymous")
    large = models.BooleanField(null=False, default=False)
    full_width = models.BooleanField(null=False, default=False)
    date = models.DateTimeField(null=False, default=timezone.now())
    cover_photo = models.ForeignKey('Image', null=True, blank=True)
    sub_photos = models.ManyToManyField('Image', related_name="image_sub", null=True, blank=True)
