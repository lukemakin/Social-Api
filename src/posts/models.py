from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse
from profiles.models import Profile
import random


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='post_img')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='profile')
    slug = models.SlugField(blank=True, unique=True)
    liked = models.ManyToManyField(
        User, blank=True, related_name="liked")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def get_absolute_url(self):
        return reverse("posts-api:post-detail", kwargs={"slug": self.slug})

    @property
    def no_of_likes(self):
        return self.liked.all().count()

    @property
    def no_of_comments(self):
        try:
            comments = Comment.objects.filter(post=self)
            size = comments.all().count()
        except:
            size = 0
        return size

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        posts = Post.objects.filter(slug=self.slug)
        if posts.exists():
            num = str(random.randint(0, 9999))
            self.slug = slugify(self.title+" "+num)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    body = models.TextField(max_length=360)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.body[:50], self.author)

    class Meta:
        ordering = ('-created',)
