from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faceform', views.newImage, name='faceform'),
    path('imagelist/<int:pk>', views.imageList, name='imagelist'),
    path('delete_image/<int:pk>', views.delete_image, name='delete_image'),
    path('train', views.train, name='train'),
    path('recognize', views.recognize, name='recognize'),
    path('testimage', views.testImage, name='testimage'),
]
