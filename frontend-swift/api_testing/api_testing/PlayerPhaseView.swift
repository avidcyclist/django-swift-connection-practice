import SwiftUI

struct PlayerPhaseView: View {
    let playerId: Int
    @State private var phaseName: String = "Loading..."
    @State private var workouts: [String] = [] // List of workouts
    let onBack: () -> Void

    var body: some View {
        VStack {
            Text("My Phase")
                .font(.title)
                .padding()

            Text(phaseName)
                .font(.headline)
                .padding()

            List(workouts, id: \.self) { workout in
                Text(workout)
            }

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
                                "\(dict["exercise"] as? String ?? "Unknown Exercise")"
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