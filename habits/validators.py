from datetime import timedelta

from rest_framework import serializers


def related_habit_or_reward(self):
    if self.related_habit and self.reward:
        raise serializers.ValidationError('Нельзя одновременно указывать связанную привычку и вознаграждение.')


def execution_time_no_more_120_seconds(value):
    if value['time_execution'] > timedelta(seconds=120):
        raise serializers.ValidationError('Время на выполнение не должно превышать 120 секунд.')


def only_nice_habit_into_related_habit(value):
    if value.get('related_habit') and not value['related_habit'].nice_habit:
        raise serializers.ValidationError(
            'В связанные привычки могут попадать только привычки с признаком приятной привычки.')


def nice_habit_cannot_have_reward_or_related_habit(value):
    if value['nice_habit'] and value.get('reward') or value.get('related_habit'):
        raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')
