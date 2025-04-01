import SwiftUI

struct DaysView: View {
    let playerId: Int
    let week: String
    let days: [String: [WorkoutEntry]] // Days data passed from WeeksView

    var body: some View {
        VStack {
            Text("Week \(week): Select a Day")
                .font(.largeTitle)
                .padding()

            if days.isEmpty {
                Text("No days available for this week.")
                    .foregroundColor(.gray)
                    .padding()
            } else {
                List(days.keys.sorted(), id: \.self) { day in
                    NavigationLink(destination: WorkoutDayView(playerId: playerId, day: Int(day) ?? 0, workouts: days[day] ?? [])) {
                        Text("Day \(day)")
                            .font(.headline)
                            .padding()
                    }
                }
            }
        }
    }
}