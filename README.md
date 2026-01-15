# 📧 Spam Email Detector (Streamlit + Machine Learning)

A Streamlit web application that detects whether an email is **Spam** or **Not Spam** using a trained Machine Learning model.

The UI allows users to:
- ✅ Paste an email message
- ✅ Upload an email file (`.txt` or `.eml`)
- ✅ Get instant prediction with spam probability

## 🚀 Features
- **Streamlit UI** (fast & simple)
- **Single email prediction**
- Upload email in **.txt** or **.eml**
- Clear input + output using **Clear** button
- Uses a **pre-trained model (`spam_model.pkl`)** for fast results

## 🧠 Model Used
This project uses the Notebook-trained ML pipeline:

- **Text Feature Extraction:** `CountVectorizer`
- **Classifier:** `Multinomial Naive Bayes (MultinomialNB)`
- Output:
  - `Spam`
  - `Not Spam`
  - Spam Probability (if supported)

The trained model is stored in:

✅ `spam_model.pkl`

---

## 📂 Project Structure
```
spam-email-detector/
│
├── app.py  (Streamlit UI application)
├── spam_model.pkl  (Trained ML model (Notebook output))
├── requirements.txt  (Required libraries)
├── README.md  (Project documentation)
├── spam.csv  (Dataset)
├── run_app.bat  (Windows launcher (optional))
└── email_spam_detection.ipynb  (Training notebook (optional))
```

---

## ⚙️ Requirements
Make sure you have:
- Python 3.8+
- pip installed

---

The project works in 3 parts :


1️⃣ Dataset (spam.csv) (pre-processing)


Dataset contains emails and labels.
Example columns:
Message = email text
Category = label (spam or ham)


2️⃣ Training Model in Notebook (.ipynb)


-Step A: It reads dataset,

-Step B: Separate X and y
  -X = messages
  -y = label

-Step C: Convert text into numbers using CountVectorizer

-Step D: Train ML Algorithm
  -Algorithm: Multinomial Naive Bayes

-Step E: Save trained model
  -file : spam_model.pkl


3️⃣ Streamlit UI (app.py)


-> Load model <br>
-> Take user input <br>
-> Predict result <br>
-> Display output <br>

What run_app.bat contains

the command for run this project, you can directly run this by write the command in your terminal where your project directory is 
command : python -m streamlit run app.py

=> For run this simply double click on run_app.bat

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

![Streamlit](https://img.shields.io/badge/Streamlit-App-red)

![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange)

![Accuracy](https://img.shields.io/badge/Accuracy-99%25-success)
