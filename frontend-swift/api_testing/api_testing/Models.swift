import Foundation

// Response for the entire phase, grouped by weeks
struct PhaseWorkoutsResponse: Decodable {
    let phaseName: String
    let weeks: [String: WeekDetails] // Group workouts by week

    enum CodingKeys: String, CodingKey {
        case phaseName = "phase_name"
        case weeks
    }
}

// Details for a specific week, grouped by days
struct WeekDetails: Decodable {
    let days: [String: [WorkoutEntry]] // Group workouts by day
}

// Individual workout entry
// Individual workout entry
struct WorkoutEntry: Decodable {
    let workout: WorkoutDetails
    let reps: Int
    let sets: Int
    let tempo: String // Add tempo if needed
    var rpe: [Int] // Maps to "default_rpe" in the API response
    let day: Int
    let order: Int
    var weight: [Double] // Athlete-entered weights
    var rpeValues: [Double] // Athlete-entered RPEs

    // Custom initializer to set default values for `weight` and `rpeValues`
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        self.workout = try container.decode(WorkoutDetails.self, forKey: .workout)
        self.reps = try container.decode(Int.self, forKey: .reps)
        self.sets = try container.decode(Int.self, forKey: .sets)
        self.tempo = try container.decodeIfPresent(String.self, forKey: .tempo) ?? ""
        self.rpe = try container.decodeIfPresent([Int].self, forKey: .rpe) ?? [] // Decode as an array of integers
        self.day = try container.decode(Int.self, forKey: .day)
        self.order = try container.decode(Int.self, forKey: .order)

        // Initialize `weight` and `rpeValues` with default values
        self.weight = Array(repeating: 0.0, count: self.sets)
        self.rpeValues = Array(repeating: 0.0, count: self.sets)
    }

    enum CodingKeys: String, CodingKey {
        case workout, reps, sets, tempo, rpe = "default_rpe", day, order
    }
}


// Details about the workout itself
struct WorkoutDetails: Decodable {
    let id: Int
    let exercise: String
    let youtubeLink: String?

    enum CodingKeys: String, CodingKey {
        case id
        case exercise
        case youtubeLink = "youtube_link"
    }
}

struct WorkoutLog: Decodable {
    let id: Int
    let player: Int
    let week: Int
    let day: Int
    let exercises: [Exercise]
    let comments: String? // Add the comments field

    struct Exercise: Decodable {
        let exercise: String
        let youtubeLink: String? 
        let sets: [Set]

        struct Set: Decodable {
            let set_number: Int
            let weight: Double
            let rpe: Double
        }
    }
}

struct ExerciseLog: Decodable {
    let exercise: String
    let sets: [SetLog]
}

struct SetLog: Decodable {
    let set_number: Int
    let weight: Double
    let rpe: Double
}

// Active Warmup Model
struct ActiveWarmup: Identifiable, Codable {
    let id: Int
    let name: String
    let youtube_link: String?
}

// Throwing Active Warmup Model
struct ThrowingActiveWarmup: Identifiable, Codable {
    let id: Int
    let name: String
    let youtube_link: String?
    let sets_reps: String?
}



// Power CNS Exercise Model
struct PowerCNSExercise: Identifiable, Codable {
    let id: Int
    let name: String
    let youtube_link: String?
}

// Power CNS Warmup Model
struct PowerCNSWarmup: Identifiable, Codable {
    let id: Int
    let name: String
    let day: Int
    let exercises: [PowerCNSExercise]
}

// Combined Warmup Response Model
struct PlayerWarmupResponse: Codable {
    let active_warmups: [ActiveWarmup]
    let power_cns_warmups: [PowerCNSWarmup]
}

// Model for a routine
struct Routine: Identifiable, Decodable {
    let id: Int
    let name: String
    let description: String
}

// Model for routine details
struct RoutineDetail: Decodable {
    let id: Int
    let name: String
    let description: String?
    let drills: [Drill]
}

// Model for a drill
struct Drill: Identifiable, Decodable {
    let id: Int
    let name: String? // Make name optional
    let setsReps: String? // Make setsReps optional
    let weight: String?
    let distance: String?
    let throwsCount: String? // Use a different name for 'throws'
    let rpe: String?
    let videoLink: String?

    enum CodingKeys: String, CodingKey {
        case id, name
        case setsReps = "sets_reps"
        case weight, distance
        case throwsCount = "throws" // Map 'throws' from JSON to 'throwsCount'
        case rpe
        case videoLink = "video_link"
    }
}

struct PlayerThrowingProgram: Decodable {
    let id: Int
    let player: Int
    let program: Int
    let startDate: String
    let endDate: String
    let days: [PlayerThrowingProgramDay]

    enum CodingKeys: String, CodingKey {
        case id, player, program
        case startDate = "start_date"
        case endDate = "end_date"
        case days
    }
}

struct PlayerThrowingProgramDay: Decodable, Identifiable {
    let id: Int
    let weekNumber: Int
    let dayNumber: Int
    let name: String?
    let warmup: String?
    let plyos: String?
    let throwing: String?
    let veloCommand: String?
    let armCare: String?
    let lifting: String?
    let conditioning: String?

    enum CodingKeys: String, CodingKey {
        case id
        case weekNumber = "week_number"
        case dayNumber = "day_number"
        case name, warmup, plyos, throwing
        case veloCommand = "velo_command"
        case armCare = "arm_care"
        case lifting, conditioning
    }
}

struct Player: Codable {
    let playerId: Int
    let firstName: String
    let lastName: String
    let email: String

    enum CodingKeys: String, CodingKey {
        case playerId = "playerId"
        case firstName = "first_name"
        case lastName = "last_name"
        case email = "email"
    }
}

struct ArmCareRoutineResponse: Codable {
    let id: Int
    let player: Int
    let playerName: String
    let routineName: String
    let description: String?
    let startDate: String?
    let endDate: String?
    let days: [String: [ArmCareExercise]] // Grouped by day

    enum CodingKeys: String, CodingKey {
        case id
        case player
        case playerName = "player_name" // Map "player_name" to "playerName"
        case routineName = "routine_name" // Map "routine_name" to "routineName"
        case description
        case startDate = "start_date" // Map "start_date" to "startDate"
        case endDate = "end_date" // Map "end_date" to "endDate"
        case days
    }
}


struct ArmCareExercise: Codable, Identifiable {
    let id: Int
    let day: Int
    let focus: String?
    let exercise: String
    let setsReps: String?
    let youtubeLink: String?

    enum CodingKeys: String, CodingKey {
        case id
        case day
        case focus
        case exercise
        case setsReps = "sets_reps"
        case youtubeLink = "youtube_link"
    }
}

struct LoginResponse: Codable {
    let token: String
    let user: Player
}

struct DailyIntake: Codable, Identifiable {
    let id: Int
    let player: Int
    let date: String // Use String to handle date formatting from the API
    let armFeel: Int? // Optional, 1-5 scale
    let bodyFeel: Int? // Optional, 1-5 scale
    let sleepHours: Double? // Optional, e.g., 7.5 hours
    let weight: Double? // Optional, e.g., 180.5 lbs
    let metCalorieMacros: Bool // Checkbox for meeting calorie/macros
    let completedDayPlan: Bool // Checkbox for completing the day's plan
    let comments: String? // Optional comments/notes

    enum CodingKeys: String, CodingKey {
        case id, player, date
        case armFeel = "arm_feel"
        case bodyFeel = "body_feel"
        case sleepHours = "sleep_hours"
        case weight
        case metCalorieMacros = "met_calorie_macros"
        case completedDayPlan = "completed_day_plan"
        case comments
    }
}