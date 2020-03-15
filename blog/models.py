from django.db import models
from tinymce.models import HTMLField
from django.shortcuts import reverse
from django.contrib.auth.models import User
from core.models import Profile

CATEGORY_OPTION = (
    ('NS', 'news'),
    ('TM', 'tourism')
)


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    heading = models.TextField(max_length=2000)
    content = HTMLField('Content')
    thumbnail = models.ImageField(blank=True, upload_to='post/%Y/%m/')
    slug = models.SlugField(blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    category = models.CharField(
        max_length=2, choices=CATEGORY_OPTION, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("blog-delete", kwargs={"slug": self.slug})

    def delete(self, *args, **kwargs):
        if self.thumbnail:
            self.thumbnail.delete()
        super().delete(*args, **kwargs)

    @property
    def get_comments(self):
        return self.post_comment.all()


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(max_length=5000, blank=True, null=True)
    post = models.ForeignKey(
        Post, related_name='post_comment', on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
