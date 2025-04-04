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