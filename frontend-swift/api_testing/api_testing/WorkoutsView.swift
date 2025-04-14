import SwiftUI

struct WorkoutsView: View {
    let playerId: Int
    let playerFirstName: String
    // Placeholder for player name
    var body: some View {
        VStack {
            Text("Workouts")
                .font(.largeTitle)
                .fontWeight(.bold)
                .padding()

            // Blocks for categories
            VStack(spacing: 20) {
                NavigationLink(destination: CorrectivesView(playerId: playerId, playerName: playerFirstName)) {
                    BlockView(title: "Correctives", color: .blue)
                }

                NavigationLink(destination: ActiveWarmupView(playerId: playerId)) {
                    BlockView(title: "Active Warmup", color: .green)
                }

                NavigationLink(destination: WeeksView(playerId: playerId)) {
                    BlockView(title: "Workout", color: .orange)
                }

                NavigationLink(destination: CardioView(playerId: playerId)) {
                    BlockView(title: "Cardio", color: .purple)
                }
            }
            .padding()
        }
    }
}
