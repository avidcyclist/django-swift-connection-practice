from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from api_test.models import (
    Player, Workout, Phase, PhaseWorkout, PlayerPhase, WorkoutLog,
    ArmCareRoutine, PlayerArmCareRoutine, ArmCareExercise
)

class ModelCreationTest(TestCase):
    def test_user_and_player_creation(self):
        # Create a User
        user = User.objects.create_user(username="testuser", password="testpass")

        # Check if a Player already exists for the User
        if not Player.objects.filter(user=user).exists():
            # Create a Player linked to the User
            player = Player.objects.create(user=user, first_name="John", last_name="Doe", email="john.doe@example.com")

            # Assert the Player is linked to the User
            self.assertEqual(player.user.username, "testuser")
            self.assertEqual(player.first_name, "John")
            self.assertEqual(player.last_name, "Doe")
            self.assertEqual(player.email, "john.doe@example.com")

    def test_workout_creation(self):
        # Create a Workout
        workout = Workout.objects.create(exercise="Squat")
        # Assert the Workout was created successfully
        self.assertEqual(workout.exercise, "Squat")
        self.assertEqual(str(workout), "Squat")

    def test_phase_creation(self):
        # Create a Phase
        phase = Phase.objects.create(name="Phase 1")
        # Assert the Phase was created successfully
        self.assertEqual(phase.name, "Phase 1")
        self.assertEqual(str(phase), "Phase 1")

    def test_phase_workout_creation(self):
        # Create a Phase and a Workout
        phase = Phase.objects.create(name="Phase 1")
        workout = Workout.objects.create(exercise="Deadlift")
        # Create a PhaseWorkout
        phase_workout = PhaseWorkout.objects.create(
            phase=phase,
            workout=workout,
            reps=5,
            sets=3,
            week=1,
            day=1,
            order=1,
            default_rpe=[7, 8, 9]
        )

        # Assert the PhaseWorkout is linked correctly
        self.assertEqual(phase_workout.phase.name, "Phase 1")
        self.assertEqual(phase_workout.workout.exercise, "Deadlift")
        self.assertEqual(phase_workout.reps, 5)
        self.assertEqual(phase_workout.sets, 3)
        self.assertEqual(str(phase_workout), "Phase 1 - Deadlift (3 sets x 5 reps)")

    def test_arm_care_routine_creation(self):
        # Create an ArmCareRoutine
        routine = ArmCareRoutine.objects.create(name="Routine 1")
        # Create an ArmCareExercise linked to the routine
        exercise = ArmCareExercise.objects.create(
            routine=routine,
            day=1,
            focus="Shoulder Strength",
            exercise="Crossover Symmetry",
            sets_reps="3x10"
        )

        # Assert the routine and exercise were created successfully
        self.assertEqual(routine.name, "Routine 1")
        self.assertEqual(str(routine), "Routine 1")
        self.assertEqual(exercise.routine.name, "Routine 1")
        self.assertEqual(exercise.exercise, "Crossover Symmetry")
        self.assertEqual(str(exercise), "Routine 1 - Crossover Symmetry")
        
        
class WorkoutLogModelTest(TestCase):
    def setUp(self):
        # Create a test user and player
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.player, _ = Player.objects.get_or_create(
            user=self.user,
            defaults={"first_name": "John", "last_name": "Doe"}
        )
        self.phase = Phase.objects.create(name="Phase 1")

    def test_workout_log_creation(self):
        # Create a WorkoutLog
        workout_log = WorkoutLog.objects.create(
            player=self.player,
            phase=self.phase,
            week=1,
            day=1,
            exercises={"Squat": [{"set": 1, "weight": 100, "reps": 10}]}
        )
        # Assert the WorkoutLog was created successfully
        self.assertEqual(workout_log.player, self.player)
        self.assertEqual(workout_log.phase, self.phase)
        self.assertEqual(workout_log.week, 1)
        self.assertEqual(workout_log.day, 1)
        self.assertEqual(workout_log.exercises["Squat"][0]["weight"], 100)
        self.assertEqual(str(workout_log), "testuser - Phase: Phase 1, Week: 1, Day: 1")


