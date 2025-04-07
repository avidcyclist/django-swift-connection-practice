import SwiftUI

struct PlyoThrowingRoutinesView: View {
    let playerId: Int
    @State private var routines: [Routine] = [] // Array to hold fetched routines
    @State private var isLoading = true // Loading state
    @State private var errorMessage: String? = nil // Error message

    var body: some View {
        VStack {
            Text("Plyo / Throwing Routines")
                .font(.largeTitle)
                .fontWeight(.bold)
                .padding()

            if isLoading {
                ProgressView("Loading routines...") // Show loading indicator
                    .padding()
            } else if let errorMessage = errorMessage {
                Text("Error: \(errorMessage)") // Show error message
                    .foregroundColor(.red)
                    .padding()
            } else if routines.isEmpty {
                Text("No routines available.") // Show message if no routines
                    .foregroundColor(.gray)
                    .padding()
            } else {
                List(routines) { routine in
                    NavigationLink(destination: RoutineDetailView(routineId: routine.id)) {
                        Text(routine.name)
                            .font(.headline)
                            .padding()
                    }
                }
            }
        }
        .onAppear {
            fetchRoutines() // Fetch routines when the view appears
        }
    }

    // Function to fetch routines from the API
    private func fetchRoutines() {
        guard let url = URL(string: "\(baseURL)/api/throwing-routines/") else {
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
                    let decodedRoutines = try JSONDecoder().decode([Routine].self, from: data)
                    routines = decodedRoutines
                } catch {
                    errorMessage = "Failed to decode routines: \(error.localizedDescription)"
                }
            }
        }.resume()
    }
}
