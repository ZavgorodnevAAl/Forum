from django.contrib import admin
from .models import Profile, FriendRequest, Friend, Post

# Register your models here.
admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Friend)
admin.site.register(Post)