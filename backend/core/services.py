from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.db.models import Model

User = get_user_model()


class AuthorService(ABC):

    def __init__(self, author: User):
        """
        Initializes the service with the user performing the action.
        """
        if not author or not author.is_authenticated:
            raise ValueError("Author must be an authenticated user.")
        self.author = author

    @abstractmethod
    def create(self, *args, **kwargs) -> Model:
        ...
