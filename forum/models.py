from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField("first name", max_length=100)
    last_name = models.CharField("last name", max_length=100)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True)
    twitter = models.CharField(max_length=50, null=True, blank=True)
    instagram = models.CharField(max_length=50, null=True, blank=True)

    SEX_STATUS = (
        ('m', 'male'),
        ('f', 'female'),
    )

    sex = models.CharField(max_length=1, choices=SEX_STATUS, blank=True, default='m')

    def __str__(self):
        return str(self.user)


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)
        new_friend, new_created = cls.objects.get_or_create(
            current_user=new_friend
        )
        new_friend.users.add(current_user)

    @classmethod
    def lose_friend(cls, current_user, ex_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(ex_friend)
        new_friend, new_created = cls.objects.get_or_create(
            current_user=ex_friend
        )
        new_friend.users.remove(ex_friend)

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient', on_delete=models.CASCADE)