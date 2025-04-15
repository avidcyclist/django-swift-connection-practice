from django.db import models
from django.contrib.auth.models import User  # Assuming Player is tied to the User model
from django.core.validators import MinValueValidator
from django.utils.timezone import now
# Create your models here.

class Workout(models.Model):
    exercise = models.CharField(max_length=100)
    youtube_link = models.URLField(blank=True, null=True)  # Optional field for YouTube link
    
    def __str__(self):
        return self.exercise
    
class Phase(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)  # Ensure name is required

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    password_changed = models.BooleanField(default=False)  # Track if the password has been changed  
    
class PhaseWorkout(models.Model):
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    reps = models.IntegerField(validators=[MinValueValidator(1)])  # Ensure reps are >= 1
    sets = models.IntegerField(validators=[MinValueValidator(1)])  # Ensure sets are >= 1
    week = models.IntegerField()
    day = models.IntegerField()
    order = models.IntegerField()
    default_rpe = models.JSONField()

    def __str__(self):
        return f"{self.phase.name} - {self.workout.exercise} ({self.sets} sets x {self.reps} reps)"
    
    
class Corrective(models.Model):
    name = models.CharField(max_length=100)  # Name of the corrective exercise
    sets = models.IntegerField(null=True, blank=True)  # Optional: Number of sets
    reps = models.IntegerField(null=True, blank=True)  # Optional: Number of reps
    youtube_link = models.URLField(max_length=200, null=True, blank=True)  # Optional: YouTube link for explanation

    def __str__(self):
        return self.name
    
class ActiveWarmup(models.Model):
    name = models.CharField(max_length=100)  # Name of the active warmup exercise
    youtube_link = models.URLField(max_length=200, null=True, blank=True)  # Optional: YouTube link for explanation

    def __str__(self):
        return self.name


class PowerCNSWarmup(models.Model):
    name = models.CharField(max_length=100)  # Name of the warmup (e.g., "Day 1 Power CNS Warmup")
    day = models.IntegerField()  # Day number (e.g., 1, 2, 3, 4)
    youtube_link = models.URLField(max_length=200, null=True, blank=True)  # Optional: YouTube link for explanation

    def __str__(self):
        return f"{self.name} (Day {self.day})"

class ArmCareRoutine(models.Model):
    name = models.CharField(max_length=255)  # e.g., "Day 1 Arm Care Routine"
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return self.name


class PowerCNSExercise(models.Model):
    warmup = models.ForeignKey(PowerCNSWarmup, on_delete=models.CASCADE, related_name="exercises")  # Link to the warmup
    name = models.CharField(max_length=100)  # Name of the exercise
    youtube_link = models.URLField(max_length=200, null=True, blank=True)  # Optional: YouTube link for explanation

    def __str__(self):
        return f"{self.name} ({self.warmup.name})"
    
class ThrowingActiveWarmup(models.Model):
    name = models.CharField(max_length=100)  # Name of the throwing-specific warmup drill
    youtube_link = models.URLField(max_length=200, null=True, blank=True)  # Optional: YouTube link for explanation
    sets_reps = models.CharField(max_length=50, null=True, blank=True)  # New field for sets and reps (e.g., "1x20", "15 sec each")
    
    def __str__(self):
        return self.name


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=100, blank=True)  # Allow blank values
    last_name = models.CharField(max_length=100, blank=True)   # Allow blank values
    email = models.EmailField(unique=True, default="default@example.com")
    age = models.IntegerField(null=True, blank=True)  # Allow NULL values
    team = models.CharField(max_length=100, blank=True, default="")  # Default to an empty string
    correctives = models.ManyToManyField(Corrective, blank=True, related_name="players")  # Many-to-Many relationship
    active_warmup = models.ManyToManyField(ActiveWarmup, blank=True, related_name="players")  # Many-to-Many relationship
    power_cns_warmups = models.ManyToManyField(PowerCNSWarmup, blank=True, related_name="players")  # Many-to-Many relationship
    throwing_active_warmups = models.ManyToManyField(ThrowingActiveWarmup, blank=True, related_name="players")
    arm_care_routines = models.ManyToManyField(ArmCareRoutine, blank=True, related_name="players")  # New field
   
    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Display full name in the admin panel
    
    
