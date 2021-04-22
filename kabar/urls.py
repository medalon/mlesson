
from django.urls import path
from kabar.views import index


urlpatterns = [
    path('', index, name='home')
]