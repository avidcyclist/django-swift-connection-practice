import Foundation

struct WorkoutEntry: Identifiable, Decodable {
    var id: UUID = UUID()
    let exercise: String
    let reps: Int
    let sets: Int
    let order: Int
    var weight: [Double] = [] // Default empty array
    var rpe: [Double] = []    // Default empty array
}