import SwiftUI

struct CorrectivesView: View {
    let playerId: Int

    var body: some View {
        Text("Correctives for Player \(playerId)")
            .font(.largeTitle)
            .padding()
    }
}