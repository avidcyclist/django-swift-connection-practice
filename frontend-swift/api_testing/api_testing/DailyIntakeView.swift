import SwiftUI

struct DailyIntakeView: View {
    let playerId: Int
    @State private var dailyIntakes: [DailyIntake] = [] // List of daily intakes
    @State private var isLoading = true
    @State private var errorMessage: String? = nil
    @State private var showNewLogForm = false // State to show the new log form

    var body: some View {
        VStack {
            if isLoading {
                ProgressView("Loading Daily Intakes...")
            } else if let errorMessage = errorMessage {
                Text("Error: \(errorMessage)")
                    .foregroundColor(.red)
            } else {
                List(dailyIntakes, id: \.id) { intake in
                    VStack(alignment: .leading) {
                        Text("Date: \(intake.date)")
                        Text("Arm Feel: \(intake.armFeel ?? 0)")
                        Text("Body Feel: \(intake.bodyFeel ?? 0)")
                        Text("Sleep Hours: \(intake.sleepHours ?? 0.0)")
                        Text("Weight: \(intake.weight ?? 0.0)")
                        Text("Comments: \(intake.comments ?? "No comments")")
                    }
                }
            }

            // Button to create a new log
            Button(action: {
                showNewLogForm = true
            }) {
                Text("Create New Log")
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(8)
            }
            .padding()
        }
        .onAppear {
            Task {
                await fetchDailyIntakes()
            }
        }
        .sheet(isPresented: $showNewLogForm) {
            NewDailyIntakeView(playerId: playerId) { newLog in
                // Add the new log to the list and refresh the view
                dailyIntakes.insert(newLog, at: 0)
            }
        }
        .navigationTitle("Daily Intake")
        .padding()
    }

    private func fetchDailyIntakes() async {
        guard let url = URL(string: "\(baseURL)/api/daily-intakes/?player_id=\(playerId)") else {
            errorMessage = "Invalid URL for fetching daily intakes"
            isLoading = false
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        do {
            let (data, _) = try await URLSession.shared.data(for: request)
            let dailyIntakes = try JSONDecoder().decode([DailyIntake].self, from: data)
            DispatchQueue.main.async {
                self.dailyIntakes = dailyIntakes
                self.isLoading = false
            }
        } catch {
            DispatchQueue.main.async {
                self.errorMessage = "Error fetching daily intakes: \(error.localizedDescription)"
                self.isLoading = false
            }
        }
    }
}
