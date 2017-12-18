from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('feed/', views.Feed.as_view(), name='feed'),
    path('upload/', views.Upload.as_view(), name='upload'),
    path('filter/<img_id>/', views.Filter.as_view(), name='filter'),
    path('rotate/<img_id>/', views.Rotate.as_view(), name='rotate'),
    path('delete/<img_id>/', views.Delete_Picture.as_view(), name='delete')
]
