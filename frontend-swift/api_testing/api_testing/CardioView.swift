import SwiftUI

struct CardioView: View {
    let playerId: Int

    var body: some View {
        Text("Cardio for Player \(playerId)")
            .font(.largeTitle)
            .padding()
    }
}