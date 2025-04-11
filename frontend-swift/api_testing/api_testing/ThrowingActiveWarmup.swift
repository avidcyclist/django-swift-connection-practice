import SwiftUI

struct ThrowingActiveWarmupView: View {
    let playerId: Int
    @State private var throwingActiveWarmups: [ThrowingActiveWarmup] = [] // Use the new struct
    @State private var isLoading = true
    @State private var errorMessage: String?

    var body: some View {
        VStack {
            if isLoading {
                ProgressView("Loading Throwing Active Warmups...")
            } else if let errorMessage = errorMessage {
                Text("Error: \(errorMessage)")
                    .foregroundColor(.red)
            } else {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        // Header
                        Text("Throwing Active Warmups")
                            .font(.title2)
                            .bold()
                            .padding(.bottom, 10)

                        // Throwing Active Warmups Section
                        ForEach(throwingActiveWarmups) { warmup in
                            VStack(alignment: .leading) {
                                Text(warmup.name)
                                    .font(.subheadline)
                                    .bold()
                                if let setsReps = warmup.sets_reps {
                                    Text("Sets/Reps: \(setsReps)")
                                        .font(.subheadline)
                                        .foregroundColor(.gray)
                                }
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
                    }
                    .padding()
                }
                .background(Color(.systemGroupedBackground)) // Light gray background
            }
        }
        .onAppear {
            fetchThrowingActiveWarmups()
        }
    }

    func fetchThrowingActiveWarmups() {
        guard let url = URL(string: "\(baseURL)/api/player/throwing-active-warmups/\(playerId)/") else {
            errorMessage = "Invalid URL"
            isLoading = false
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    errorMessage = "Failed to load Throwing Active Warmups: \(error.localizedDescription)"
                    isLoading = false
                    return
                }

                guard let data = data else {
                    errorMessage = "No data received"
                    isLoading = false
                    return
                }

                do {
                    let decodedWarmups = try JSONDecoder().decode([ThrowingActiveWarmup].self, from: data)
                    self.throwingActiveWarmups = decodedWarmups
                    self.isLoading = false
                } catch {
                    errorMessage = "Failed to decode response: \(error.localizedDescription)"
                    isLoading = false
                }
            }
        }.resume()
    }
}