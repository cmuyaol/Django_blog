from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save

from django.utils.text import slugify

# Create your models here.
# MVC MODEL VIEW CONTROLLER


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" %(instance.id, instance.id, extension)


class Post(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, 
        width_field="width_field",
        height_field="height_field")
    height_field = models.IntegerField(default=9)
    width_field = models.IntegerField(default=9)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-id", "-timestamp", "-updated"]




def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)