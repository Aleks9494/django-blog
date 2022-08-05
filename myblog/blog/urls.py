
from django.urls import path

from .views import *

app_name = 'api'

urlpatterns = [
    path('posts', PostsApiView.as_view(), name='posts'),
    path('users', UsersApiView.as_view(), name='users'),
    path('posts/<int:pk>', SubsriptionUserApiView.as_view(), name='subs'),
    path('subs', SubscriptionsListApiView.as_view(), name='usersubs'),
    path('subs/<int:pk>', SubApiView.as_view(), name = 'usersub' )
]