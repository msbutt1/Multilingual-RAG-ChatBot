"""
Setup script to initialize the vector store
Run this once before starting the app for the first time
"""
import os
from dotenv import load_dotenv
from vectorstore_service import VectorStoreService

def main():
    print("=" * 60)
    print("Initializing Multilingual Chatbot")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    print("\nCreating FAISS vector store from FAQs...")
    
    # Check if OpenAI key is available
    use_openai = bool(os.getenv("OPENAI_API_KEY"))
    
    if use_openai:
        print("OpenAI API key found - attempting to use OpenAI embeddings")
        print("Note: This requires OpenAI credits")
    else:
        print("Using free HuggingFace embeddings")
    
    try:
        # Initialize and create vector store
        vector_service = VectorStoreService(use_openai=use_openai)
        vector_service.create_vectorstore()
    except Exception as e:
        if "insufficient_quota" in str(e) or "RateLimitError" in str(e):
            print("\nOpenAI quota exceeded! Switching to free HuggingFace embeddings...")
            print("This will download the model on first run (~90MB)")
            vector_service = VectorStoreService(use_openai=False)
            vector_service.create_vectorstore()
        else:
            raise
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nYou can now run the app with:")
    print("  streamlit run app.py")

if __name__ == "__main__":
    main()
