import SwiftUI

struct ThrowingView: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("Throwing")
                .font(.largeTitle)
                .fontWeight(.bold)
                .padding()

            // Navigation blocks for Throwing options
            VStack(spacing: 20) {
                NavigationLink(destination: ActiveWarmupView()) {
                    BlockView(title: "Active Warmup", color: .blue)
                }

                NavigationLink(destination: MyProgramView()) {
                    BlockView(title: "My Program", color: .green)
                }

                NavigationLink(destination: PlyoThrowingRoutinesView()) {
                    BlockView(title: "Plyo / Throwing Routines", color: .orange)
                }

                NavigationLink(destination: ArmCareView()) {
                    BlockView(title: "Arm Care", color: .red)
                }
            }
            .padding()
        }
    }
}

// Placeholder views for each section
struct ActiveWarmupView: View {
    var body: some View {
        Text("Active Warmup Page")
            .font(.largeTitle)
            .padding()
    }
}

struct MyProgramView: View {
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
