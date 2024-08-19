from django.urls import path
from .views import index, download_video

urlpatterns = [
    path('', index, name='index'),
    path('download/', download_video, name='download_video'),
]