import SwiftUI

enum NavigationDestination: String, Hashable {
    case myProfile = "MyProfile"
    case workouts = "Workouts"
    case throwing = "Throwing"
    case nutrition = "Nutrition"
    case recovery = "Recovery"
}

struct ContentView: View {
    @State private var playerId: Int = 1 // Hardcoded playerId for testing

    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                Text("Welcome, Athlete!")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .padding()

                // Navigation blocks
                VStack(spacing: 20) {
                    NavigationLink(value: NavigationDestination.myProfile) {
                        BlockView(title: "My Profile", color: .blue)
                    }

                    NavigationLink(value: NavigationDestination.workouts) {
                        BlockView(title: "Workouts", color: .green)
                    }

                    NavigationLink(value: NavigationDestination.throwing) {
                        BlockView(title: "Throwing", color: .orange)
                    }

                    NavigationLink(value: NavigationDestination.nutrition) {
                        BlockView(title: "Nutrition", color: .purple)
                    }

                    NavigationLink(value: NavigationDestination.recovery) {
                        BlockView(title: "Recovery", color: .red)
                    }
                }
                .padding()
            }
            .navigationDestination(for: NavigationDestination.self) { destination in
                switch destination {
                case .myProfile:
                    MyProfileView()
                case .workouts:
                    WorkoutsView(playerId: playerId) // Pass the hardcoded playerId here
                case .throwing:
                    ThrowingView()
                case .nutrition:
                    NutritionView()
                case .recovery:
                    RecoveryView()
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