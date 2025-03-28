import SwiftUI

struct ContentView: View {
    @State private var playerId: Int? = nil // State to store the playerId
    @State private var isLoading: Bool = true // State to show loading indicator

    var body: some View {
        NavigationStack {
            if isLoading {
                ProgressView("Loading player data...") // Show a loading spinner while fetching playerId
                    .padding()
            } else if let playerId = playerId {
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
                        WorkoutsView(playerId: playerId) // Pass the dynamic playerId here
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
            } else {
                Text("Failed to load player data.")
                    .foregroundColor(.red)
            }
        }
        .onAppear {
            fetchPlayerId() // Fetch the playerId when the view appears
        }
    }

func fetchPlayerId() {
    guard let url = URL(string: "https://your-backend-url/api/player-id/") else {
        self.isLoading = false
        return
    }

    URLSession.shared.dataTask(with: url) { data, response, error in
        if let error = error {
            print("Error fetching playerId: \(error.localizedDescription)")
            DispatchQueue.main.async {
                self.isLoading = false
            }
            return
        }

        if let data = data, let json = try? JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
           let id = json["playerId"] as? Int {
            DispatchQueue.main.async {
                self.playerId = id
                self.isLoading = false
            }
        } else {
            DispatchQueue.main.async {
                self.isLoading = false
            }
        }
    }.resume()

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