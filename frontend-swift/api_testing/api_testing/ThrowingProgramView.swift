import SwiftUI

struct ThrowingProgramView: View {
    let programId: Int
    @State private var program: PlayerThrowingProgram? = nil
    @State private var isLoading = true
    @State private var errorMessage: String? = nil

    var body: some View {
        VStack {
            if isLoading {
                ProgressView("Loading Throwing Program...")
            } else if let errorMessage = errorMessage {
                Text("Error: \(errorMessage)")
                    .foregroundColor(.red)
            } else if let program = program {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        // Program Header
                        Text("Program \(program.program)")
                            .font(.largeTitle)
                            .bold()
                            .padding(.bottom, 10)

                        // Weekly Program Section
                        Text("Weekly Program")
                            .font(.headline)
                            .padding(.bottom, 5)

                        ForEach(program.days) { day in
                            VStack(alignment: .leading, spacing: 10) {
                                // Flip the order to "Day 1 Light Pen"
                                Text("Day \(day.dayNumber) \(day.name)")
                                    .font(.headline)
                                    .bold()

                                if let warmup = day.warmup {
                                    Text("Warmup: \(warmup)")
                                }
                                if let plyos = day.plyos {
                                    Text("Plyos: \(plyos)")
                                }
                                if let throwing = day.throwing {
                                    Text("Throwing: \(throwing)")
                                }
                                if let veloCommand = day.veloCommand {
                                    Text("Velo Command: \(veloCommand)")
                                }
                                if let armCare = day.armCare {
                                    Text("Arm Care: \(armCare)")
                                }
                                if let lifting = day.lifting {
                                    Text("Lifting: \(lifting)")
                                }
                                if let conditioning = day.conditioning {
                                    Text("Conditioning: \(conditioning)")
                                }
                            }
                            .padding()
                            .background(Color.white)
                            .cornerRadius(10)
                            .shadow(radius: 5)
                            .padding(.bottom, 10)
                        }
                    }
                    .padding()
                }
                .background(Color(.systemGroupedBackground))
            }
        }
        .onAppear {
            fetchThrowingProgram()
        }
    }

    private func fetchThrowingProgram() {
        guard let url = URL(string: "\(baseURL)/api/player-throwing-programs/\(programId)/") else {
            errorMessage = "Invalid API URL"
            isLoading = false
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    errorMessage = "Failed to load program: \(error.localizedDescription)"
                    isLoading = false
                    return
                }

                guard let data = data else {
                    errorMessage = "No data received"
                    isLoading = false
                    return
                }

                do {
                    let decodedProgram = try JSONDecoder().decode(PlayerThrowingProgram.self, from: data)
                    self.program = decodedProgram
                    self.isLoading = false
                } catch {
                    errorMessage = "Failed to decode program: \(error.localizedDescription)"
                    isLoading = false
                }
            }
        }.resume()
    }
}