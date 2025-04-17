import SwiftUI

enum NavigationDestination: String, Hashable {
    case myProfile = "MyProfile"
    case workouts = "Workouts"
    case throwing = "Throwing"
    case dailyIntake = "Daily Intake"
    case recovery = "Recovery"
}

struct ContentView: View {
    @State private var playerId: Int = 0 // Default to 0 until fetched
    @State private var playerFirstName: String = "" // Default to empty until fetched
    @State private var isLoggedIn: Bool = false
    @State private var programId: Int? = nil // Dynamically fetched programId
    @State private var isLoading = true
    @State private var errorMessage: String? = nil

    var body: some View {
            if isLoggedIn {
                NavigationStack {
                    if isLoading {
                        ProgressView("Loading Program Data...")
                    } else if let errorMessage = errorMessage {
                        Text("Error: \(errorMessage)")
                            .foregroundColor(.red)
                    } else {
                        VStack(spacing: 20) {
                            Text("Welcome, \(playerFirstName)!")
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
                                .disabled(programId == nil)

                                NavigationLink(value: NavigationDestination.dailyIntake) {
                                    BlockView(title: "Daily Intake", color: .purple)
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
                                WorkoutsView(playerId: playerId, playerFirstName: playerFirstName)
                            case .throwing:
                                if let programId = programId {
                                    ThrowingView(playerId: playerId, programId: programId)
                                } else {
                                    Text("Program ID not available")
                                }
                            case .dailyIntake:
                                DailyIntakeView(playerId: playerId)
                            case .recovery:
                                RecoveryView()
                            }
                        }
                    }
                }
                .onAppear {
                    fetchProgramData(playerId: playerId)
                }
            } else {
                LoginView(playerId: $playerId, playerFirstName: $playerFirstName, isLoggedIn: $isLoggedIn)
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

struct RecoveryView: View {
    var body: some View {
        Text("Recovery Page")
            .font(.largeTitle)
            .padding()
    }
}
