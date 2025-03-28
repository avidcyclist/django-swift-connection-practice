import SwiftUI

struct ActiveWarmupView: View {
    let playerId: Int

    var body: some View {
        Text("Active Warmup for Player \(playerId)")
            .font(.largeTitle)
            .padding()
    }
}