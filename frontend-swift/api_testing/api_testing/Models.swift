import Foundation

struct WorkoutEntry: Identifiable, Decodable {
    var id: UUID = UUID() // Generate a unique ID for SwiftUI
    let workout: WorkoutDetails
    let reps: Int
    let sets: Int
    let day: Int
    let order: Int
}

struct WorkoutDetails: Decodable {
    let id: Int
    let exercise: String
}