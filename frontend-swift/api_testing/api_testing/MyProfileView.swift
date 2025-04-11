import SwiftUI

struct MyProfileView: View {
    let playerId: Int // Pass the player ID dynamically
    @State private var apiResponse: [String] = [] // State variable to store API response

    var body: some View {
        VStack {
            Text("Player Info")
                .font(.title)
                .padding()

            List(apiResponse, id: \.self) { item in
                Text(item)
            }
        }
        .onAppear {
            fetchAPIResponse(playerId: playerId) // Pass the player ID here
        }
    }

    func fetchAPIResponse(playerId: Int) {
        guard let url = URL(string: "\(baseURL)/api/player-info/\(playerId)/") else {
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
                    // Parse the response as a single dictionary
                    if let jsonDict = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                        DispatchQueue.main.async {
                            let firstName = jsonDict["first_name"] as? String ?? "N/A"
                            let lastName = jsonDict["last_name"] as? String ?? "N/A"
                            let age = jsonDict["age"] as? Int ?? 0
                            let team = jsonDict["team"] as? String ?? "N/A"
                            apiResponse = ["Name: \(firstName) \(lastName)", "Age: \(age)", "Team: \(team)"]
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