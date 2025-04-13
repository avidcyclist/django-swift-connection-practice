import Foundation

class ArmCareRoutineViewModel: ObservableObject {
    @Published var routine: ArmCareRoutineResponse?
    @Published var groupedExercises: [Int: [ArmCareExercise]] = [:] // Grouped by day
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    func fetchRoutine(playerId: Int) {
        guard let url = URL(string: "\(baseURL)/api/player-arm-care-routines/grouped-by-day/\(playerId)/") else {
            self.errorMessage = "Invalid URL"
            return
        }
        
        self.isLoading = true
        self.errorMessage = nil
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            DispatchQueue.main.async {
                self.isLoading = false
                
                if let error = error {
                    self.errorMessage = "Error: \(error.localizedDescription)"
                    return
                }
                
                guard let data = data else {
                    self.errorMessage = "No data received"
                    return
                }
                
                do {
                    // Decode the response as a single object
                    let decodedResponse = try JSONDecoder().decode(ArmCareRoutineResponse.self, from: data)
                    self.routine = decodedResponse
                    
                    // Manually convert the `days` dictionary keys from String to Int
                    var groupedExercises: [Int: [ArmCareExercise]] = [:]
                    for (key, value) in decodedResponse.days {
                        if let intKey = Int(key) {
                            groupedExercises[intKey] = value
                        }
                    }
                    self.groupedExercises = groupedExercises
                } catch {
                    self.errorMessage = "Failed to decode response: \(error.localizedDescription)"
                }
            }
        }.resume()
    }
}
