from django.urls import path

from habits.views import HabitListAPIView, HabitCreateAPIView, HabitViewAPIView, HabitUpdateAPIView, HabitDeleteAPIView, \
    HabitPublicListAPIView

urlpatterns = [
    path('list/', HabitListAPIView.as_view(), name='habit-list'),
    path('create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('view/<int:pk>/', HabitViewAPIView.as_view(), name='habit-view'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('delete/<int:pk>/', HabitDeleteAPIView.as_view(), name='habit-delete'),
    path('list_public/<int:pk>/', HabitPublicListAPIView.as_view(), name='habit-list-public'),
]
