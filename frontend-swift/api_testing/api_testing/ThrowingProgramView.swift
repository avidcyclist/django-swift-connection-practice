import SwiftUI

struct ThrowingProgramView: View {
    let programId: Int
    @State private var weeks: [Int: [PlayerThrowingProgramDay]] = [:] // Grouped by week
    @State private var selectedWeek: Int? = 1 // Default to Week 1
    @State private var isLoading = true
    @State private var errorMessage: String? = nil

    var body: some View {
        VStack {
            if isLoading {
                ProgressView("Loading Throwing Program...")
            } else if let errorMessage = errorMessage {
                Text("Error: \(errorMessage)")
                    .foregroundColor(.red)
            } else {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        // Week Buttons
                        Text("Weeks")
                            .font(.headline)
                            .padding(.bottom, 5)

                        HStack {
                            ForEach(weeks.keys.sorted(), id: \.self) { week in
                                Button(action: {
                                    selectedWeek = week
                                }) {
                                    Text("Week \(week)")
                                        .padding()
                                        .background(selectedWeek == week ? Color.blue : Color.gray)
                                        .foregroundColor(.white)
                                        .cornerRadius(10)
                                }
                            }
                        }

                        // Display Days for Selected Week
                        if let selectedWeek = selectedWeek, let days = weeks[selectedWeek] {
                            ForEach(days) { day in
                                VStack(alignment: .leading, spacing: 10) {
                                    Text("Day \(day.dayNumber): \(day.name ?? "")")
                                        .font(.headline)
                                        .bold()

                                    if let warmup = day.warmup, !warmup.isEmpty {
                                        Text("Warmup: \(warmup)")
                                    }
                                    if let plyos = day.plyos, !plyos.isEmpty {
                                        Text("Plyos: \(plyos)")
                                    }
                                    if let throwing = day.throwing, !throwing.isEmpty {
                                        Text("Throwing: \(throwing)")
                                    }
                                    if let veloCommand = day.veloCommand, !veloCommand.isEmpty {
                                        Text("Velo Command: \(veloCommand)")
                                    }
                                    if let armCare = day.armCare, !armCare.isEmpty {
                                        Text("Arm Care: \(armCare)")
                                    }
                                    if let lifting = day.lifting, !lifting.isEmpty {
                                        Text("Lifting: \(lifting)")
                                    }
                                    if let conditioning = day.conditioning, !conditioning.isEmpty {
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
        guard let url = URL(string: "\(baseURL)/api/player-throwing-programs/weeks/\(programId)/") else {
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
                    let decodedWeeks = try JSONDecoder().decode([Int: [PlayerThrowingProgramDay]].self, from: data)
                    self.weeks = decodedWeeks
                    self.selectedWeek = decodedWeeks.keys.sorted().first // Default to the first available week
                    self.isLoading = false
                } catch {
                    errorMessage = "Failed to decode program: \(error.localizedDescription)"
                    isLoading = false
                }
            }
        }.resume()
    }
}