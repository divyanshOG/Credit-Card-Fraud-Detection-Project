# Project: Credit Card Fraud Detection System

### Project Goal
To create a web application that can detect fraudulent credit card transactions with an F1-score and AUC-ROC score of over 0.8.

***

### Team Members & Roles
* **Yadav:** ML & Backend Lead
* **Dhruv:** Data & Backend
* **Shreya:** Backend & DevOps
* **Gutka:** Frontend & DevOps
* **Dwivedi:** Frontend & ML

***

### Technologies Used
* **Python:** The main language for the backend and machine learning.
* **Pandas:** For data manipulation and preprocessing.
* **Scikit-learn:** For building and evaluating machine learning models.
* **Imblearn:** For handling the class imbalance problem.
* **Flask/Django:** A Python framework for building the backend API.
* **HTML, CSS, JavaScript:** For building the frontend web page.
* **SQL (MySQL/PostgreSQL):** For database management.
* **Git/GitHub:** For version control and team collaboration.
* **Docker:** For containerizing the application.
* **Cloud Platform (AWS/GCP):** For deploying the application.

***

### Project Roadmap

#### **Phase 1: Data Acquisition & Preprocessing (Dhruv, Yadav, Dwivedi)**
* **(Dhruv) Download Dataset:** Use the Kaggle API to download the "Credit Card Data" dataset.
* **(Yadav) Load Data:** Load the CSV file into a Pandas DataFrame in a Python environment (like VS Code).
* **(Dhruv) Initial Exploration:** Check the data's structure, types, and look for missing values.
* **(Dhruv) Data Cleaning:** Clean the data. For example, remove the '£' symbol from the 'Amount' column and convert it to a numeric type.
* **(Yadav) Feature Engineering:** Create new features (e.g., time since last transaction, international transactions).
* **(Dwivedi) Data Encoding:** Convert categorical features into a numerical format using one-hot encoding.
* **(Yadav) Address Imbalance:** Use SMOTE to balance the dataset.
* **(Yadav, Dhruv, Dwivedi) Final Data Prep:** Ensure the dataset is clean, balanced, and ready for model training.

<br>

#### **Phase 2: Model Building & Training (Yadav, Dhruv, Dwivedi)**
* **(Yadav) Split Data:** Split the dataset into training and testing sets.
* **(Yadav) Select Models:** Use Logistic Regression and Random Forest.
* **(Yadav) Train Models:** Train both models on the training data.
* **(Dwivedi) Model Evaluation:** Make predictions, calculate metrics (F1-score, AUC-ROC), and analyze which model performs better. Dwivedi will also create visualizations of the results.
* **(Yadav, Dhruv) Hyperparameter Tuning:** Fine-tune the best model to achieve a score above 0.8.

<br>

#### **Phase 3: Backend API & Database (Dhruv, Shreya, Yadav)**
* **(Dhruv) Database Setup:** Set up a SQL database.
* **(Shreya) Backend Environment:** Set up the Python backend with Flask.
* **(Shreya) API Endpoint:** Create an API endpoint for predictions.
* **(Yadav) Model Integration:** Integrate the final model into the backend API.
* **(Shreya) API Logic:** Write the code to process data, call the model, and return the result.

<br>

#### **Phase 4: Frontend & User Interface (Dwivedi, Gutka, Shreya)**
* **(Dwivedi) Frontend Structure:** Create the web page with HTML.
* **(Dwivedi) Frontend Styling:** Use CSS to style the page.
* **(Gutka) Frontend Interactivity:** Use JavaScript to handle user input.
* **(Gutka) API Communication:** Write JavaScript to send data to the API and receive responses.
* **(Dwivedi) Display Results:** Program the frontend to display the prediction dynamically.
* **(Shreya) Frontend and Backend Integration:** Ensure the connection between the two is working.

<br>

#### **Phase 5: DevOps & Deployment (Shreya, Gutka)**
* **(Shreya) Containerization:** Use Docker to containerize the backend and frontend.
* **(Shreya) Cloud Setup:** Set up an account on AWS or Google Cloud.
* **(Shreya) Deployment:** Deploy the Docker containers to the cloud.
* **(Gutka) Testing:** Perform end-to-end testing of the live application.
* **(Shreya) Final Presentation:** Prepare a presentation of the entire project.