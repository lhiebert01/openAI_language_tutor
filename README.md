# 🌍 GenAI Language Learning Tutor

An advanced AI-powered language learning application that provides interactive conversations with text-to-speech capabilities across multiple languages. Practice your language skills with a patient, adaptive AI tutor!

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://genai-language-tutor.streamlit.app)

## ✨ Features

- **Multiple Language Support**:
  - Spanish 🇪🇸
  - French 🇫🇷
  - German 🇩🇪
  - Italian 🇮🇹
  - Japanese 🇯🇵
  - Korean 🇰🇷
  - Chinese 🇨🇳

- **Interactive Learning Experience**:
  - Real-time conversations with AI tutor
  - Text-to-Speech functionality for pronunciation practice
  - Adjustable proficiency levels (Beginner, Intermediate, Advanced)
  - Quick example phrases for common situations

- **Customizable Learning Components**:
  - Pronunciation guides
  - English translations
  - Grammar corrections and suggestions
  - Save conversations for later review

- **User-Friendly Interface**:
  - Clean, intuitive design
  - Mobile-responsive layout
  - Easy-to-use chat interface
  - Visual language selection

## 🚀 Quick Start

1. Visit [GenAI Language Tutor](https://genai-language-tutor.streamlit.app)
2. Select your target language and proficiency level
3. Choose your preferred learning components
4. Start practicing with quick examples or type your own phrases
5. Listen to pronunciations and receive instant feedback

## 💻 Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/lhiebert01/openAI_language_tutor.git
   cd openAI_language_tutor
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.template .env
   ```
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## ⚙️ Configuration

The application can be configured through the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)

Additional configuration options are available through the Streamlit interface:
- Language selection
- Proficiency level
- Display components (pronunciation, translation, corrections)

## 🔧 Technical Features

- **AI Model**: Uses OpenAI's GPT-4 for natural language understanding and generation
- **Text-to-Speech**: Implements gTTS (Google Text-to-Speech) for pronunciation
- **Frontend**: Built with Streamlit for a responsive web interface
- **Session Management**: Maintains conversation history and user preferences
- **File Handling**: Supports conversation export and audio generation

## 🛠️ Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add your feature description"
   ```
4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

Developed by [Lindsay Hiebert](https://www.linkedin.com/in/lindsayhiebert/) ([GitHub](https://github.com/lhiebert01))

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 API
- Streamlit for the web framework
- Google Text-to-Speech for pronunciation capabilities
 

---