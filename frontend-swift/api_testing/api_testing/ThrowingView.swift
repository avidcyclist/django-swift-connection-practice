import SwiftUI

struct ThrowingView: View {
    let playerId: Int // Pass the playerId to this view

    var body: some View {
        VStack(spacing: 20) {
            Text("Throwing")
                .font(.largeTitle)
                .fontWeight(.bold)
                .padding()

            // Navigation blocks for Throwing options
            VStack(spacing: 20) {
                NavigationLink(destination: ThrowingActiveWarmupView(playerId: playerId)) {
                    BlockView(title: "Active Warmup", color: .blue)
                }

                NavigationLink(destination: ThrowingProgramView(playerId: playerId)) { // Fixed typo here
                    BlockView(title: "My Program", color: .green)
                }

                NavigationLink(destination: PlyoThrowingRoutinesView(playerId: playerId)) {
                    BlockView(title: "Plyo / Throwing Routines", color: .orange)
                }

                NavigationLink(destination: ArmCareRoutineView(playerId: playerId)) {
                    BlockView(title: "Arm Care", color: .red)
                }
            }
            .padding()
        }
    }
}

