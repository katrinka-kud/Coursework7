from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'action', 'nice_habit', 'period')
    list_filter = ('owner', 'action')
    search_fields = ('owner', 'action')
