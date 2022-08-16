from django.urls import path

from .views import (CategoryDetailView, CategoryListView, LeadDetailApiView,
                    LeadsListApiView, api_root)

urlpatterns = [
    path("", api_root),
    path("leads/", LeadsListApiView.as_view(), name="leads"),
    path("leads/<int:pk>/", LeadDetailApiView.as_view()),
    path("category/", CategoryListView.as_view(), name="categories"),
    path("category/<int:pk>/", CategoryDetailView.as_view()),
]
