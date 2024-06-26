from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        exclude = ('owner',)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user

        return super().create(validated_data)
