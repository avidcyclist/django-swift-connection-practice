import SwiftUI

struct WorkoutsView: View {
    let playerId: Int

    var body: some View {
        VStack {
            Text("Workouts")
                .font(.largeTitle)
                .fontWeight(.bold)
                .padding()

            // Blocks for categories
            VStack(spacing: 20) {
                NavigationLink(destination: CorrectivesView(playerId: playerId)) {
                    BlockView(title: "Correctives", color: .blue)
                }

                NavigationLink(destination: ActiveWarmupView(playerId: playerId)) {
                    BlockView(title: "Active Warmup", color: .green)
                }

                NavigationLink(destination: WorkoutsDetailView(playerId: playerId)) {
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