class PlayerPhase(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)  # Link to a player
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)    # Link to a phase
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.player.first_name} - {self.phase.name}"

    def save(self, *args, **kwargs):
        # Check if this is an update and the phase has changed
        if self.pk:  # If the instance already exists (not a new one)
            old_phase = PlayerPhase.objects.get(pk=self.pk).phase
            if old_phase != self.phase:  # If the phase has changed
                # Delete existing PlayerPhaseWorkout entries
                from .models import PlayerPhaseWorkout, PhaseWorkout  # Avoid circular imports
                PlayerPhaseWorkout.objects.filter(player_phase=self).delete()

                # Repopulate PlayerPhaseWorkout with defaults from the new phase
                phase_workouts = PhaseWorkout.objects.filter(phase=self.phase)
                for workout in phase_workouts:
                    PlayerPhaseWorkout.objects.create(
                        player_phase=self,
                        workout=workout.workout,
                        reps=workout.reps,
                        sets=workout.sets,
                        week=workout.week,
                        day=workout.day,
                        order=workout.order,
                        rpe=workout.default_rpe,
                        player_rpe=[None] * len(workout.default_rpe)  
                    )

        # Save the PlayerPhase instance
        super().save(*args, **kwargs)
    
class WorkoutLog(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)  # Link to the phase
    week = models.IntegerField()  # Week number within the phase
    day = models.IntegerField()   # Day number within the week
    exercises = models.JSONField()  # Store all exercises and their sets as a JSON object
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the log is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update when the log is modified

    class Meta:
        unique_together = ('player', 'phase', 'week', 'day')  # Ensure no duplicate logs for the same week/day

    def __str__(self):
        return f"{self.player.user.username} - Phase: {self.phase.name}, Week: {self.week}, Day: {self.day}"
    
    
class PlayerPhaseWorkout(models.Model):
    player_phase = models.ForeignKey(
        PlayerPhase, 
        on_delete=models.CASCADE, 
        related_name="player_phase_workouts"
    )  # Link to the player's phase
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)  # Link to the workout
    reps = models.IntegerField()  # Custom reps for this workout
    sets = models.IntegerField()  # Custom sets for this workout
    week = models.IntegerField()  # Week of the phase (1, 2, 3, etc.)hen
    day = models.IntegerField()  # Day of the phase (1, 2, 3, etc.)
    order = models.IntegerField(default=1)  # Order of the workout in the day
    rpe = models.JSONField(default=list)  # Custom RPE values
    player_rpe = models.JSONField(default=list, blank=True)  # Player-entered RPE values (mutable)

    def __str__(self):
        return f"{self.player_phase.player.first_name} - {self.workout.exercise} ({self.sets} sets x {self.reps} reps)"
    
    
    
class ThrowingRoutine(models.Model):
    name = models.CharField(max_length=255)  # e.g., "Plyo Routines"
    description = models.TextField(blank=True, null=True)  # Optional description


    def __str__(self):
        return self.name


class Drill(models.Model):
    routine = models.ForeignKey(ThrowingRoutine, on_delete=models.CASCADE, related_name="drills")
    name = models.CharField(max_length=255, blank=True, null=True)  # e.g., "Reverse Throws"
    sets_reps = models.CharField(max_length=50, blank=True, null=True)  # e.g., "2x10"
    weight = models.CharField(max_length=50, blank=True, null=True)  # e.g., "2lb"
    distance = models.CharField(max_length=50, blank=True, null=True)  # e.g., "60ft"
    throws = models.CharField(max_length=50, blank=True, null=True)  # e.g., "5-15"
    rpe = models.CharField(max_length=50, blank=True, null=True)  # e.g., "80-90%"
    video_link = models.URLField(blank=True, null=True)  # Optional instructional video

    def __str__(self):
        return f"{self.routine.name} - {self.name}"
    
class ThrowingProgram(models.Model):
    name = models.CharField(max_length=255)  # e.g., "In Season: Starter"

    def __str__(self):
        return self.name
    
class ThrowingProgramDay(models.Model):
    program = models.ForeignKey(ThrowingProgram, on_delete=models.CASCADE, related_name="days")
    week_number = models.IntegerField()  # e.g., "Week 1"
    day_number = models.IntegerField()  # e.g., "Day 1"
    name = models.CharField(max_length=255, blank=True, null=True)  # e.g., "GAME DAY"
    warmup = models.TextField(blank=True, null=True)  # e.g., "WU, ACT"
    plyos = models.TextField(blank=True, null=True) # Reference routines
    throwing = models.TextField(blank=True, null=True)  # e.g., "Long Toss to Preferred Distance"
    velo_command = models.TextField(blank=True, null=True)  # e.g., "3-5 Pulldowns"
    arm_care = models.TextField(blank=True, null=True)  # e.g., "Light Recovery"
    lifting = models.TextField(blank=True, null=True)  # e.g., "Day 1 Lift"
    conditioning = models.TextField(blank=True, null=True)  # e.g., "15min bike"

    def __str__(self):
        return f"{self.program.name} - Day {self.day_number}: {self.name}"
    
