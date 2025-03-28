import SwiftUI

struct PlayerPhaseView: View {
    let playerId: Int
    @State private var phaseName: String = "Loading..."
    @State private var workouts: [WorkoutEntry] = [] // Updated to use WorkoutEntry for editable fields
    @State private var showSuccessAlert: Bool = false // State for showing success alert
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

                        ForEach(0..<workouts[index].sets, id: \.self) { setIndex in
                            HStack {
                                Text("Set \(setIndex + 1):")
                                TextField("Enter weight", value: $workouts[index].weight[setIndex], format: .number)
                                    .textFieldStyle(RoundedBorderTextFieldStyle())
                                    .keyboardType(.decimalPad)
                                    .frame(width: 100)

                                TextField("Enter RPE", value: $workouts[index].rpe[setIndex], format: .number)
                                    .textFieldStyle(RoundedBorderTextFieldStyle())
                                    .keyboardType(.decimalPad)
                                    .frame(width: 100)
                            }
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
        .alert(isPresented: $showSuccessAlert) {
            Alert(
                title: Text("Success"), 
                message: Text("Workout log saved successfully!"), 
                dismissButton: .default(Text("OK")))
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

                            if let phaseWorkoutsArray = (firstPhase["phase"] as? [String: Any])?["phase_workouts"] as? [[String: Any]] {
                                workouts = phaseWorkoutsArray.compactMap { dict in
                                    let workout = dict["workout"] as? [String: Any] ?? [:]
                                    let exercise = workout["exercise"] as? String ?? "Unknown Exercise"
                                    let workoutId = workout["id"] as? Int ?? 0

                                    // Add validation for workoutId
                                    if workoutId == 0 {
                                        print("Error: Missing or invalid workout ID for workout: \(workout)")
                                        return nil // Skip invalid workouts
                                    }

                                    let reps = dict["reps"] as? Int ?? 0
                                    let sets = dict["sets"] as? Int ?? 0
                                    return WorkoutEntry(
                                        workoutId: workoutId,
                                        exercise: exercise,
                                        reps: reps,
                                        sets: sets,
                                        weight: Array(repeating: 0.0, count: sets),
                                        rpe: Array(repeating: 0.0, count: sets)
                                    )
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

    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")

    // Create the exercises array
    let exercises = workouts.map { workout in
        return [
            "exercise": workout.exercise,
            "sets": (0..<workout.sets).map { setIndex in
                return [
                    "set_number": setIndex + 1,
                    "weight": workout.weight[setIndex],
                    "rpe": workout.rpe[setIndex]
                ]
            }
        ]
    }

    // Create the request body
    let body: [String: Any] = [
        "player": playerId,
        "date": DateFormatter.localizedString(from: Date(), dateStyle: .short, timeStyle: .none),
        "exercises": exercises
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
            DispatchQueue.main.async {
                showSuccessAlert = true // Show success alert
            }
            workouts = workouts.map { workout in
                var updatedWorkout = workout
                updatedWorkout.weight = Array(repeating: 0.0, count: workout.sets) // Reset weight fields after saving
                updatedWorkout.rpe = Array(repeating: 0.0, count: workout.sets)    // Reset RPE fields after saving
                return updatedWorkout
            }
        } else {
            print("Failed to save workout log. Response: \(response.debugDescription)")
        }
    }.resume()
}


struct WorkoutEntry {
    var workoutId: Int
    var exercise: String
    var reps: Int
    var sets: Int
    var weight: [Double] // Editable weight field for each set
    var rpe: [Double]    // Editable RPE field for each set
}
