import SwiftUI

struct PlayerSelectionView: View {
    @State private var players: [(id: Int, name: String)] = [] // List of players with IDs and names
    @State private var selectedPlayerId: Int? = nil // Selected player ID
    @State private var currentView: String = "PlayerSelection" // Tracks the current view
    let onBack: () -> Void // Callback for the back button

    var body: some View {
        VStack {
            if currentView == "PlayerSelection" {
                Text("Select a Player")
                    .font(.title)
                    .padding()

                List(players, id: \.id) { player in
                    Button(player.name) {
                        selectedPlayerId = player.id
                        currentView = "PlayerPhase"
                    }
                }

                Button("Back") {
                    onBack() // Call the onBack callback to navigate back
                }
                .padding()
            } else if currentView == "PlayerPhase" {
                if let playerId = selectedPlayerId {
                    PlayerPhaseView(playerId: playerId, onBack: { currentView = "PlayerSelection" })
                }
            }
        }
        .onAppear {
            fetchPlayers()
        }
    }

func fetchPlayers() {
    guard let url = URL(string: "https://ce30-2601-246-8101-eff0-40fd-799a-6b28-c7b8.ngrok-free.app/api/players/") else { return }

    URLSession.shared.dataTask(with: url) { data, response, error in
        if let data = data {
            do {
                // Decode the JSON response into an array of players
                let decodedPlayers = try JSONDecoder().decode([Player].self, from: data)
                DispatchQueue.main.async {
                    // Since we expect only one player, take the first player from the array
                    if let firstPlayer = decodedPlayers.first {
                        players = [(id: firstPlayer.id, name: firstPlayer.name)]
                    } else {
                        print("No players found in the response.")
                        players = []
                    }
                }
            } catch {
                print("Error decoding players: \(error)")
            }
        } else if let error = error {
            print("Error fetching players: \(error)")
        }
    }.resume()
}

// Define a Player struct to match the API response
struct Player: Codable, Identifiable {
    let id: Int
    let name: String
}