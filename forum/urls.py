from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^register/$', views.register, name='register'),

    path('user_profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='user_profile'),
    path('create_profile_page/', views.CreateProfilePageView.as_view(), name='create_user_profile'),
    path('update_user_profile/<int:pk>/', views.UpdateProfilePageView.as_view(), name='update_user_profile'),
    re_path(r'^send_request/(?P<spk>\d+)/(?P<rpk>\d+)/$', views.send_request, name='send_request'),
    re_path(r'^friend_requests/$', views.UserFriendRequests.as_view(), name='user_friend_requests'),
    re_path(r'^connect/(?P<operation>.+)/(?P<pk>\d+)$', views.change_friend, name='change_friend'),
    re_path(r'^friends/$', views.FriendList.as_view(), name='friends'),
    re_path(r'^all_users/$', views.AllUserList.as_view(), name='all_users'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)