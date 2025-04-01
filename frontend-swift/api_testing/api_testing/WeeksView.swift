import SwiftUI

struct WeeksView: View {
    let playerId: Int
    @State private var weeks: [String: WeekDetails] = [:]
    @State private var phaseName: String = "Loading..."
    @State private var showErrorAlert: Bool = false
    @State private var errorMessage: String = ""

    var body: some View {
        VStack {
            Text(phaseName)
                .font(.largeTitle)
                .padding()

            if weeks.isEmpty {
                Text("Loading weeks...")
                    .foregroundColor(.gray)
                    .padding()
            } else {
                List(weeks.keys.sorted(), id: \.self) { week in
                    NavigationLink(destination: DaysView(playerId: playerId, week: week, days: weeks[week]?.days ?? [:])) {
                        Text("Week \(week)")
                            .font(.headline)
                            .padding()
                    }
                }
            }
        }
        .onAppear {
            fetchWeeks()
        }
        .alert(isPresented: $showErrorAlert) {
            Alert(
                title: Text("Error"),
                message: Text(errorMessage),
                dismissButton: .default(Text("OK"))
            )
        }
    }

    func fetchWeeks() {
        guard let url = URL(string: "\(baseURL)/api/player-phases/\(playerId)/workouts-by-week/") else {
            errorMessage = "Invalid URL"
            showErrorAlert = true
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    errorMessage = "Error: \(error.localizedDescription)"
                    showErrorAlert = true
                }
                return
            }

            if let data = data {
                do {
                    let response = try JSONDecoder().decode(PhaseWorkoutsResponse.self, from: data)
                    DispatchQueue.main.async {
                        self.phaseName = response.phaseName
                        self.weeks = response.weeks
                    }
                } catch {
                    DispatchQueue.main.async {
                        errorMessage = "Error decoding JSON"
                        showErrorAlert = true
                    }
                }
            }
        }.resume()
    }
}