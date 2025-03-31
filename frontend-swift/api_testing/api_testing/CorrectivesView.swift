import SwiftUI
import Config

struct CorrectivesView: View {
    let playerId: Int
    let playerName: String // Added playerName to display in the view
    @State private var correctives: [Corrective] = [] // State to store fetched correctives
    @State private var errorMessage: String? = nil   // State to store error messages

    var body: some View {
        VStack {
            Text("Correctives for Player \(playerName)")
                .font(.largeTitle)
                .padding()

            if let errorMessage = errorMessage {
                // Display error message if there's an error
                Text(errorMessage)
                    .foregroundColor(.red)
                    .padding()
            } else if correctives.isEmpty {
                // Show a loading or empty state
                Text("Loading correctives...")
                    .foregroundColor(.gray)
                    .padding()
            } else {
                // Display the list of correctives
                List(correctives, id: \.id) { corrective in
                    VStack(alignment: .leading) {
                        Text(corrective.name)
                            .font(.headline)
                        if let sets = corrective.sets, let reps = corrective.reps {
                            Text("Sets: \(sets), Reps: \(reps)")
                                .font(.subheadline)
                        }
                        if let youtubeLink = corrective.youtubeLink {
                            Link("Watch Video", destination: URL(string: youtubeLink)!)
                                .foregroundColor(.blue)
                        }
                    }
                    .padding(.vertical, 5)
                }
            }
        }
        .onAppear {
            fetchCorrectives()
        }
    }

    func fetchCorrectives() {
        guard let url = URL(string: "\(baseURL)/api/player/\(playerId)/correctives/") else {
            errorMessage = "Invalid URL"
            return
        }

        var request = URLRequest(url: url)
        request.setValue("1", forHTTPHeaderField: "ngrok-skip-browser-warning")

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    errorMessage = "Error: \(error.localizedDescription)"
                }
                return
            }

            if let data = data {
                do {
                    let fetchedCorrectives = try JSONDecoder().decode([Corrective].self, from: data)
                    DispatchQueue.main.async {
                        self.correctives = fetchedCorrectives
                    }
                } catch {
                    DispatchQueue.main.async {
                        errorMessage = "Error decoding data"
                    }
                }
            }
        }.resume()
    }
}

// Model for Corrective
struct Corrective: Identifiable, Decodable {
    let id: Int
    let name: String
    let sets: Int?
    let reps: Int?
    let youtubeLink: String?

    enum CodingKeys: String, CodingKey {
    case id
    case name
    case sets
    case reps
    case youtubeLink = "youtube_link" // Map API field to Swift property
    }
}