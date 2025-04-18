import SwiftUI

struct RoutineDetailView: View {
    let routineId: Int // Pass the routine ID to fetch its details
    @State private var routine: RoutineDetail? = nil // Holds the fetched routine details
    @State private var isLoading = true // Loading state
    @State private var errorMessage: String? = nil // Error message

    var body: some View {
        VStack {
            if isLoading {
                ProgressView("Loading Routine Details...")
            } else if let errorMessage = errorMessage {
                Text("Error: \(errorMessage)")
                    .foregroundColor(.red)
            } else if let routine = routine {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        // Header Section
                        Text(routine.name)
                            .font(.largeTitle)
                            .bold()
                            .padding(.bottom, 10)

                        if let description = routine.description, !description.isEmpty {
                            Text(description)
                                .font(.body)
                                .foregroundColor(.gray)
                                .padding(.bottom, 10)
                        }

                        // Drills Section
                        Text("Drills")
                            .font(.headline)
                            .padding(.bottom, 5)

                        ForEach(routine.drills) { drill in
                            VStack(alignment: .leading) {
                                if let name = drill.name {
                                    Text(name)
                                        .font(.subheadline)
                                        .bold()
                                }

                                if let setsReps = drill.setsReps {
                                    Text("Sets/Reps: \(setsReps)")
                                }

                                if let weight = drill.weight {
                                    Text("Weight: \(weight)")
                                }

                                if let distance = drill.distance {
                                    Text("Distance: \(distance)")
                                }

                                if let throwsCount = drill.throwsCount {
                                    Text("Throws: \(throwsCount)")
                                }

                                if let rpe = drill.rpe {
                                    Text("RPE: \(rpe)")
                                }

                                if let videoLink = drill.videoLink, let url = URL(string: videoLink) {
                                    Link("Watch Video", destination: url)
                                        .foregroundColor(.blue)
                                }
                            }
                            .padding()
                            .background(Color.white)
                            .cornerRadius(10)
                            .shadow(radius: 5)
                            .padding(.bottom, 10)
                        }
                    }
                    .padding()
                }
                .background(Color(.systemGroupedBackground)) // Light gray background
            }
        }
        .onAppear {
            fetchRoutineDetails()
        }
    }

    // Function to fetch routine details from the API
    private func fetchRoutineDetails() {
        guard let url = URL(string: "\(baseURL)/api/throwing-routines/\(routineId)/") else {
            errorMessage = "Invalid API URL"
            isLoading = false
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    errorMessage = "Failed to load routine details: \(error.localizedDescription)"
                    isLoading = false
                    return
                }

                guard let data = data else {
                    errorMessage = "No data received"
                    isLoading = false
                    return
                }

                do {
                    let decodedRoutine = try JSONDecoder().decode(RoutineDetail.self, from: data)
                    self.routine = decodedRoutine
                    self.isLoading = false
                } catch {
                    errorMessage = "Failed to decode routine details: \(error.localizedDescription)"
                    isLoading = false
                }
            }
        }.resume()
    }
}

struct DrillCard: View {
    let drill: Drill

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            if let name = drill.name {
                Text(name)
                    .font(.headline)
            }

            if let setsReps = drill.setsReps {
                Text("Sets/Reps: \(setsReps)")
            }

            if let weight = drill.weight {
                Text("Weight: \(weight)")
            }

            if let distance = drill.distance {
                Text("Distance: \(distance)")
            }

            if let throwsCount = drill.throwsCount {
                Text("Throws: \(throwsCount)")
            }

            if let rpe = drill.rpe {
                Text("RPE: \(rpe)")
            }

            if let videoLink = drill.videoLink, let url = URL(string: videoLink) {
                Link("Watch Video", destination: url)
                    .foregroundColor(.blue)
            }
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading) // Stretch horizontally and align left
        .background(Color.white) // Use white for better contrast
        .cornerRadius(10)
        .shadow(radius: 5) // Slightly larger shadow for better visibility
        .padding(.horizontal) // Add horizontal padding for better spacing
    }
}