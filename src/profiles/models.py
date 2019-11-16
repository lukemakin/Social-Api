from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.defaultfilters import slugify
import random
# Create your models here.


class ProfileManager(models.Manager):
    def get_random_profiles(self, sender):
        return self.filter(~Q(user=sender)).order_by("?")

    def get_people_to_invite(self, sender):
        qs = Relationship.objects.filter(sender=sender)
        qs_all = Profile.objects.get_random_profiles(sender)
        qs_filtered = filter(lambda x: x.status !=
                             'send' or x.status != 'accepted', qs)
        invites = []
        for profile in qs_filtered:
            invites.append(profile.receiver)

        available = [item for item in qs_all if item not in invites]
        return available


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=360,  blank=True, default="no bio...")
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(blank=True, null=True, default='avatar.png')
    friends = models.ManyToManyField('self', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return "{}".format(self.user.username)

    @property
    def get_friends(self):
        return self.friends.all()

    @property
    def get_friends_no(self):
        return self.friends.all().count()

    @property
    def get_slug(self):
        val = self.first_name+' '+self.last_name
        qs = Profile.objects.filter(user=self.user)
        if qs.exists():
            slug = val + ' ' + random.randint(0, 9999)
        else:
            slug = slugify(val)
        return slug


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
    ('declined', 'declined'),
    ('deleted', 'deleted'),
)


class RelationshipManager(models.Manager):
    def invations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver)
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(choices=STATUS_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return "{}-{}-{}".format(self.sender, self.receiver, self.status)
