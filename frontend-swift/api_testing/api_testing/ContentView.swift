import SwiftUI

struct ContentView: View {
    @State private var selectedView: String? = nil // Tracks the selected view

    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                Text("Welcome, Athlete!")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .padding()

                // Navigation blocks
                VStack(spacing: 20) {
                    NavigationLink(value: "MyProfile") {
                        BlockView(title: "My Profile", color: .blue)
                    }

                    NavigationLink(value: "Workouts") {
                        BlockView(title: "Workouts", color: .green)
                    }

                    NavigationLink(value: "Throwing") {
                        BlockView(title: "Throwing", color: .orange)
                    }

                    NavigationLink(value: "Nutrition") {
                        BlockView(title: "Nutrition", color: .purple)
                    }

                    NavigationLink(value: "Recovery") {
                        BlockView(title: "Recovery", color: .red)
                    }
                }
                .padding()
            }
            .navigationDestination(for: String.self) { view in
                switch view {
                case "MyProfile":
                    MyProfileView()
                case "Workouts":
                    WorkoutsView(playerId: 1, onBack: {}) // Updated to use WorkoutsView
                case "Throwing":
                    ThrowingView()
                case "Nutrition":
                    NutritionView()
                case "Recovery":
                    RecoveryView()
                default:
                    Text("Unknown View")
                }
            }
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

// Placeholder views for each section

struct ThrowingView: View {
    var body: some View {
        Text("Throwing Page")
            .font(.largeTitle)
            .padding()
    }
}

struct NutritionView: View {
    var body: some View {
        Text("Nutrition Page")
            .font(.largeTitle)
            .padding()
    }
}

struct RecoveryView: View {
    var body: some View {
        Text("Recovery Page")
            .font(.largeTitle)
            .padding()
    }
}