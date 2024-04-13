from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_pan, name='upload_pan'),  # Upload Image URL
    path('result/', views.result, name='result'),  # Result URL
]
