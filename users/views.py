from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """
    Создание новых пользователей без ограничений на доступ к данному эндопоинту.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
