"""
Test script to verify all services are working correctly
"""
import os
from dotenv import load_dotenv
from translation_service import TranslationService
from vectorstore_service import VectorStoreService
from vertexai_service import VertexAIService

def test_translation():
    """Test translation service."""
    print("\nTesting Translation Service...")
    print("-" * 50)
    
    try:
        service = TranslationService()
        
        text_es = "¿Cómo restablezco mi contraseña?"
        lang = service.detect_language(text_es)
        print(f"Language detection: '{text_es}' -> {lang}")
        
        translated = service.translate_to_english(text_es)
        print(f"Translation to English: '{translated}'")
        
        back = service.translate_from_english("How do I reset my password?", "es")
        print(f"Translation to Spanish: '{back}'")
        
        return True
    except Exception as e:
        print(f"Translation service failed: {e}")
        return False

def test_vectorstore():
    """Test vector store service."""
    print("\nTesting Vector Store Service...")
    print("-" * 50)
    
    try:
        service = VectorStoreService(use_openai=False)
        service.load_vectorstore()
        
        query = "How do I reset my password?"
        result = service.get_best_match(query)
        print(f"Query: '{query}'")
        print(f"  Matched: '{result['question']}'")
        print(f"  Answer: '{result['answer'][:100]}...'")
        
        return True
    except Exception as e:
        print(f"Vector store service failed: {e}")
        return False

def test_vertexai():
    """Test Vertex AI service."""
    print("\nTesting Vertex AI Service...")
    print("-" * 50)
    
    project_id = os.getenv("GCP_PROJECT_ID")
    
    if not project_id:
        print("GCP_PROJECT_ID not set, skipping Vertex AI test")
        return None
    
    try:
        service = VertexAIService(project_id=project_id)
        
        context = "Q1: How do I reset my password?\nA1: Click on 'Forgot Password' on the login page."
        question = "I forgot my password, what should I do?"
        
        answer = service.generate_answer(question, context)
        print(f"Question: '{question}'")
        print(f"  Answer: '{answer}'")
        
        return True
    except Exception as e:
        print(f"Vertex AI service failed: {e}")
        print("  Make sure Vertex AI API is enabled and credentials are set")
        return False

def main():
    """Run all service tests."""
    print("Testing All Services")
    print("=" * 50)
    
    load_dotenv()
    
    print("\nChecking Environment Variables...")
    print("-" * 50)
    
    checks = {
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        "GCP_PROJECT_ID": os.getenv("GCP_PROJECT_ID"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")
    }
    
    for key, value in checks.items():
        if value:
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"{key}: {display_value}")
        else:
            print(f"{key}: Not set")
    
    results = []
    results.append(("Translation", test_translation()))
    results.append(("Vector Store", test_vectorstore()))
    results.append(("Vertex AI", test_vertexai()))
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    for name, result in results:
        if result is True:
            print(f"{name}: PASSED")
        elif result is False:
            print(f"{name}: FAILED")
        else:
            print(f"{name}: SKIPPED")
    
    all_passed = all(r in [True, None] for _, r in results)
    any_failed = any(r is False for _, r in results)
    
    print("\n" + "=" * 50)
    if all_passed and not any_failed:
        print("All tests passed!")
    elif any_failed:
        print("Some tests failed. Please check your configuration.")
    else:
        print("Tests completed with warnings.")

if __name__ == "__main__":
    main()

