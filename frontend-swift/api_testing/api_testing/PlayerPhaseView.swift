import SwiftUI

struct PlayerPhaseView: View {
    let playerId: Int
    @State private var phaseName: String = "Loading..."
    @State private var workouts: [WorkoutEntry] = [] // Updated to use WorkoutEntry for editable fields
    let onBack: () -> Void

    var body: some View {
        VStack {
            Text("My Phase")
                .font(.title)
                .padding()

            Text(phaseName)
                .font(.headline)
                .padding()

            List {
                ForEach(workouts.indices, id: \.self) { index in
                    VStack(alignment: .leading) {
                        Text(workouts[index].exercise)
                            .font(.headline)

                        HStack {
                            Text("Reps: \(workouts[index].reps)")
                            Text("Sets: \(workouts[index].sets)")
                        }
                        .font(.subheadline)

                        HStack {
                            TextField("Enter weight", value: $workouts[index].weight, format: .number )
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .keyboardType(.decimalPad)
                                .frame(width: 100)

                            TextField("Enter RPE", value: $workouts[index].rpe, format: .number)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .keyboardType(.decimalPad)
                                .frame(width: 100)
                        }
                    }
                    .padding(.vertical, 8)
                }
            }

            Button("Save") {
                saveWorkoutData()
            }
            .padding()
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(8)

            Button("Back") {
                onBack()
            }
            .padding()
        }
        .onAppear {
            fetchPlayerPhase()
        }
    }

    func fetchPlayerPhase() {
        guard let url = URL(string: "https://ce30-2601-246-8101-eff0-40fd-799a-6b28-c7b8.ngrok-free.app/api/player-phases/\(playerId)/") else {
            phaseName = "Invalid URL"
            return
        }

        var request = URLRequest(url: url)
        request.setValue("1", forHTTPHeaderField: "ngrok-skip-browser-warning")

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    phaseName = "Error: \(error.localizedDescription)"
                }
                return
            }

            if let data = data {
                do {
                    if let jsonArray = try JSONSerialization.jsonObject(with: data, options: []) as? [[String: Any]],
                       let firstPhase = jsonArray.first {
                        DispatchQueue.main.async {
                            if let phaseDict = firstPhase["phase"] as? [String: Any],
                               let name = phaseDict["name"] as? String {
                                phaseName = name
                            } else {
                                phaseName = "Unknown Phase"
                            }

                            if let workoutsArray = (firstPhase["phase"] as? [String: Any])?["workouts"] as? [[String: Any]] {
                                workouts = workoutsArray.map { dict in
                                    let exercise = dict["exercise"] as? String ?? "Unknown Exercise"
                                    let reps = dict["reps"] as? Int ?? 0
                                    let sets = dict["sets"] as? Int ?? 0
                                    return WorkoutEntry(exercise: exercise, reps: reps, sets: sets, weight: 0.0, rpe: 0.0)
                                }
                            } else {
                                workouts = []
                            }
                        }
                    }
                } catch {
                    DispatchQueue.main.async {
                        phaseName = "Error decoding JSON"
                    }
                }
            }
        }

        task.resume()
    }

    func saveWorkoutData() {
        guard let url = URL(string: "https://ce30-2601-246-8101-eff0-40fd-799a-6b28-c7b8.ngrok-free.app/api/save-workout-log/") else { return }

        for (index, workout) in workouts.enumerated() {
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")

            let body: [String: Any] = [
                "player": playerId,
                "workout": index + 1, // Assuming workout IDs are sequential for now
                "set_number": index + 1,
                "weight": Double(workout.weight) ?? 0.0,
                "rpe": Double(workout.rpe) ?? 0.0
            ]
            print("Sending request body: \(body)") // Debugging

            request.httpBody = try? JSONSerialization.data(withJSONObject: body)

            URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("Error saving workout log: \(error.localizedDescription)")
                    return
                }

                if let response = response as? HTTPURLResponse, response.statusCode == 201 {
                    print("Workout log saved successfully!")
                }
            }.resume()
        }
    }
}

struct WorkoutEntry {
    var exercise: String
    var reps: Int
    var sets: Int
    var weight: [Double] // Editable weight field
    var rpe: [Double]    // Editable RPE field
}