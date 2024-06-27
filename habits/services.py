from django_celery_beat.models import CrontabSchedule, PeriodicTask

import habits.tasks
from config import settings


def create_schedule_and_habit_periodic_task(habit):
    """
    Создание регламентной задачи, которая будет отправлять сообщение
    в Telegram для определенной привычки в определенное время.
    """
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute=habit.time.minute,
        hour=habit.time.hour,
        day_of_week=f'*/{habit.period}',
        month_of_year='*',
        time_zone=settings.TIME_ZONE,
    )

    PeriodicTask.objects.create(
        crontab=schedule,
        name=f'HabitTask{habit.id}',
        task='habits.tasks.send_telegram_message',
        args=[habit.id],
    )


def update_habit_periodic_task(habit):
    """
    Обновление периодической задачи, связанной с конкретной привычкой (habit).
    """
    delete_habit_periodic_task(habit)
    create_schedule_and_habit_periodic_task(habit)


def delete_habit_periodic_task(habit):
    """
    Удаление периодической задачи, связанной с конкретной привычкой (habit).
    """
    PeriodicTask.objects.filter(name=f'HabitTask{habit.id}').delete()
