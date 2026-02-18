// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", () => {

    const fraudForm = document.getElementById("fraud-form");
    const resultDiv = document.getElementById("result");
    const predictionText = document.getElementById("prediction-text");
    const probabilityScore = document.getElementById("probability-score");

    fraudForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent page reload

        resultDiv.style.display = "block";
        predictionText.textContent = "Checking...";
        probabilityScore.textContent = "Please wait...";
        predictionText.className = "";

        const formData = new FormData(fraudForm);
        const data = {};

        formData.forEach((value, key) => {
            if (key === 'Amount' || key === 'Age') {
                data[key] = parseFloat(value);
            } else if (typeof value === 'string') {
                // Normalize strings to Title Case & trim spaces
                data[key] = value.trim().split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ');
            } else {
                data[key] = value;
            }
        });

        // Handle known abbreviations explicitly
        if (data['Country of Transaction'].toUpperCase() === 'USA') data['Country of Transaction'] = 'USA';
        if (data['Country of Residence'].toUpperCase() === 'USA') data['Country of Residence'] = 'USA';
        if (data['Shipping Address'].toUpperCase() === 'USA') data['Shipping Address'] = 'USA';
        if (data['Country of Transaction'].toUpperCase() === 'UAE') data['Country of Transaction'] = 'UAE';
        if (data['Country of Residence'].toUpperCase() === 'UAE') data['Country of Residence'] = 'UAE';
        if (data['Shipping Address'].toUpperCase() === 'UAE') data['Shipping Address'] = 'UAE';

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if(result.error){
                predictionText.textContent = "Error";
                probabilityScore.textContent = result.error;
                predictionText.className = 'prediction-fraud';
                return;
            }

            predictionText.textContent = result.prediction;
            probabilityScore.textContent = `Confidence Score: ${(result.probability_score * 100).toFixed(2)}%`;
            predictionText.className = result.prediction === 'Fraudulent' ? 'prediction-fraud' : 'prediction-legitimate';
        })
        .catch(error => {
            console.error('Error:', error);
            predictionText.textContent = "Error";
            probabilityScore.textContent = "Could not connect to the API.";
            predictionText.className = 'prediction-fraud';
        });
    });
});
