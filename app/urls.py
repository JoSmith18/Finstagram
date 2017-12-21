from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('feed/', views.Feed.as_view(), name='feed'),
    path('upload/', views.Upload.as_view(), name='upload'),
    path('uploadvideo/', views.Upload_Video.as_view(), name='uploadvideo'),
    path('filter/<doc_id>/', views.Filter.as_view(), name='filter'),
    path('rotate/<doc_id>/', views.Rotate.as_view(), name='rotate'),
    path('delete/<doc_id>/', views.Delete_Picture.as_view(), name='delete'),
    path(
        'deletevideo/<doc_id>/',
        views.Delete_Video.as_view(),
        name='deletevideo'),
    path(
        'comment/<document_id>/', views.Add_Comment.as_view(), name='comment'),
    path(
        'commentvideo/<document_id>/',
        views.Add_Comment_Video.as_view(),
        name='commentvideo'),
    path('likepic/<doc_id>/', views.Like_Pic.as_view(), name='likepic'),
    path('likevideo/<doc_id>/', views.Like_Vid.as_view(), name='likevideo'),
    path(
        'dislikepic/<doc_id>/', views.DisLike_Pic.as_view(),
        name='dislikepic'),
    path(
        'dislikevideo/<doc_id>/',
        views.DisLike_Vid.as_view(),
        name='dislikevideo')
]
