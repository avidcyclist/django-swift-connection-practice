import SwiftUI

struct RoutineDetailView: View {
    let routineId: Int // Pass the routine ID to fetch its details
    @State private var routine: RoutineDetail? = nil // Holds the fetched routine details
    @State private var isLoading = true // Loading state
    @State private var errorMessage: String? = nil // Error message

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            if isLoading {
                ProgressView("Loading routine details...") // Show loading indicator
                    .padding()
            } else if let errorMessage = errorMessage {
                Text("Error: \(errorMessage)") // Show error message
                    .foregroundColor(.red)
                    .padding()
            } else if let routine = routine {
                VStack(alignment: .leading, spacing: 20) {
                    Text(routine.name)
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .padding(.bottom)

                    if let description = routine.description, !description.isEmpty {
                        Text(description)
                            .font(.body)
                            .padding(.bottom)
                    }

                    Text("Drills")
                        .font(.title2)
                        .fontWeight(.bold)
                        .padding(.bottom)

                    ForEach(routine.drills) { drill in
                        VStack(alignment: .leading, spacing: 10) {
                            Text(drill.name)
                                .font(.headline)

                            if let setsReps = drill.setsReps {
                                Text("Sets/Reps: \(setsReps)")
                            }

                            if let weight = drill.weight {
                                Text("Weight: \(weight)")
                            }

                            if let rpe = drill.rpe {
                                Text("RPE: \(rpe)")
                            }

                            if let videoLink = drill.videoLink {
                                Link("Watch Video", destination: URL(string: videoLink)!)
                                    .foregroundColor(.blue)
                            }
                        }
                        .padding()
                        .background(Color(.systemGray6))
                        .cornerRadius(10)
                        .shadow(radius: 2)
                    }
                }
                .padding()
            } else {
                Text("No routine details available.")
                    .foregroundColor(.gray)
                    .padding()
            }
        }
        .onAppear {
            fetchRoutineDetails() // Fetch routine details when the view appears
        }
        .navigationTitle("Routine Details")
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
                isLoading = false
                if let error = error {
                    errorMessage = error.localizedDescription
                    return
                }

                guard let data = data else {
                    errorMessage = "No data received"
                    return
                }

                do {
                    let decodedRoutine = try JSONDecoder().decode(RoutineDetail.self, from: data)
                    routine = decodedRoutine
                } catch {
                    errorMessage = "Failed to decode routine details: \(error.localizedDescription)"
                }
            }
        }.resume()
    }
}