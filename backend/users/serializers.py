from djoser.serializers import UserCreateSerializer

from .models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "password",
            'role',
        )
