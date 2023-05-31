from django.urls import path

from organizations import views

urlpatterns = [
    path('', views.OrgViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('join/<int:org_id>', views.join_org)
]
