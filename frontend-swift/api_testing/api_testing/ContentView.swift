//
//  ContentView.swift
//  api_testing
//
//  Created by user271568 on 3/26/25.
//

import SwiftUI

struct ContentView: View {
    @State private var apiResponse: String = "Loading..." // State variable to store API response

    var body: some View {
        VStack {
            Text(apiResponse) // Display the API response
                .padding()
                .multilineTextAlignment(.center)
                .onAppear {
                    fetchAPIResponse() // Call the API when the view appears
                }
        }
    }

    // Function to fetch the API response
    func fetchAPIResponse() {
        guard let url = URL(string: "https://ce30-2601-246-8101-eff0-40fd-799a-6b28-c7b8.ngrok-free.app/api/test/") else {
            apiResponse = "Invalid URL"
            return
        }

        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    apiResponse = "Error: \(error.localizedDescription)"
                }
                return
            }

            if let data = data, let responseString = String(data: data, encoding: .utf8) {
                DispatchQueue.main.async {
                    apiResponse = responseString // Update the UI with the API response
                }
            } else {
                DispatchQueue.main.async {
                    apiResponse = "No data received"
                }
            }
        }

        task.resume()
    }
}

#Preview {
    ContentView()
}
