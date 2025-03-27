import SwiftUI

struct PlayerSelectionView: View {
    @State private var players: [String] = [] // List of player names
    @State private var selectedPlayerId: Int? = nil // Selected player ID
    let onBack: () -> Void // Callback for the back button

    var body: some View {
        VStack {
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
                }
            }

            if let playerId = selectedPlayerId {
                NavigationLink(
                    destination: PlayerPhaseView(playerId: playerId, onBack: { selectedPlayerId = nil }),
                    label: {
                        Text("View Phase for Selected Player")
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(8)
                    }
                )
            }

            Button("Back") {
                onBack() // Call the onBack callback to navigate back
            }
            .padding()
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