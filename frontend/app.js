/// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    const fraudForm = document.getElementById("fraud-form") || document.getElementById("fraudForm");
    const resultDiv = document.getElementById("result");
    const predictionText = document.getElementById("prediction-text") || document.getElementById("predictionText");
    const probabilityScore = document.getElementById("probability-score") || document.getElementById("probabilityScore");

    if (!fraudForm) {
        console.error("❌ Error: Could not find the form element in HTML. Check your form ID.");
        return;
    }

    fraudForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Stop page reload

        if (resultDiv) resultDiv.style.display = "block";
        if (predictionText) {
            predictionText.textContent = "Checking...";
            predictionText.className = "";
        }
        if (probabilityScore) probabilityScore.textContent = "Please wait...";

        const formData = new FormData(fraudForm);
        const data = {};

        formData.forEach((value, key) => {
            if (key === 'Amount' || key === 'Age') {
                data[key] = Number(value);
            } else {
                data[key] = typeof value === 'string' ? value.trim() : value;
            }
        });

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                if (predictionText) {
                    predictionText.textContent = "Error";
                    predictionText.className = 'prediction-fraud';
                }
                if (probabilityScore) probabilityScore.textContent = result.error;
                return;
            }

            if (predictionText) {
                predictionText.textContent = result.prediction;
                predictionText.className = result.prediction === 'Fraudulent' ? 'prediction-fraud' : 'prediction-legitimate';
            }
            if (probabilityScore) {
                probabilityScore.textContent = `Confidence Score: ${(result.probability_score * 100).toFixed(2)}%`;
            }
        })
        .catch(error => {
            console.error('API Error:', error);
            if (predictionText) {
                predictionText.textContent = "Error";
                predictionText.className = 'prediction-fraud';
            }
            if (probabilityScore) probabilityScore.textContent = "Could not connect to the API.";
        });
    });
});