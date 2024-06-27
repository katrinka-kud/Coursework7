from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Пользователь.
    """

    class Meta:
        model = User
        fields = ['email', 'password', 'chat_id', 'is_active']

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.chat_id = validated_data['chat_id']
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user
