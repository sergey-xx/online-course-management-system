from abc import ABC

from django.contrib.auth import get_user_model
from django.db.models import Model

User = get_user_model()


class AuthorService(ABC):
    model: type[Model]

    def __init__(self, author: User):
        """Initializes the service with the user performing the action."""
        if not author or not author.is_authenticated:
            raise ValueError("Author must be an authenticated user.")
        self.author = author

    def create(self, **kwargs) -> Model:
        return self.model.objects.create(author=self.author, **kwargs)

    def update(self, instance: Model, **kwargs) -> Model:
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance: Model):
        instance.delete()
