from django.urls import path
from . import views


app_name = 'news'

urlpatterns = [
    #path('', views.news_list, name='news_list'),
    path('', views.NewsListView.as_view(), name='news_list'),
    path('news_list/', views.news_list, name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:news>/',
            views.news_detail,
            name='news_detail'),
    path('<int:news_id>/share/', views.news_share, name='news_share'),
]