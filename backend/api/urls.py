from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .v1.consumers import NotificationConsumer

urlpatterns = [
    path('v1/', include('api.v1.urls')),
    path('schema/download/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

websocket_urlpatterns = [
    path('api/v1/notifications/', NotificationConsumer.as_asgi()),
]
