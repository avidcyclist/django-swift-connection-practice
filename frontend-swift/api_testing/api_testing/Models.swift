import Foundation

struct WorkoutEntry: Identifiable, Decodable {
    var id: Int { workoutId }
    let workoutId: Int
    let exercise: String
    let reps: Int
    let sets: Int
    var weight: [Double] // Editable weight field for each set
    var rpe: [Double]    // Editable RPE field for each set
}