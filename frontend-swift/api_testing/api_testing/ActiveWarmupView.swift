import SwiftUI

struct ActiveWarmupView: View {
    let playerId: Int
    @State private var activeWarmups: [ActiveWarmup] = []
    @State private var powerCNSWarmups: [PowerCNSWarmup] = []
    @State private var isLoading = true
    @State private var errorMessage: String?

    var groupedPowerCNSWarmups: [Int: [PowerCNSWarmup]] {
        Dictionary(grouping: powerCNSWarmups, by: { $0.day })
    }

    var body: some View {
        VStack {
            if isLoading {
                ProgressView("Loading Warmups...")
            } else if let errorMessage = errorMessage {
                Text("Error: \(errorMessage)")
                    .foregroundColor(.red)
            } else {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        // Header
                        Text("All exercises 10-15 yards")
                            .font(.title2)
                            .bold()
                            .padding(.bottom, 10)

                        // Active Warmups Section
                        Text("Active Warmup")
                            .font(.headline)
                            .padding(.bottom, 5)
                        ForEach(activeWarmups) { warmup in
                            VStack(alignment: .leading) {
                                Text(warmup.name)
                                    .font(.subheadline)
                                    .bold()
                                if let link = warmup.youtube_link {
                                    Link("Watch Video", destination: URL(string: link)!)
                                        .foregroundColor(.blue)
                                }
                            }
                            .padding()
                            .background(Color.white)
                            .cornerRadius(10)
                            .shadow(radius: 5)
                            .padding(.bottom, 10)
                        }

                        // Power CNS Warmups Section
                        ForEach(groupedPowerCNSWarmups.keys.sorted(), id: \.self) { day in
                            VStack(alignment: .leading, spacing: 10) {
                                Text("Power CNS Warmup Day \(day)")
                                    .font(.headline)
                                    .padding(.bottom, 5)

                                ForEach(groupedPowerCNSWarmups[day] ?? []) { warmup in
                                    VStack(alignment: .leading) {
                                        Text(warmup.name)
                                            .font(.subheadline)
                                            .bold()
                                            .padding(.bottom, 5)
                                        ForEach(warmup.exercises) { exercise in
                                            VStack(alignment: .leading) {
                                                Text("- \(exercise.name)")
                                                    .font(.subheadline)
                                                if let link = exercise.youtube_link {
                                                    Link("Watch Video", destination: URL(string: link)!)
                                                        .foregroundColor(.blue)
                                                }
                                            }
                                            .padding(.leading, 10)
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
                    }
                    .padding()
                }
                .background(Color(.systemGroupedBackground)) // Light gray background
            }
        }
        .onAppear {
            fetchWarmups()
        }
    }

    func fetchWarmups() {
        guard let url = URL(string: "\(baseURL)/api/player-warmup/\(playerId)/") else {
            errorMessage = "Invalid URL"
            isLoading = false
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    errorMessage = "Failed to load warmups: \(error.localizedDescription)"
                    isLoading = false
                    return
                }

                guard let data = data else {
                    errorMessage = "No data received"
                    isLoading = false
                    return
                }

                do {
                    let decodedResponse = try JSONDecoder().decode(PlayerWarmupResponse.self, from: data)
                    self.activeWarmups = decodedResponse.active_warmups
                    self.powerCNSWarmups = decodedResponse.power_cns_warmups
                    self.isLoading = false
                } catch {
                    errorMessage = "Failed to decode response: \(error.localizedDescription)"
                    isLoading = false
                }
            }
        }.resume()
    }
}