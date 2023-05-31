from django.urls import path

from events import views

urlpatterns = [
    path('', views.EventViewSet.as_view({'get': 'list', 'post': 'create'})),
]
