from django_elasticsearch_dsl import Document


class ServiceViewMixin:
    """Overrides creation, update and delete methods not to use serializer."""

    service_class: type

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


class SearchViewMixin:
    document_class: type[Document]
    search_fields: tuple["str"]
    search_query_parameter: str = "search"

    def get_search_kwargs(self, value):
        return dict.fromkeys(self.search_fields, value)

    def get_search_ids(self, value):
        s = self.document_class.search().query("match", **self.get_search_kwargs(value))
        s = s.source(False)
        try:
            pks = [int(hit.meta.id) for hit in s.execute()]
        except Exception:
            pks = []
        return pks

    def get_search_queryset(self, queryset):
        if self.search_query_parameter in self.request.query_params:
            value = self.request.query_params[self.search_query_parameter]
            queryset = queryset.filter(pk__in=self.get_search_ids(value))
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.get_search_queryset(queryset)
