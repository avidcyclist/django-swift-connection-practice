import SwiftUI

struct ArmCareRoutineView: View {
    let playerId: Int
    @StateObject private var viewModel = ArmCareRoutineViewModel()

    var body: some View {
        VStack {
            if viewModel.isLoading {
                ProgressView("Loading...")
            } else if let errorMessage = viewModel.errorMessage {
                Text(errorMessage)
                    .foregroundColor(.red)
                    .padding()
            } else if let routine = viewModel.routine {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        Text(routine.routineName)
                            .font(.largeTitle)
                            .fontWeight(.bold)
                            .padding(.bottom, 10)

                        Text("Description: \(routine.description ?? "No description available.")")
                            .font(.subheadline)
                            .foregroundColor(.gray)

                        ForEach(viewModel.groupedExercises.keys.sorted(), id: \.self) { day in
                            if let exercises = viewModel.groupedExercises[day] {
                                VStack(alignment: .leading, spacing: 10) {
                                    Text("Day \(day)")
                                        .font(.title2)
                                        .fontWeight(.semibold)
                                        .padding(.top, 10)

                                    ForEach(exercises) { exercise in
                                        VStack(alignment: .leading, spacing: 5) {
                                            Text("Focus: \(exercise.focus ?? "N/A")")
                                                .font(.headline)
                                            Text("Exercise: \(exercise.exercise)")
                                            Text("Sets/Reps: \(exercise.setsReps ?? "N/A")")
                                            if let youtubeLink = exercise.youtubeLink, !youtubeLink.isEmpty {
                                                Link("Watch Video", destination: URL(string: youtubeLink)!)
                                                    .foregroundColor(.blue)
                                            }
                                        }
                                        .padding()
                                        .background(Color(.systemGray6))
                                        .cornerRadius(8)
                                    }
                                }
                            }
                        }
                    }
                    .padding()
                }
            } else {
                Text("No routine data available.")
                    .foregroundColor(.gray)
                    .padding()
            }
        }
        .onAppear {
            viewModel.fetchRoutine(playerId: playerId)
        }
        .navigationTitle("Arm Care Routine")
        .navigationBarTitleDisplayMode(.inline)
    }
}