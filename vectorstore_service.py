"""
Vector store service using FAISS for FAQ retrieval
Supports both OpenAI and HuggingFace embeddings
"""
import json
import os
from typing import List, Dict
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document


class VectorStoreService:
    """Handles FAQ storage and retrieval using FAISS vector store"""
    
    def __init__(self, faqs_file: str = "faqs.json", index_path: str = "faiss_index", use_openai: bool = False):
        """
        Initialize the vector store service
        
        Args:
            faqs_file: Path to JSON file containing FAQs
            index_path: Path to save/load FAISS index
            use_openai: If True, use OpenAI embeddings (requires credits).
                       If False, use free HuggingFace embeddings (default)
        """
        self.faqs_file = faqs_file
        self.index_path = index_path
        self.use_openai = use_openai
        
        if use_openai:
            print("Using OpenAI embeddings...")
            from langchain_openai import OpenAIEmbeddings
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        else:
            print("Using HuggingFace embeddings...")
            from langchain_community.embeddings import HuggingFaceEmbeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        
        self.vectorstore = None
        self.faqs = []
        
    def load_faqs(self) -> List[Dict]:
        """Load FAQs from JSON file"""
        with open(self.faqs_file, 'r', encoding='utf-8') as f:
            self.faqs = json.load(f)
        return self.faqs
    
    def create_vectorstore(self):
        """Create and save FAISS vector store from FAQs"""
        self.load_faqs()
        
        # Create documents from FAQs
        documents = []
        for faq in self.faqs:
            doc = Document(
                page_content=faq['question'],
                metadata={'answer': faq['answer']}
            )
            documents.append(doc)
        
        print(f"Creating embeddings for {len(documents)} FAQs...")
        
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        self.vectorstore.save_local(self.index_path)
        print(f"Vector store created and saved to {self.index_path}")
        
    def load_vectorstore(self):
        """Load existing FAISS vector store"""
        if os.path.exists(self.index_path):
            self.vectorstore = FAISS.load_local(
                self.index_path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"Vector store loaded from {self.index_path}")
        else:
            print(f"No vector store found at {self.index_path}. Creating new one...")
            self.create_vectorstore()
    
    def search(self, query: str, k: int = 1) -> List[Dict]:
        """
        Search for most relevant FAQs
        
        Args:
            query: User query (should be in English)
            k: Number of results to return
            
        Returns:
            List of matching FAQ dictionaries
        """
        if self.vectorstore is None:
            self.load_vectorstore()
        
        results = self.vectorstore.similarity_search(query, k=k)
        matches = []
        for doc in results:
            matches.append({
                'question': doc.page_content,
                'answer': doc.metadata['answer']
            })
        
        return matches
    
    def get_best_match(self, query: str) -> Dict:
        """
        Get the single best matching FAQ.
        
        Args:
            query: User query (should be in English)
            
        Returns:
            Dictionary with 'question' and 'answer' keys
        """
        results = self.search(query, k=1)
        return results[0] if results else {'question': '', 'answer': 'I could not find a relevant answer.'}
    
    def get_relevant_context(self, query: str, k: int = 5) -> List[Dict]:
        """
        Get multiple relevant FAQs for better context
        
        Args:
            query: User query (should be in English)
            k: Number of relevant FAQs to retrieve (default: 5)
            
        Returns:
            List of matching FAQ dictionaries
        """
        results = self.search(query, k=k)
        return results if results else []
