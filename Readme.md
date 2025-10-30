# Project: Credit Card Fraud Detection System

### Project Goal
To create a web application that can detect fraudulent credit card transactions with an F1-score and AUC-ROC score of over 0.75.

***

### Team Members & Roles
* **Divyansh Yadav:** ML & Backend
* **Divyansh Dwivedi:** Backend & ML
* **Dhruv Bhardwaj:** Data & Backend
* **Shreya Gupta:** Frontend & DevOps
* **Srishti Gupta:** Frontend & DevOps

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

#### **Phase 1: Data Acquisition & Preprocessing (Dhruv Bhardwaj, Divyansh Yadav, Divyansh Dwivedi)**
* **(Dhruv Bhardwaj) Download Dataset:** Use the Kaggle API to download the "Credit Card Data" dataset.
* **(Divyansh Yadav) Load Data:** Load the CSV file into a Pandas DataFrame in a Python environment (like VS Code).
* **(Dhruv Bhardwaj) Initial Exploration:** Check the data's structure, types, and look for missing values.
* **(Dhruv Bhardwaj) Data Cleaning:** Clean the data. For example, remove the '£' symbol from the 'Amount' column and convert it to a numeric type.
* **(Divyansh Yadav) Feature Engineering:** Create new features (e.g., time since last transaction, international transactions).
* **(Divyansh Dwivedi) Data Encoding:** Convert categorical features into a numerical format using one-hot encoding.
* **(Divyansh Yadav) Address Imbalance:** Use SMOTE to balance the dataset.
* **(Divyansh Yadav, Dhruv Bhardwaj, Divyansh Dwivedi) Final Data Prep:** Ensure the dataset is clean, balanced, and ready for model training.

<br>

#### **Phase 2: Model Building & Training (Divyansh Yadav, Dhruv Bhardwaj, Divyansh Dwivedi)**
* **(Divyansh Yadav) Split Data:** Split the dataset into training and testing sets.
* **(Divyansh Yadav) Select Models:** Use Logistic Regression and Random Forest.
* **(Divyansh Yadav) Train Models:** Train both models on the training data.
* **(Divyansh Dwivedi) Model Evaluation:** Make predictions, calculate metrics (F1-score, AUC-ROC), and analyze which model performs better. Divyansh Dwivedi will also create visualizations of the results.
* **(Divyansh Yadav, Dhruv Bhardwaj) Hyperparameter Tuning:** Fine-tune the best model to achieve a score above 0.75.

<br>

#### **Phase 3: Backend API & Database (Dhruv Bhardwaj, Shreya Gupta, Divyansh Yadav)**
* **(Dhruv Bhardwaj) Database Setup:** Set up a SQL database.
* **(Divyansh Dwivedi) Backend Environment:** Set up the Python backend with Flask.
* **(Divyansh Dwivedi) API Endpoint:** Create an API endpoint for predictions.
* **(Divyansh Yadav) Model Integration:** Integrate the final model into the backend API.
* **(Divyansh Dwivedi) API Logic:** Write the code to process data, call the model, and return the result.

<br>

#### **Phase 4: Frontend & User Interface (Divyansh Dwivedi, Srishti Gupta, Shreya Gupta)**
* **(Shreya Gupta) Frontend Structure:** Create the web page with HTML.
* **(Shreya Gupta) Frontend Styling:** Use CSS to style the page.
* **(Srishti Gupta) Frontend Interactivity:** Use JavaScript to handle user input.
* **(Srishti Gupta) API Communication:** Write JavaScript to send data to the API and receive responses.
* **(Shreya Gupta) Display Results:** Program the frontend to display the prediction dynamically.
* **(Divyansh Dwivedi) Frontend and Backend Integration:** Ensure the connection between the two is working.

<br>

#### **Phase 5: DevOps & Deployment (Shreya Gupta, Srishti Gupta)**
* **(Shreya Gupta) Containerization:** Use Docker to containerize the backend and frontend.
* **(Shreya Gupta) Cloud Setup:** Set up an account on AWS or Google Cloud.
* **(Shreya Gupta) Deployment:** Deploy the Docker containers to the cloud.
* **(Srishti Gupta) Testing:** Perform end-to-end testing of the live application.
* **(Srishti Gupta) Final Presentation:** Prepare a presentation of the entire project.