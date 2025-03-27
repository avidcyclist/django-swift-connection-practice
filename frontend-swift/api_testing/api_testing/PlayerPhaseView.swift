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
                            phaseName = firstPhase["phase"] as? [String: Any]? ?? ["name": "Unknown Phase"]?["name"] as! String
                            workouts = (firstPhase["workouts"] as? [[String: Any]])?.map { dict in
                                "\(dict["exercise"] as? String ?? "Unknown Exercise")"
                            } ?? []
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
}