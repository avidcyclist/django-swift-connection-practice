import SwiftUI

struct ContentView: View {
    @State private var currentView: String = "Landing" // Tracks which view to display

    var body: some View {
        VStack {
            if currentView == "Landing" {
                // Landing Screen
                Text("Welcome to the App!")
                    .font(.largeTitle)
                    .padding()

                Button("Player Info") {
                    currentView = "PlayerInfo"
                }
                .padding()

                Button("Workout Info") {
                    currentView = "WorkoutInfo"
                }
                .padding()

                Button("Player Selection") {
                    currentView = "PlayerSelection"
                }
                .padding()
            } else if currentView == "PlayerInfo" {
                PlayerInfoView(onBack: { currentView = "Landing" }) // Navigate to Player Info
            } else if currentView == "WorkoutInfo" {
                WorkoutInfoView(onBack: { currentView = "Landing" }) // Navigate to Workout Info
            } else if currentView == "PlayerSelection" {
                PlayerSelectionView(onBack: { currentView = "Landing" }) // Navigate to Player Selection
            }
        }
    }
}