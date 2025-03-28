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

                NavigationLink(destination: DetailedWorkoutsView(playerId: playerId)) {
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

// A reusable block view for navigation
struct BlockView: View {
    let title: String
    let color: Color

    var body: some View {
        Text(title)
            .font(.headline)
            .frame(maxWidth: .infinity)
            .padding()
            .background(color)
            .foregroundColor(.white)
            .cornerRadius(10)
            .shadow(radius: 5)
    }
}