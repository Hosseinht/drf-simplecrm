from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/auth/', include('djoser.urls'), ),
    path('api/auth/', include('djoser.urls.jwt')),
    path("api/", include('leads.urls')),
    # path("api/", include('leads.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
