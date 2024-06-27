from django.core.management import BaseCommand

from habits.tasks import send_telegram_message


class Command(BaseCommand):
    """
    Тестирование отправки сообщений в Телеграм.
    """
    def handle(self, *args, **options):
        send_telegram_message(1)
