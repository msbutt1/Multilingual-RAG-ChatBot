"""
Main Streamlit application for multilingual chatbot
"""
import streamlit as st
import os
from dotenv import load_dotenv
from translation_service import TranslationService
from vectorstore_service import VectorStoreService
from vertexai_service import VertexAIService

load_dotenv()

st.set_page_config(
    page_title="AI Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
    /* Dark theme */
    .stApp {
        background: #343541;
    }
    
    /* Hide Streamlit UI */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stSidebar"] {visibility: hidden;}
    
    /* Top bar */
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 52px;
        background: #202123;
        border-bottom: 1px solid #4d4d4f;
        display: flex;
        align-items: center;
        padding: 0 24px;
        z-index: 1000;
    }
    
    .top-bar-title {
        color: #ececf1;
        font-size: 16px;
        font-weight: 600;
        letter-spacing: -0.01em;
    }
    
    /* Main content */
    .main-content {
        margin-top: 52px;
        margin-bottom: 180px;
        padding: 24px 16px;
    }
    
    /* Welcome section */
    .welcome-section {
        max-width: 768px;
        margin: 80px auto 0;
        text-align: center;
    }
    
    .welcome-title {
        font-size: 32px;
        font-weight: 600;
        color: #ececf1;
        margin-bottom: 48px;
        letter-spacing: -0.02em;
    }
    
    /* Chat messages */
    .chat-messages {
        max-width: 768px;
        margin: 0 auto;
        padding: 24px 0;
    }
    
    .message {
        margin-bottom: 24px;
        padding: 20px;
        border-radius: 12px;
        line-height: 1.6;
        font-size: 15px;
    }
    
    .user-message {
        background: #444654;
        color: #ececf1;
    }
    
    .assistant-message {
        background: #343541;
        color: #d1d5db;
        border: 1px solid #4d4d4f;
    }
    
    .message-label {
        font-weight: 600;
        margin-bottom: 8px;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.7;
    }
    
    /* Input section */
    .input-section {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(180deg, transparent, #343541 15%);
        padding: 32px 16px 24px;
        z-index: 1000;
    }
    
    .input-wrapper {
        max-width: 768px;
        margin: 0 auto;
    }
    
    /* Form styling */
    .stForm {
        border: none !important;
        background: transparent !important;
    }
    
    /* Input field */
    .stTextInput > div > div > input {
        background: #40414f !important;
        border: 1px solid #565869 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-size: 15px !important;
        color: #ececf1 !important;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #8e8ea0 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #10a37f !important;
        box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.15) !important;
    }
    
    /* Submit button - hide it but keep it functional */
    .stForm button[type="submit"] {
        display: none;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #10a37f !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #343541;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #565869;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #6e6e80;
    }
    
    /* Info footer */
    .info-footer {
        text-align: center;
        color: #8e8ea0;
        font-size: 13px;
        margin-top: 16px;
        padding-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize services
@st.cache_resource(show_spinner=False)
def init_services():
    """Initialize all services."""
    try:
        project_id = os.getenv("GCP_PROJECT_ID")
        region = os.getenv("GCP_REGION", "us-central1")
        
        if not project_id:
            return None, None, None, "GCP_PROJECT_ID not found. Please set it in your .env file."
        
        print("Initializing translation service...")
        translation_service = TranslationService()
        
        use_openai = bool(os.getenv("OPENAI_API_KEY")) and os.getenv("USE_OPENAI_EMBEDDINGS", "false").lower() == "true"
        print("Initializing vector store service...")
        vector_service = VectorStoreService(use_openai=use_openai)
        
        print("Initializing Vertex AI service...")
        vertexai_service = VertexAIService(project_id=project_id, location=region)
        
        print("Loading vector store...")
        vector_service.load_vectorstore()
        
        print("All services initialized successfully!")
        return translation_service, vector_service, vertexai_service, None
    except Exception as e:
        print(f"Error initializing services: {e}")
        return None, None, None, str(e)


def process_query(user_input: str, translation_service, vector_service, vertexai_service):
    """Process user query and generate AI-powered answer."""
    try:
        detected_lang, translated = translation_service.translate_with_detection(user_input)
        relevant_faqs = vector_service.get_relevant_context(translated, k=5)
        
        if relevant_faqs:
            context_parts = []
            for i, faq in enumerate(relevant_faqs, 1):
                context_parts.append(f"Q{i}: {faq['question']}\nA{i}: {faq['answer']}")
            context_text = "\n\n".join(context_parts)
        else:
            context_text = "No relevant information found in the knowledge base."
        
        answer_en = vertexai_service.generate_answer(translated, context_text)
        
        if answer_en is None:
            if relevant_faqs:
                answer_en = relevant_faqs[0]['answer']
            else:
                answer_en = "I couldn't find relevant information to answer your question. Please try rephrasing or ask about something else."
        
        final_answer = translation_service.translate_from_english(answer_en, detected_lang)
        return final_answer, None
    except Exception as e:
        error_msg = str(e)
        print(f"Error in process_query: {error_msg}")
        return None, f"Error processing query: {error_msg}"


def main():
    """Main application entry point."""
    
    st.markdown("""
    <div class="top-bar">
        <div class="top-bar-title">AI Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Initializing services... This may take a minute on first run."):
        translation_service, vector_service, vertexai_service, error = init_services()
    
    if error:
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        st.error(f"Configuration Error: {error}")
        st.info("Please check your .env file and ensure all required credentials are set.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-section">
            <div class="welcome-title">What's on the agenda today?</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.messages:
        st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
        
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message user-message">
                    <div class="message-label">You</div>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message assistant-message">
                    <div class="message-label">Assistant</div>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
    
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Message",
            placeholder="Ask anything in any language...",
            key="user_input",
            label_visibility="collapsed"
        )
        
        submit_button = st.form_submit_button("Send", use_container_width=False)
        
        if submit_button and user_input:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            with st.spinner("Processing..."):
                answer, error = process_query(user_input, translation_service, vector_service, vertexai_service)
            
            if error:
                answer = f"I encountered an error: {error}"
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })
            
            st.rerun()
    
    st.markdown("""
    <div class="info-footer">
        Supports 100+ languages • Powered by Google Vertex AI
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
