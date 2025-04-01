/*

import SwiftUI

struct WorkoutsDetailView: View {
    let playerId: Int
    @State private var phaseName: String = "Loading..."
    @State private var workoutsByDay: [String: [WorkoutEntry]] = [:] // Group workouts by day
    @State private var showErrorAlert: Bool = false
    @State private var errorMessage: String = ""

    var body: some View {
        VStack {
            Text(phaseName)
                .font(.largeTitle)
                .padding()

            if workoutsByDay.isEmpty {
                Text("Loading workouts...")
                    .foregroundColor(.gray)
                    .padding()
            } else {
                
                List(workoutsByDay.keys.compactMap { Int($0) }.sorted(), id: \.self) { day in
                    NavigationLink(destination: WorkoutDayView(playerId: playerId, day: day, workouts: workoutsByDay[String(day)] ?? [])) {
                        Text("Day \(day)")
                            .font(.headline)
                            .padding()
                    }
                }
            }
        }
        .onAppear {
            fetchWorkoutsByDay()
        }
        .alert(isPresented: $showErrorAlert) {
            Alert(
                title: Text("Error"),
                message: Text(errorMessage),
                dismissButton: .default(Text("OK"))
            )
        }
    }

    func fetchWorkoutsByDay() {
        guard let url = URL(string: "\(baseURL)/api/player-phases/\(playerId)/workouts-by-day/") else {
            errorMessage = "Invalid URL"
            showErrorAlert = true
            return
        }

        var request = URLRequest(url: url)
        request.setValue("1", forHTTPHeaderField: "ngrok-skip-browser-warning")

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    errorMessage = "Error: \(error.localizedDescription)"
                    showErrorAlert = true
                }
                return
            }

            if let data = data {
                do {
                    let response = try JSONDecoder().decode(PhaseWorkoutsResponse.self, from: data)
                    DispatchQueue.main.async {
                        self.phaseName = response.phaseName
                        self.workoutsByDay = response.workoutsByDay
                    }
                } catch {
                    DispatchQueue.main.async {
                        errorMessage = "Error decoding JSON"
                        showErrorAlert = true
                    }
                }
            }
        }.resume()
    }
}

struct PhaseWorkoutsResponse: Decodable {
    let phaseName: String
    let workoutsByDay: [String: [WorkoutEntry]]

    enum CodingKeys: String, CodingKey {
        case phaseName = "phase_name"
        case workoutsByDay = "workouts_by_day"
    }
}


*/