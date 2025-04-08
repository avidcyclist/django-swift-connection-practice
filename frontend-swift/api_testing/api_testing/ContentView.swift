import SwiftUI

enum NavigationDestination: String, Hashable {
    case myProfile = "MyProfile"
    case workouts = "Workouts"
    case throwing = "Throwing"
    case nutrition = "Nutrition"
    case recovery = "Recovery"
}

struct ContentView: View {
    @State private var playerId: Int = 1 // Hardcoded playerId for now
    @State private var playerName: String = "Mitch" // Hardcoded player name for now
    @State private var programId: Int? = nil // Dynamically fetched programId
    @State private var isLoading = true
    @State private var errorMessage: String? = nil

    var body: some View {
        NavigationStack {
            if isLoading {
                ProgressView("Loading Program Data...")
            } else if let errorMessage = errorMessage {
                Text("Error: \(errorMessage)")
                    .foregroundColor(.red)
            } else {
                VStack(spacing: 20) {
                    Text("Welcome, \(playerName)!")
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
                        .disabled(programId == nil) // Disable if programId is nil

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
                        MyProfileView(playerId: playerId)
                    case .workouts:
                        WorkoutsView(playerId: playerId, playerName: playerName)
                    case .throwing:
                        if let programId = programId {
                            ThrowingView(playerId: playerId, programId: programId)
                        } else {
                            Text("Program ID not available")
                        }
                    case .nutrition:
                        NutritionView()
                    case .recovery:
                        RecoveryView()
                    }
                }
            }
        }
        .onAppear {
            fetchProgramData(playerId: playerId)
        }
    }

    // Fetch program data for the hardcoded playerId
    private func fetchProgramData(playerId: Int) {
        guard let url = URL(string: "\(baseURL)/api/player-throwing-programs/?player_id=\(playerId)") else {
            errorMessage = "Invalid API URL"
            isLoading = false
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    errorMessage = "Failed to fetch program data: \(error.localizedDescription)"
                    isLoading = false
                    return
                }

                guard let data = data else {
                    errorMessage = "No data received"
                    isLoading = false
                    return
                }

                do {
                    // Decode the response to get the list of PlayerThrowingPrograms
                    let programs = try JSONDecoder().decode([PlayerThrowingProgram].self, from: data)
                    
                    // Set the programId for the first program (or handle multiple programs if needed)
                    if let program = programs.first {
                        self.programId = program.id
                    } else {
                        errorMessage = "No programs found for playerId \(playerId)"
                    }
                } catch {
                    errorMessage = "Failed to decode program data: \(error.localizedDescription)"
                }
                isLoading = false
            }
        }.resume()
    }
}

// Placeholder views for each section
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