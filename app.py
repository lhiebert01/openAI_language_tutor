import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime
from gtts import gTTS
import tempfile
import time

# Load environment variables
load_dotenv(override=True)

# Configure OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to convert text to speech and play it
def text_to_speech(text, lang='en'):
    try:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        # Generate speech
        tts = gTTS(text=text, lang=lang)
        # Save to temporary file
        tts.save(temp_file.name)
        # Return the filename
        return temp_file.name
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        height: 2.2rem;
        background-color: #f0f2f6;
        color: #0e1117;
        border: 1px solid #e0e0e0;
        margin-bottom: 0.3rem;
        font-size: 0.9rem;
    }
    .stButton>button:hover {
        background-color: #e0e0e0;
        color: #0e1117;
        border: 1px solid #c0c0c0;
    }
    .action-button>button {
        background-color: #ff4b4b;
        color: white;
    }
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding: 0.5rem;
        border-radius: 0.5rem;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-top: 0.5rem;
    }
    .example-container {
        background-color: #ffffff;
        padding: 0.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .example-category {
        font-size: 0.9rem;
        font-weight: bold;
        margin-bottom: 0.3rem;
        color: #0e1117;
    }
    .example-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.3rem;
        margin-bottom: 0.5rem;
    }
    .block-container {
        padding: 1rem !important;
        max-width: 95% !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_ai_response(language, level, user_message, conversation_history, show_components):
    # Modify system prompt based on selected components
    components = []
    if show_components['pronunciation']:
        components.append("(Pronunciation: [Simple phonetic pronunciation guide])\\n")
    if show_components['translation']:
        components.append("Translation: [English translation]\\n")
    if show_components['corrections']:
        components.append("Corrections: [Any corrections or suggestions]\\n")
    
    system_prompt = f"""You are a helpful language learning partner for {language}. 
    Adjust to {level} level. Keep responses natural and simple. 
    Format your response with exactly these line breaks using '\\n':
    
    Response: [Phrase in {language}]\\n
    {"".join(components)}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                *conversation_history,
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.replace("\\n", "\n")
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "selected_example" not in st.session_state:
        st.session_state.selected_example = None
    
    # Main header with styling
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("✨ 🎓 🌍 GenAI Language Learning Tutor 🗣️ 🤖 ✨")
    st.markdown('<div style="text-align: left; font-size: 1.2em; font-weight: bold; margin-top: -0.5em; padding-bottom: 0.5em; padding-left: 1em;">⭐ Your OpenAI AI language learning companion ⭐ | Designed by <a href="https://www.linkedin.com/in/lindsayhiebert/" target="_blank" style="text-decoration: none; color: #0e76a8;">Lindsay Hiebert</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar settings
    with st.sidebar:
        try:
            st.image("AppImage.png", caption="Language Partner")
        except:
            st.write("Please add AppImage.png to your project directory")
        
        st.markdown("### 🎯 Learning Settings")
        language = st.selectbox(
            "Choose your language",
            [ "Spanish 🇪🇸", "French 🇫🇷", "German 🇩🇪", 
             "Italian 🇮🇹", "Japanese 🇯🇵", "Korean 🇰🇷", "Chinese 🇨🇳"]
        )
        level = st.select_slider(
            "Proficiency Level",
            options=["Beginner 🌱", "Intermediate 🌿", "Advanced 🌳"]
        )
        
        # Language code mapping for TTS
        lang_codes = {
            "Spanish 🇪🇸": "es",
            "French 🇫🇷": "fr",
            "German 🇩🇪": "de",
            "Italian 🇮🇹": "it",
            "Japanese 🇯🇵": "ja",
            "Korean 🇰🇷": "ko",
            "Chinese 🇨🇳": "zh-CN"
        }
        
        st.markdown("### 🔧 Display Options")
        show_components = {
            'pronunciation': st.toggle('Show Pronunciation', value=True),
            'translation': st.toggle('Show Translation', value=True),
            'corrections': st.toggle('Show Corrections', value=True)
        }

    # Create main container for chat interface
    main_container = st.container()

    with main_container:
        # Create two columns: examples on the left, chat interface on the right
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Quick Examples")
            example_categories = {
                "👋 Greetings": [
                    "Hello and Welcome, how are you today?",
                    "My name is Ms. GenAI Tutor. What is your name?"
        
                ],
                "🔢 Numbers": [
                    "Count numbers 1 to 10",
                    "What is the cost of these items, please?" 
                ],
                "🍽️ Dining": [
                    "I would like a cup a coffee, with milk and sugar please",
                     " May I please see menu"
                
                ],
                "🗺️ Directions": [
                    "Excuse me, Would you please tell me how to get to Train station? ",
                    "Where is the nearest pharmacy?"
                ]
            }

            st.markdown('<div class="example-container">', unsafe_allow_html=True)
            for category, phrases in example_categories.items():
                st.markdown(f'<div class="example-category">{category}</div>', unsafe_allow_html=True)
                for phrase in phrases:
                    if st.button(phrase, key=f"btn_{phrase}", help="Click to use this phrase"):
                        st.session_state.selected_example = phrase
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # If an example was selected, display it subtly
            if st.session_state.selected_example:
                st.caption(f"Ready to translate: {st.session_state.selected_example}")

            # User input
            user_message = st.chat_input(
                "Type your message here or select an example...",
                key="chat_input"
            )

            # Use selected example if available and user hasn't typed anything
            if st.session_state.selected_example and not user_message:
                user_message = st.session_state.selected_example
                st.session_state.selected_example = None
            
            # Action buttons
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("Clear Chat 🗑️", use_container_width=True):
                    st.session_state.conversation = []
                    st.rerun()
            with act_col2:
                if 'conversation' in st.session_state and st.session_state.conversation:
                    chat_content = "\n".join([
                        f"{'User' if msg['role']=='user' else 'Assistant'}: {msg['content']}"
                        for msg in st.session_state.conversation
                    ])
                    st.download_button(
                        "Save Chat 💾",
                        chat_content,
                        file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

            # Process new messages
            if user_message:
                # Display user message with TTS
                with st.chat_message("user"):
                    st.write(user_message)
                    original_audio = text_to_speech(user_message, 'en')
                    if original_audio:
                        st.audio(original_audio)
                
                ai_response = get_ai_response(
                    language.split()[0],
                    level.split()[0],
                    user_message,
                    st.session_state.get('conversation', []),
                    show_components
                )
                
                # Display assistant message
                with st.chat_message("assistant"):
                    components = ai_response.split('\n')
                    for component in components:
                        if component.strip():
                            st.markdown(component)
                            if component.startswith("Response:"):
                                translated_text = component.replace("Response:", "").strip()
                                lang_code = lang_codes.get(language, "en")
                                translated_audio = text_to_speech(translated_text, lang_code)
                                if translated_audio:
                                    st.audio(translated_audio)
                                    st.markdown(
                                        f"""
                                        <script>
                                            const audio = document.querySelector('audio[src="{translated_audio}"]');
                                            audio.play();
                                        </script>
                                        """,
                                        unsafe_allow_html=True
                                    )
                
                # Add to conversation history
                st.session_state.conversation.extend([
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": ai_response}
                ])
            
            # Display conversation history
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for message in st.session_state.get('conversation', []):
                with st.chat_message(message["role"]):
                    if message["role"] == "assistant":
                        components = message["content"].split('\n')
                        for comp in components:
                            if comp.strip():
                                st.markdown(comp)
                                if comp.startswith("Response:"):
                                    translated_text = comp.replace("Response:", "").strip()
                                    lang_code = lang_codes.get(language, "en")
                                    translated_audio = text_to_speech(translated_text, lang_code)
                                    if translated_audio:
                                        st.audio(translated_audio)
                    else:
                        st.write(message["content"])
                        original_audio = text_to_speech(message["content"], 'en')
                        if original_audio:
                            st.audio(original_audio)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()