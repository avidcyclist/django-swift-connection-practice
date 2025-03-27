import SwiftUI

struct WorkoutInfoView: View {
    @State private var apiResponse: [String] = [] // State variable to store API response
    let onBack: () -> Void // Callback for the back button

    var body: some View {
        VStack {
            Text("Workout Info")
                .font(.title)
                .padding()

            List(apiResponse, id: \.self) { item in
                Text(item)
            }

            Button("Back") {
                onBack()
            }
            .padding()
        }
        .onAppear {
            fetchAPIResponse(endpoint: "player-workout")
        }
    }

    func fetchAPIResponse(endpoint: String) {
        guard let url = URL(string: "https://ce30-2601-246-8101-eff0-40fd-799a-6b28-c7b8.ngrok-free.app/api/\(endpoint)/") else {
            apiResponse = ["Invalid URL"]
            return
        }

        var request = URLRequest(url: url)
        request.setValue("1", forHTTPHeaderField: "ngrok-skip-browser-warning")

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    apiResponse = ["Error: \(error.localizedDescription)"]
                }
                return
            }

            if let data = data {
                do {
                    if let jsonArray = try JSONSerialization.jsonObject(with: data, options: []) as? [[String: Any]] {
                        DispatchQueue.main.async {
                        // Format the data in a specific order
                        apiResponse = jsonArray.map { dict in
                            let exercise = dict["exercise"] as? String ?? "N/A"
                            let reps = dict["reps"] as? Int ?? 0
                            let sets = dict["sets"] as? Int ?? 0
                            return "Exercise: \(exercise), Reps: \(reps), Sets: \(sets)"
                            }
                        }
                    }
                } catch {
                    DispatchQueue.main.async {
                        apiResponse = ["Error decoding JSON"]
                    }
                }
            }
        }

        task.resume()
    }
}