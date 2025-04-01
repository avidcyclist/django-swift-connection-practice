import SwiftUI

struct WorkoutDayView: View {
    let playerId: Int
    let day: Int
    @State var workouts: [WorkoutEntry]
    @State private var showSuccessAlert: Bool = false

    var body: some View {
        VStack {
            Text("Workouts for Day \(day)")
                .font(.largeTitle)
                .padding()

            List(workouts.indices, id: \.self) { index in
                VStack(alignment: .leading) {
                    Text(workouts[index].workout.exercise)
                        .font(.headline)

                    HStack {
                        Text("Reps: \(workouts[index].reps)")
                        Text("Sets: \(workouts[index].sets)")
                    }
                    .font(.subheadline)

                    // Display Default RPE values
                    if !workouts[index].rpe.isEmpty {
                        Text("Default RPE: \(workouts[index].rpe.map { String($0) }.joined(separator: ", "))")
                            .font(.subheadline)
                            .foregroundColor(.gray)
                    } else {
                        Text("Default RPE: None")
                            .font(.subheadline)
                            .foregroundColor(.gray)
                    }

                    // Add column headers for Weight and RPE
                    HStack {
                        Text("Set")
                            .frame(width: 100, alignment: .leading)
                        Text("Weight")
                            .font(.subheadline)
                            .frame(width: 100, alignment: .center)
                        Text("RPE")
                            .font(.subheadline)
                            .frame(width: 100, alignment: .center)
                    }

                    ForEach(0..<workouts[index].sets, id: \.self) { setIndex in
                        HStack {
                            Text("Set \(setIndex + 1):")
                                .frame(width: 100, alignment: .leading)

                            TextField("Enter weight", value: $workouts[index].weight[setIndex], format: .number)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .keyboardType(.decimalPad)
                                .frame(width: 100)

                            TextField("Enter RPE", value: $workouts[index].rpeValues[setIndex], format: .number)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .keyboardType(.numberPad)
                                .frame(width: 100)
                        }
                    }
                }
                .padding(.vertical, 8)
            }

            Button("Save") {
                saveWorkoutData()
            }
            .padding()
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(8)
        }
        .alert(isPresented: $showSuccessAlert) {
            Alert(
                title: Text("Success"),
                message: Text("Workout log saved successfully!"),
                dismissButton: .default(Text("OK"))
            )
        }
        .onAppear {
            fetchWorkoutLog() // Fetch saved workout data when the view appears
        }
    }

func fetchWorkoutLog() {
    guard let url = URL(string: "\(baseURL)/api/get-workout-log/\(playerId)/\(day)/") else { return }

    URLSession.shared.dataTask(with: url) { data, response, error in
        if let error = error {
            print("Error fetching workout log: \(error.localizedDescription)")
            return
        }

        if let data = data {
            do {
                let log = try JSONDecoder().decode(WorkoutLog.self, from: data)
                DispatchQueue.main.async {
                    for (index, workout) in workouts.enumerated() {
                        // Match exercises by their name
                        if let savedWorkout = log.exercises.first(where: { $0.exercise == workout.workout.exercise }) {
                            workouts[index].weight = savedWorkout.sets.map { $0.weight }
                            workouts[index].rpeValues = savedWorkout.sets.map { $0.rpe }
                        }
                    }
                }
            } catch {
                print("Error decoding workout log: \(error)")
            }
        }
    }.resume()
}

    func saveWorkoutData() {
        guard !workouts.isEmpty else {
            print("Error: No workouts to save.")
            return
        }

        guard let url = URL(string: "\(baseURL)/api/save-workout-log/") else { return }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        // Create the exercises array
        let exercises = workouts.map { workout in
            return [
                "exercise": workout.workout.exercise,
                "sets": (0..<workout.sets).map { setIndex in
                    return [
                        "set_number": setIndex + 1,
                        "weight": workout.weight[setIndex],
                        "rpe": workout.rpeValues[setIndex]
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
            } else {
                print("Failed to save workout log. Response: \(response.debugDescription)")
            }
        }.resume()
    }
}