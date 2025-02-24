# Sign_bot: Bridging Communication for the Hearing-Impaired

## Overview
Welcome to **Signblang_chatbot** — a groundbreaking digital assistant designed to break down communication barriers between hearing-impaired individuals and the broader community. 🌍

Sign_bot combines the power of **Natural Language Processing (NLP)** and **Computer Vision (CV)** to create a seamless interaction between text and sign language. By interpreting text input and responding with corresponding sign language animations or text, Sign_bot facilitates real-time, fluent conversations. Whether you're communicating with deaf individuals or simply learning more about sign language, Sign_bot is here to empower and connect people like never before! 🤝

This open-source project leverages deep learning models and a robust dataset of sign language gestures to ensure accurate, real-time gesture recognition and language translation.

**Tech Stack:**
- **Mobile App**: Flutter & Dart
- **Backend**: Django
- **Model Development**: Deep learning,NLP
- **Languages**: Python,Dart

## Features:
- Real-time translation of **sign language gestures** to **text or spoken language**.
- **Text input** is converted into corresponding **sign language gestures**.
- Built with **deep learning models** for gesture recognition.
- Uses **LangChain framework** for chatbot integrations.
- Mobile app interface built with **Flutter**, ensuring cross-platform support.
## Project directory structure
Directory structure:
└── poojitha319-signlang_chatbot/
    ├── README.md
    ├── chatbot.iml
    ├── main.dart
    ├── pubspec.yaml
    ├── .flutter-plugins
    ├── .flutter-plugins-dependencies
    ├── android
    ├── assets/
    ├── backend/
    │   ├── backend/
    │   │   └── __pycache__/
    │   └── backendChat/
    │       ├── __pycache__/
    │       └── migrations/
    │           └── __pycache__/
    ├── ios/
    │   ├── Flutter/
    ├── lib/
    │   ├── firebase_options.dart
    │   ├── main.dart
    │   ├── speech.dart
    │   ├── screens/
    │   │   ├── chat_screen.dart
    │   │   └── message.dart
    │   └── widgets/
    │       ├── login.dart
    │       ├── profile.dart
    │       └── signup.dart
    ├── linux
    ├── macos
    ├── sign/
    │   ├── db.sqlite3
    │   ├── manage.py
    │   ├── media/
    │   │   ├── dl_models/
    │   │   │   └── sign_to_text/
    │   │   │       ├── action.h5
    │   │   │       ├── asl_classifier.h5
    │   │   │       ├── smnist.h5
    │   │   │       └── notebooks/
    │   │   │           ├── ASL_train.ipynb
    │   │   │           └── train (1).py
    │   │   └── videos/
    │   ├── sign/
    │   │   ├── __init__.py
    │   │   ├── asgi.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   ├── wsgi.py
    │   │   └── __pycache__/
    │   └── signlang/
    │       ├── __init__.py
    │       ├── admin.py
    │       ├── apps.py
    │       ├── models.py
    │       ├── serializers.py
    │       ├── tests.py
    │       ├── urls.py
    │       ├── views.py
    │       ├── __pycache__/
    │       ├── dl_models/
    │       │   ├── models/
    │       │   │   ├── action.h5
    │       │   │   ├── sign.hdf5
    │       │   │   └── smnist.h5
    │       │   ├── sign_language_translator/
    │       │   │   ├── __init__.py
    │       │   │   ├── cli.py
    │       │   │   ├── config/
    │       │   │   │   ├── __init__.py
    │       │   │   │   ├── assets.py
    │       │   │   │   ├── colors.py
    │       │   │   │   ├── enums.py
    │       │   │   │   ├── settings.py
    │       │   │   │   ├── urls.json
    │       │   │   │   └── utils.py
    │       │   │   ├── languages/
    │       │   │   │   ├── __init__.py
    │       │   │   │   ├── utils.py
    │       │   │   │   ├── vocab.py
    │       │   │   │   ├── sign/
    │       │   │   │   │   ├── __init__.py
    │       │   │   │   │   ├── mapping_rules.py
    │       │   │   │   │   └── sign_language.py
    │       │   │   │   └── text/
    │       │   │   │       ├── __init__.py
    │       │   │   │       ├── english.py
    │       │   │   │       ├── hindi.py
    │       │   │   │       └── text_language.py
    │       │   │   ├── models/
    │       │   │   │   ├── __init__.py
    │       │   │   │   ├── _utils.py
    │       │   │   │   ├── utils.py
    │       │   │   │   ├── language_models/
    │       │   │   │   │   ├── __init__.py
    │       │   │   │   │   ├── abstract_language_model.py
    │       │   │   │   │   ├── beam_sampling.py
    │       │   │   │   │   ├── mixer.py
    │       │   │   │   │   ├── ngram_language_model.py
    │       │   │   │   │   └── transformer_language_model/
    │       │   │   │   │       ├── __init__.py
    │       │   │   │   │       ├── layers.py
    │       │   │   │   │       ├── model.py
    │       │   │   │   │       └── train.py
    │       │   │   │   ├── sign_to_text/
    │       │   │   │   │   └── __init__.py
    │       │   │   │   └── text_to_sign/
    │       │   │   │       ├── __init__.py
    │       │   │   │       ├── concatenative_synthesis.py
    │       │   │   │       └── t2s_model.py
    │       │   │   ├── text/
    │       │   │   │   ├── __init__.py
    │       │   │   │   ├── metrics.py
    │       │   │   │   ├── preprocess.py
    │       │   │   │   ├── subtitles.py
    │       │   │   │   ├── synonyms.py
    │       │   │   │   ├── tagger.py
    │       │   │   │   ├── tokenizer.py
    │       │   │   │   └── utils.py
    │       │   │   ├── utils/
    │       │   │   │   ├── __init__.py
    │       │   │   │   ├── archive.py
    │       │   │   │   ├── arrays.py
    │       │   │   │   ├── download.py
    │       │   │   │   ├── parallel.py
    │       │   │   │   ├── tree.py
    │       │   │   │   └── utils.py
    │       │   │   └── vision/
    │       │   │       ├── __init__.py
    │       │   │       ├── _utils.py
    │       │   │       ├── utils.py
    │       │   │       ├── landmarks/
    │       │   │       │   ├── __init__.py
    │       │   │       │   ├── connections.py
    │       │   │       │   ├── display.py
    │       │   │       │   └── landmarks.py
    │       │   │       ├── sign/
    │       │   │       │   ├── __init__.py
    │       │   │       │   ├── sign.py
    │       │   │       │   └── transformations.py
    │       │   │       └── video/
    │       │   │           ├── __init__.py
    │       │   │           ├── display.py
    │       │   │           ├── transformations.py
    │       │   │           ├── video.py
    │       │   │           └── video_iterators.py
    │       │   ├── sign_to_text/
    │       │   │   ├── action.h5
    │       │   │   ├── asl_classifier.h5
    │       │   │   ├── smnist.h5
    │       │   │   └── notebooks/
    │       │   │       ├── ASL_train.ipynb
    │       │   │       └── action.py.py
    │       │   ├── text_to_sign/
    │       │   │   └── notebooks/
    │       │   │       ├── text_sign.py
    │       │   │       └── use-less.py
    │       │   └── videos/
    │       └── migrations/
    │           ├── 0001_initial.py
    │           ├── 0002_video.py
    │           ├── __init__.py
    │           └── __pycache__/
    ├── test/
    │   └── widget_test.dart
    ├── web/
    │   ├── index.html
    │   ├── manifest.json
    │   └── icons/
    ├── widgets/
    │   ├── login.dart
    │   ├── profile.dart
    │   └── signup.dart
    └── .dart_tool

## 📥 Installation (Flutter Front-End)

### **Prerequisites**
- **Flutter SDK**: Install from [Flutter Installation Guide](https://flutter.dev/docs/get-started/install).
- **Firebase Account**: Create a Firebase project for authentication and database integration.

### **Steps to Install**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Poojitha319/signlang_chatbot.git
   cd SignSiksha_SIH
2.**Get all requirements**:
```bash
   flutter pub get
   ```
3.**Run the app**:
```bash
   flutter run
   ```
## 🌐Backend Setup
1.**Clone the backend repository**:
   ```bash
   git clone https://github.com/Poojitha319/signlang_chatbot.git
   cd backend
   ```
2.**Install required dependencies**:
  ```bash
   pip install -r requirements.txt
   ```
3.**Configure databases**:
  Open settings file and set up your database configurations.
4.**Run database migrations**:
```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5.**Run the server**:
```bash
   python manage.py runserver
   ```
Conclusion

Sign_bot is more than just a chatbot—it's a revolutionary step towards bridging communication gaps and fostering inclusivity for the hearing-impaired community. By integrating cutting-edge AI technologies, we are making sign language more accessible, enabling effortless communication, and empowering users worldwide. Join us in revolutionizing communication accessibility! 