class PlayerThrowingProgram(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="throwing_programs")
    program = models.ForeignKey(ThrowingProgram, on_delete=models.CASCADE)  # Link to the base program
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name} - {self.program.name}"
    
class PlayerThrowingProgramDay(models.Model):
    player_program = models.ForeignKey(PlayerThrowingProgram, on_delete=models.CASCADE, related_name="days")
    week_number = models.IntegerField()  # e.g., "Week 1"
    day_number = models.IntegerField()  # e.g., "Day 1"
    name = models.CharField(max_length=255, blank=True, null=True)  # e.g., "GAME DAY"
    warmup = models.TextField(blank=True, null=True)  # e.g., "WU, ACT"
    plyos = models.TextField(blank=True, null=True) #
    throwing = models.TextField(blank=True, null=True)  # e.g., "Long Toss to Preferred Distance"
    velo_command = models.TextField(blank=True, null=True)  # e.g., "3-5 Pulldowns"
    arm_care = models.TextField(blank=True, null=True)  # e.g., "Light Recovery"
    lifting = models.TextField(blank=True, null=True)  # e.g., "Day 1 Lift"
    conditioning = models.TextField(blank=True, null=True)  # e.g., "15min bike"

    def __str__(self):
        return f"{self.player_program.player.first_name} {self.player_program.player.last_name}- Day {self.day_number}: {self.name}"



class ArmCareExercise(models.Model):
    routine = models.ForeignKey(ArmCareRoutine, on_delete=models.CASCADE, related_name="exercises")
    day = models.IntegerField(validators=[MinValueValidator(1)])  # Ensure day is >= 1
    focus = models.CharField(max_length=255, blank=True, null=True)
    exercise = models.CharField(max_length=255)
    sets_reps = models.CharField(max_length=50, blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.routine.name} - {self.exercise}"
    
    
class PlayerArmCareRoutine(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player_arm_care_routines")
    routine = models.ForeignKey(ArmCareRoutine, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name} - {self.routine.name}"

    def save(self, *args, **kwargs):
        # Check if this is a new instance or if the routine has changed
        is_new = self.pk is None
        old_routine = None
        if not is_new:
            old_routine = PlayerArmCareRoutine.objects.get(pk=self.pk).routine

        super().save(*args, **kwargs)  # Save the routine first

        # If the routine is new or has changed, update the exercises
        if is_new or old_routine != self.routine:
            # Delete existing exercises for this routine
            PlayerArmCareExercise.objects.filter(routine=self).delete()

            # Copy exercises from the base routine
            for exercise in self.routine.exercises.all():
                PlayerArmCareExercise.objects.create(
                    routine=self,
                    day=exercise.day,
                    focus=exercise.focus,
                    exercise=exercise.exercise,
                    sets_reps=exercise.sets_reps,
                    youtube_link=exercise.youtube_link,
                )
    
class PlayerArmCareExercise(models.Model):
    routine = models.ForeignKey(PlayerArmCareRoutine, on_delete=models.CASCADE, related_name="exercises")
    day = models.IntegerField()  # e.g., "1" for Day 1    
    focus = models.CharField(max_length=255, blank=True, null=True)  # e.g., "Shoulder/Cuff Strength"
    exercise = models.CharField(max_length=255)  # e.g., "Crossover Symmetry"
    sets_reps = models.CharField(max_length=50, blank=True, null=True)  # e.g., "1x10"
    youtube_link = models.URLField(blank=True, null=True)  # Optional instructional video link

    def __str__(self):
        return f"{self.routine.routine.name} - {self.exercise}"
    
    
class DailyIntake(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="daily_intakes")
    date = models.DateField(default=now)  # Default to today's date
    arm_feel = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])  # 1-5 scale
    body_feel = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])  # 1-5 scale
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # e.g., 7.5 hours
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # e.g., 180.5 lbs
    met_calorie_macros = models.BooleanField(default=False)  # Checkbox for meeting calorie/macros
    completed_day_plan = models.BooleanField(default=False)  # Checkbox for completing the day's plan
    comments = models.TextField(blank=True, null=True)  # Optional comments/notes

    class Meta:
        unique_together = ('player', 'date')  # Ensure one log per player per day

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name} - {self.date}"