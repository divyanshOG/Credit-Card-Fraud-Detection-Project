// Wait for the HTML document to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
    
    // Get references to the form and the result elements
    const fraudForm = document.getElementById("fraud-form");
    const resultDiv = document.getElementById("result");
    const predictionText = document.getElementById("prediction-text");
    const probabilityScore = document.getElementById("probability-score");

    // This is the most important part
    fraudForm.addEventListener("submit", (event) => {
        
        // THIS IS THE FIX:
        // Prevent the form from refreshing the page
        event.preventDefault();

        // Show the results div and set a "loading" message
        resultDiv.style.display = "block";
        predictionText.textContent = "Checking...";
        probabilityScore.textContent = "Please wait.";
        predictionText.className = ""; // Clear old color classes

        // 1. Get all the data from the form
        const formData = new FormData(fraudForm);
        
        // 2. Convert the form data into a simple JSON object
        const data = {};
        formData.forEach((value, key) => {
            // Convert numerical values from strings to numbers
            if (key === 'Amount' || key === 'Age') {
                data[key] = parseFloat(value);
            } else {
                data[key] = value;
            }
        });
        
        // 4. Send the data to the backend API using fetch()
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST', // Specify the method
            headers: {
                'Content-Type': 'application/json' // Tell the server we're sending JSON
            },
            body: JSON.stringify(data) // Convert the data object to a JSON string
        })
        .then(response => response.json()) // Parse the JSON response from the server
        .then(result => {
            // 5. We have the result! Now, display it.
            
            // Display the prediction text (e.g., "Fraudulent")
            predictionText.textContent = result.prediction;
            
            // Display the probability score
            const probabilityPercent = (result.probability_score * 100).toFixed(2);
            probabilityScore.textContent = `Confidence Score: ${probabilityPercent}%`;

            // Add the correct color class based on the prediction
            if (result.prediction === 'Fraudulent') {
                predictionText.className = 'prediction-fraud';
            } else {
                predictionText.className = 'prediction-legitimate';
            }
        })
        .catch(error => {
            // 6. Handle any errors
            console.error('Error:', error);
            resultDiv.style.display = "block";
            predictionText.textContent = "Error";
            probabilityScore.textContent = "Could not connect to the API. Is the server running?";
            predictionText.className = 'prediction-fraud';
        });
    });
});