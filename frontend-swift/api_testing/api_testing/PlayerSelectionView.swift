import SwiftUI

struct PlayerSelectionView: View {
    @State private var players: [String] = [] // List of player names
    @State private var selectedPlayerId: Int? = nil // Selected player ID
    @State private var currentView: String = "PlayerSelection" // Tracks the current view
    let onBack: () -> Void // Callback for the back button

    var body: some View {
        VStack {
            if currentView == "PlayerSelection" {
                Text("Select a Player")
                    .font(.title)
                    .padding()

                List(players, id: \.self) { player in
                    Button(player) {
                        // Simulate selecting a player (hard-code IDs for now)
                        if player == "Walt" {
                            selectedPlayerId = 1
                        } else if player == "Bruiser" {
                            selectedPlayerId = 2
                        }
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
        // Hard-code player names for now
        players = ["Walt", "Bruiser"]
    }
}