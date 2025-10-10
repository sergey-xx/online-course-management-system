from django.contrib import admin
from django.urls import include, path

from .views import trigger_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('sentry-debug/', trigger_error),
]
