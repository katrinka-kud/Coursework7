from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginations import HabitsPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HabitSerializer
    pagination_class = HabitsPagination

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class HabitCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HabitSerializer


class HabitViewAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitPublicListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
