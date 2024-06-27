from celery import shared_task
from requests import post

from config import settings
from habits.models import Habit


@shared_task
def send_telegram_message(habit_id):
    """
    Отправление  сообщения в Telegram с информацией о привычке (habit) пользователя.
    """
    habit = Habit.objects.get(id=habit_id)
    post(
        params={
            'text': f'Я буду {habit.action} в {habit.time} в {habit.place}',
            'chat_id': habit.owner.chat_id,
        },
        url=f'{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage'
    )
