🔍 TrustLens AI

AI-Based Multilingual Scam Detection & Digital Fraud Awareness Platform

TrustLens AI is an AI-powered web platform designed to help users identify scam messages, suspicious links, images, and audio-based fraud attempts.

The platform focuses on making scam detection simple and accessible by supporting English, Hindi, Marathi, and Hinglish.

 🚨 Problem

Online scams are becoming increasingly common through:

* 📱 SMS and chat messages
* 🔗 Suspicious links
* 🖼️ Scam screenshots and images
* 🎙️ Fraudulent audio messages
* 💼 Fake job and internship offers
* 🎁 Lottery and prize scams
* 💳 Banking and UPI fraud
* 🔐 Fake account/KYC verification messages

Many users cannot easily recognize these scams, especially when messages are written in regional languages.

 💡 Our Solution

TrustLens AI analyzes the content provided by the user and gives an easy-to-understand safety assessment.

It provides:

* 📊 Scam probability
* ⚠️ Risk level
* 🔎 Reasons behind the detection
* 🛡️ Safety recommendations
* 🌐 Multilingual analysis
* 🚨 Scam reporting support

 ✨ Key Features

 1. 💬 Text Scam Detection

Users can enter a suspicious message and TrustLens AI analyzes it using a machine-learning model.

The system provides:

Scam Probability → Risk Level → Reasons → Safety Tips

 2. 🌐 Multilingual Scam Detection

The platform supports:

* English
* Hindi
* Marathi
* Hinglish

This helps users detect scams even when the message is not written in English.

 3. 🔗 Fake Link Detection

TrustLens AI checks suspicious URLs and identifies warning signs such as:

* HTTP connections
* Suspicious keywords
* Prize/winner/claim-related links
* Other risky URL patterns

 4. 🖼️ Screenshot Detection

Users can upload screenshots or images containing suspicious messages.

Using OCR (Optical Character Recognition), TrustLens AI extracts the text from the image and analyzes it for possible scam indicators.

 5. 🎙️ Audio Scam Detection

Users can upload an audio message.

The system:

Audio → Speech-to-Text → Scam Detection → Risk Analysis

Whisper is used for speech transcription.

6. 🔊 Text-to-Speech Results

Users can choose to receive the analysis as text or audio.

The platform can convert the result into speech using gTTS.

 7. 🌍 Translation Support

The system can translate scam analysis into supported languages, making the results easier to understand.

 8. 🛡️ Scam Awareness Mode

TrustLens AI also provides educational information about common scams and safety practices.

The goal is not only to detect scams but also to help users recognize and avoid them in the future.

9. 🚨 Report Scam

Users can report suspicious scam content, helping create awareness and support safer digital practices.

 🤖 Machine Learning

TrustLens AI uses TF-IDF and Logistic Regression for text classification.

The model is trained using a combined multilingual dataset containing scam and legitimate messages.

The dataset includes:

* English
* Hindi
* Marathi
* Hinglish


The final dataset contains 29,163 records.

 🏗️ Technology Stack

# Frontend

* HTML
* CSS
* JavaScript

# Backend

* Python
* Flask

# Machine Learning

* Scikit-learn
* TF-IDF
* Logistic Regression
* Joblib

# AI / NLP

* Whisper
* LangDetect
* Deep Translator

# Image Processing

* Tesseract OCR
* Pytesseract
* Pillow

# Audio

* Whisper
* gTTS
* Pydub
* FFmpeg

# Database

* SQL Lite Database

 📁 Project Structure


TrustLensAI/
│
├── app.py
├── detect.py
├── link_detector.py
├── database.py
├── ocr.py
├── translator.py
|__ train_model.py
|__ prepare_datasets.py
|__ audio_detector.py
├── requirements.txt
│
├── model/
│   └── multilingual_models.pkl
│
├── dataset/
│   └── combined_scam_dataset.csv
│
├── templates/
│   ├── home.html
│   ├── about.html
|   |__ report.html
│   |__ link_check.html
│   |__ privacy.html
│   |__ success.html
│   ├── awareness.html
│   ├── contact.html
│   ├── dashboard.html
│   └── result.html
│

🔄 How It Works


User Input
    ↓
Text / Link / Image / Audio
    ↓
Preprocessing
    ↓
AI / ML Analysis
    ↓
Scam Probability
    ↓
Risk Classification
    ↓
Reasons & Safety Tips
    ↓
Text / Audio Result

🎯 Objective

The main objective of TrustLens AI is to make digital fraud detection easier, faster, and more accessible, especially for users who communicate in regional Indian languages.

Instead of simply saying "Scam" or "Not Scam", TrustLens AI explains why the content may be dangerous and what the user should do next.

🚀 Future Scope

Possible future improvements include:

* WhatsApp/Telegram scam detection integration
* Real-time browser protection
* Mobile application
* Voice-call scam detection
* More Indian regional languages
* Improved AI models
* Community-based scam reporting
* Real-time suspicious-link intelligence
* Personalized fraud awareness
