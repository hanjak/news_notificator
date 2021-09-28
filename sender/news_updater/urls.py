from django.urls import path
from . import views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

app_name = 'news_updater'

urlpatterns = [
    path('', views.index, name='index'),
    ]

handler404 = 'news_updater.views.error_404'