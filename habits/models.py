from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    PERIOD_DAY_1 = 1
    PERIOD_DAY_2 = 2
    PERIOD_DAY_3 = 3
    PERIOD_DAY_4 = 4
    PERIOD_DAY_5 = 5
    PERIOD_DAY_6 = 6
    PERIOD_DAY_7 = 7

    PERIODICITY = (
        (PERIOD_DAY_1, 'раз в день'),
        (PERIOD_DAY_2, 'раз в 2 дня'),
        (PERIOD_DAY_3, 'раз в 3 дня'),
        (PERIOD_DAY_4, 'раз в 4 дня'),
        (PERIOD_DAY_5, 'раз в 5 дня'),
        (PERIOD_DAY_6, 'раз в 6 дня'),
        (PERIOD_DAY_7, 'раз в неделю'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец')
    place = models.CharField(max_length=300, verbose_name='место')
    time = models.TimeField(**NULLABLE, verbose_name='время')
    action = models.CharField(max_length=300, verbose_name='действие')
    nice_habit = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE, verbose_name='связанная привычка')
    period = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)], default=PERIOD_DAY_1,
                                 choices=PERIODICITY, verbose_name='периодичность')
    reward = models.CharField(max_length=300, **NULLABLE, verbose_name='вознаграждение')
    time_execution = models.IntegerField(default=timedelta(seconds=120), verbose_name='время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='публичная')

    def __str__(self):
        return f'{self.action} - {self.owner}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
