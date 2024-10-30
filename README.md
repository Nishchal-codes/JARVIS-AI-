
---

# JARVIS - Your Advanced AI Personal Assistant

Welcome to **JARVIS**, an AI-powered personal assistant built to simplify your daily tasks with ease and efficiency. Designed for flexible interaction, JARVIS can switch between voice-based and text-based chat modes, combining natural language understanding with a sleek, custom GUI.

## 🌟 Key Features

- **Voice and Text Interaction**: JARVIS can operate through both voice commands and chat mode, making it adaptable to different user preferences.
- **CustomTkinter Interface**: The GUI is built using CustomTkinter, providing a clean, responsive window with interactive response and query sections.
- **Cohere API Integration**: For generating thoughtful, context-aware responses to user queries, JARVIS uses the Cohere language model.
- **Spotify and Web Support**: JARVIS can play music from Spotify and open websites directly, making it versatile for entertainment and productivity.
- **Weather Updates**: Integrated with WeatherAPI, JARVIS provides real-time weather information for the Raipur region.
- **Session-Based Context Management**: Each interaction in chat mode maintains session context, allowing for smooth, continuous conversations.

---

## 📂 Project Structure

- **jarvis_ai.py**: The main application file, managing voice activation, voice-to-text conversion, and core logic handling.
- **chat_interface.py**: Contains the CustomTkinter chat GUI, which processes text input and displays animated responses from JARVIS.
- **API_CREDENTIALS.env**: Stores sensitive API keys and credentials for secure access to Cohere, Spotify, and WeatherAPI (not included in this repository).

---

## 🛠️ Tech Stack

- **Python Libraries**: `customtkinter`, `requests`, `pyttsx3`, `speech_recognition`, `cohere`, `spotipy`
- **APIs**: Cohere (for NLP), WeatherAPI, and Spotify API
- **Environment**: CustomTkinter-based GUI with CustomTkinter framework integration for styling and ease of interaction.

---

## 🚀 Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/JARVIS.git
   cd JARVIS
   ```

2. **Set Up API Keys**:
   - Create an `.env` file and add your API keys following this format:
     ```
     api_key=your_cohere_api_key
     wapi_key=your_weather_api_key
     client_id=your_spotify_client_id
     client_secret=your_spotify_client_secret
     ```

3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run JARVIS**:
   ```bash
   python jarvis_ai.py
   ```

---

## 📄 License

This project is not currently licensed for public use. All rights are reserved by Nishchal Sahu. For inquiries, please reach out directly.

---

## 🤝 Contributing

Your ideas and feedback are welcome! If you have suggestions or would like to collaborate, feel free to open issues or reach out.

---

