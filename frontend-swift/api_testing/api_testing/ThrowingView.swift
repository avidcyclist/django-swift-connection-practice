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

                NavigationLink(destination: ThrowingProgramView(playerId: playerId)) {
                    BlockView(title: "My Program", color: .green)
                }

                NavigationLink(destination: PlyoThrowingRoutinesView(playerId: playerId)) {
                    BlockView(title: "Plyo / Throwing Routines", color: .orange)
                }

                NavigationLink(destination: ArmCareView(playerId: playerId)) {
                    BlockView(title: "Arm Care", color: .red)
                }
            }
            .padding()
        }
    }
}


struct ThrowingProgramView: View {
    var body: some View {
        Text("My Program Page")
            .font(.largeTitle)
            .padding()
    }
}

struct PlyoThrowingRoutinesView: View {
    var body: some View {
        Text("Plyo / Throwing Routines Page")
            .font(.largeTitle)
            .padding()
    }
}

struct ArmCareView: View {
    var body: some View {
        Text("Arm Care Page")
            .font(.largeTitle)
            .padding()
    }
}

struct ThrowingActiveWarmupView: View {
    let playerId: Int

    var body: some View {
        Text("Active Warmup for Player \(playerId)")
            .font(.largeTitle)
            .padding()
    }
}