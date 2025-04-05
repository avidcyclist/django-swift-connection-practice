import SwiftUI

struct WorkoutDayView: View {
    let playerId: Int
    let week: Int
    let day: Int
    @State var workouts: [WorkoutEntry] = []
    @State private var showSuccessAlert: Bool = false
    @State private var youtubeLinks: [String: String] = [:]  // Map exercise name to YouTube link
    
    var body: some View {
        VStack {
            Text("Workouts for Day \(day)")
                .font(.largeTitle)
                .padding()
            
            if workouts.isEmpty {
                Text("Loading workouts...")
                    .foregroundColor(.gray)
                    .padding()
            } else {
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
                        
                        // Display YouTube link if available
                        if let youtubeLink = youtubeLinks[workouts[index].workout.exercise],
                           !youtubeLink.isEmpty {
                            Button(action: {
                                if let url = URL(string: youtubeLink) {
                                    UIApplication.shared.open(url)  // Open the YouTube link
                                }
                            }) {
                                Text("Watch Tutorial")
                                    .foregroundColor(.blue)
                                    .font(.subheadline)
                            }
                            .buttonStyle(PlainButtonStyle())  // Prevents default button styling
                            .padding(.top, 5)
                        }
                    }
                    .padding(.vertical, 8)
                }
            }
            
            Button("Save") {
                Task {
                    await saveWorkoutData()
                }
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
        .task {
            await fetchWorkoutLog()  // Fetch saved workout data when the view appears
            await fetchYouTubeLinks()  // Fetch YouTube links
        }
    }
    
    // Fetch workout log for the specified player, week, and day
    func fetchWorkoutLog() async {
        guard let url = URL(string: "\(baseURL)/api/get-workout-log/\(playerId)/\(week)/\(day)/") else {
            print("Invalid URL")
            return
        }
        
        print("Fetching workout log from URL: \(url)") // Debugging
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            let log = try JSONDecoder().decode(WorkoutLog.self, from: data)
            DispatchQueue.main.async {
                // Iterate over the workouts array and update it with the fetched data
                for (index, workout) in workouts.enumerated() {
                    if let savedWorkout = log.exercises.first(where: {
                        $0.exercise == workout.workout.exercise
                    }) {
                        // Update weight and RPE values for each set
                        workouts[index].weight = savedWorkout.sets.map { $0.weight ?? 0.0 }
                        workouts[index].rpeValues = savedWorkout.sets.map { $0.rpe ?? 0.0 }
                        workouts[index].rpe = savedWorkout.defaultRpe ?? [] }// Map defaultRpe to rpe                    }
                    }
                }
            } catch {
                print("Error fetching workout log: \(error)")
            }
        }
        
        // Save workout data to the backend
        func saveWorkoutData() async {
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
                            "rpe": workout.rpeValues[setIndex],
                        ]
                    },
                ]
            }
            
            // Create the request body
            let body: [String: Any] = [
                "player": playerId,
                "week": week,
                "day": day,
                "exercises": exercises,
            ]
            
            do {
                request.httpBody = try JSONSerialization.data(withJSONObject: body)
                let (_, response) = try await URLSession.shared.data(for: request)
                
                if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 || httpResponse.statusCode == 201 {
                    print("Workout log saved successfully!")
                    DispatchQueue.main.async {
                        showSuccessAlert = true  // Show success alert
                    }
                } else {
                    print("Failed to save workout log.")
                }
            } catch {
                print("Error saving workout log: \(error)")
            }
        }
        
        // Fetch YouTube links for all workouts
        func fetchYouTubeLinks() async {
            guard let url = URL(string: "\(baseURL)/api/player-workout/") else {
                print("Invalid URL for fetching YouTube links")
                return
            }
            
            do {
                let (data, _) = try await URLSession.shared.data(from: url)
                let workouts = try JSONDecoder().decode([WorkoutDetails].self, from: data)
                DispatchQueue.main.async {
                    // Map exercise names to YouTube links
                    youtubeLinks = workouts.reduce(into: [:]) { result, workout in
                        result[workout.exercise] = workout.youtubeLink
                    }
                }
            } catch {
                print("Error fetching YouTube links: \(error)")
            }
        }
    }

