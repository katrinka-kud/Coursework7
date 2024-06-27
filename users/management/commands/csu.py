from os import getenv

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email=getenv('ADMIN_EMAIL'),
                                   chat_id=getenv('TELEGRAM_CHAT_ID'),)
        user.set_password(getenv('ADMIN_PASSWORD'))
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
