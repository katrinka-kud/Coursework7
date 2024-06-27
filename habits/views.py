from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginations import HabitsPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer
from habits.services import create_schedule_and_habit_periodic_task, update_habit_periodic_task


class HabitListAPIView(generics.ListAPIView):
    """
    Предоставление точки доступа к списку привычек для конкретного пользователя.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HabitSerializer
    pagination_class = HabitsPagination

    def get_queryset(self):
        """
        Получение только тех привычек, которые принадлежат текущему пользователю.
        """
        return Habit.objects.filter(owner=self.request.user)


class HabitCreateAPIView(generics.CreateAPIView):
    """
    Создание новых привычек.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        """
        После сохранения новой привычки вызывается функция, которая создает периодическое задание для данной привычки.
        """
        new_habit = serializer.save()
        create_schedule_and_habit_periodic_task(new_habit)


class HabitViewAPIView(generics.RetrieveAPIView):
    """
    Получение информации о конкретной привычке, с учетом указанных прав доступа и формата предоставления данных.
    """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    Для обновления данных объекта модели Привычка.
    """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_update(self, serializer):
        """
        После успешного обновления, вызывается функция, которая обновляет периодическую задачу для данной привычки.
        """
        new_habit = serializer.save()
        update_habit_periodic_task(new_habit)


class HabitDeleteAPIView(generics.DestroyAPIView):
    """
    Удаление конкретной привычки с учетом прав доступа и сериализации данных.
    """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitPublicListAPIView(generics.ListAPIView):
    """
    Получение списка публичных привычек.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HabitSerializer

    def get_queryset(self):
        """
        Возвращает список объектов модели Привычка, где только публичные привычки.
        """
        return Habit.objects.filter(is_public=True)
