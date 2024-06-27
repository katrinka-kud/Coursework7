from rest_framework import serializers

from habits.models import Habit
from habits.validators import related_habit_or_reward, execution_time_no_more_120_seconds, \
    only_nice_habit_into_related_habit, nice_habit_cannot_have_reward_or_related_habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Привычка.
    """
    class Meta:
        model = Habit
        exclude = ('owner',)

        validators = [
            related_habit_or_reward,
            execution_time_no_more_120_seconds,
            only_nice_habit_into_related_habit,
            nice_habit_cannot_have_reward_or_related_habit,
        ]

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user

        return super().create(validated_data)
