from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (LeadDetailApiView,
                    LeadsListApiView, CategoryViewSet)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    # path("", api_root),
    path("leads/", LeadsListApiView.as_view(), name="leads"),
    path("leads/<int:pk>/", LeadDetailApiView.as_view()),
    path('', include(router.urls))
    # path("category/", CategoryListView.as_view(), name="categories"),
    # path("category/<int:pk>/", CategoryDetailView.as_view()),
]
