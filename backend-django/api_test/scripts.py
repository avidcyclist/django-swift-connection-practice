from api_test.models import WorkoutLog
from django.db.models import Count

def remove_duplicate_workout_logs():
    # Find duplicate logs based on player, week, and day
    duplicates = (
        WorkoutLog.objects.values('player', 'week', 'day')
        .annotate(count=Count('id'))
        .filter(count__gt=1)
    )

    for duplicate in duplicates:
        logs = WorkoutLog.objects.filter(
            player=duplicate['player'],
            week=duplicate['week'],
            day=duplicate['day']
        )
        print(f"Duplicate found for player={duplicate['player']}, week={duplicate['week']}, day={duplicate['day']}")
        print(f"Logs to delete: {[log.id for log in logs[1:]]}")  # Log IDs of duplicates

        # Keep the first log and delete the rest
        logs.exclude(id=logs.first().id).delete()

    print("Duplicate workout logs removed.")