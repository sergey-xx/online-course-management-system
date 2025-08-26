from typing import Type


class ServiceViewMixin:
    """Overrides creation, update and delete methods not to use serializer."""

    service_class: Type

    def get_service(self):
        return self.service_class(self.request.user)

    def perform_create(self, serializer):
        """Set the user who created the course as the author."""
        service = self.get_service()
        serializer.instance = service.create(**serializer.validated_data)

    def perform_update(self, serializer):
        service = self.get_service()
        serializer.instance = service.update(serializer.instance, **serializer.validated_data)

    def perform_destroy(self, instance):
        service = self.get_service()
        service.delete(instance)