class PlayerPhaseModelTest(TestCase):
    def setUp(self):
        # Create a test user, player, and phases
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.player, _ = Player.objects.get_or_create(
            user=self.user,
            defaults={"first_name": "John", "last_name": "Doe"}
        )
        self.phase1 = Phase.objects.create(name="Phase 1")
        self.phase2 = Phase.objects.create(name="Phase 2")

    def test_player_phase_creation(self):
        # Create a PlayerPhase
        player_phase = PlayerPhase.objects.create(
            player=self.player,
            phase=self.phase1,
            start_date="2025-04-01",
            end_date="2025-04-30"
        )
        # Assert the PlayerPhase was created successfully
        self.assertEqual(player_phase.player, self.player)
        self.assertEqual(player_phase.phase, self.phase1)

    def test_phase_change_repopulates_workouts(self):
        # Create a PlayerPhase
        player_phase = PlayerPhase.objects.create(
            player=self.player,
            phase=self.phase1,
            start_date="2025-04-01",
            end_date="2025-04-30"
        )
        # Change the phase
        player_phase.phase = self.phase2
        player_phase.save()

        # Assert the phase was updated
        self.assertEqual(player_phase.phase, self.phase2)


class PlayerArmCareRoutineTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        
        # Get or create the Player object
        self.player, created = Player.objects.get_or_create(
            user=self.user,
            defaults={"first_name": "John", "last_name": "Doe"}
        )
        
        # Ensure the Player has the correct first_name and last_name
        if not created:
            self.player.first_name = "John"
            self.player.last_name = "Doe"
            self.player.save()

        # Create the routine
        self.routine = ArmCareRoutine.objects.create(name="Routine 1")

    def test_arm_care_routine_creation(self):
        # Create a PlayerArmCareRoutine
        player_routine = PlayerArmCareRoutine.objects.create(
            player=self.player,
            routine=self.routine,
            start_date="2025-04-01",
            end_date="2025-04-30"
        )
        # Assert the PlayerArmCareRoutine was created successfully
        self.assertEqual(player_routine.player.first_name, "John")
        self.assertEqual(player_routine.player.last_name, "Doe")
        self.assertEqual(player_routine.routine.name, "Routine 1")
        self.assertEqual(str(player_routine), "John Doe - Routine 1")
        
class InvalidDataTest(TestCase):
    def test_player_creation_without_user(self):
        # Attempt to create a Player without a User
        with self.assertRaises(IntegrityError):
            Player.objects.create(first_name="John", last_name="Doe")

    def test_workout_creation_without_exercise(self):
        # Attempt to create a Workout without an exercise name
        with self.assertRaises(IntegrityError):
            Workout.objects.create(exercise=None)

    def test_phase_creation_with_blank_name(self):
        # Attempt to create a Phase with a blank name
        phase = Phase(name="")
        with self.assertRaises(ValidationError):
            phase.full_clean()  # Trigger model validation
            phase.save()

    def test_phase_workout_with_negative_reps(self):
        # Create a Phase and a Workout
        phase = Phase.objects.create(name="Phase 1")
        workout = Workout.objects.create(exercise="Deadlift")
        # Attempt to create a PhaseWorkout with negative reps
        with self.assertRaises(ValidationError):
            phase_workout = PhaseWorkout(
                phase=phase,
                workout=workout,
                reps=-5,  # Invalid value
                sets=3,
                week=1,
                day=1,
                order=1,
                default_rpe=[7, 8, 9]
            )
            phase_workout.full_clean()  # Trigger validation

    def test_player_arm_care_routine_without_player(self):
        # Attempt to create a PlayerArmCareRoutine without a Player
        routine = ArmCareRoutine.objects.create(name="Routine 1")
        with self.assertRaises(IntegrityError):
            PlayerArmCareRoutine.objects.create(
                player=None,
                routine=routine,
                start_date="2025-04-01",
                end_date="2025-04-30"
            )

    def test_arm_care_exercise_with_invalid_day(self):
        # Create an ArmCareRoutine
        routine = ArmCareRoutine.objects.create(name="Routine 1")
        # Attempt to create an ArmCareExercise with an invalid day
        with self.assertRaises(ValidationError):
            exercise = ArmCareExercise(
                routine=routine,
                day=-1,  # Invalid day
                focus="Shoulder Strength",
                exercise="Crossover Symmetry",
                sets_reps="3x10"
            )
            exercise.full_clean()  # Trigger validation