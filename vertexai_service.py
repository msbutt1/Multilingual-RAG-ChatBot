"""
Vertex AI service for answer generation using Gemini
"""
import os
from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class VertexAIService:
    """Handles answer generation using Google Vertex AI (Gemini)"""
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        """
        Initialize Vertex AI service
        
        Args:
            project_id: GCP project ID
            location: GCP region (default: us-central1)
        """
        self.project_id = project_id
        self.location = location
        
        self.llm = ChatVertexAI(
            model_name="gemini-2.5-flash",
            temperature=0.4,
            max_output_tokens=2048,
            project=project_id,
            location=location
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant with access to a knowledge base.

You have access to the following relevant information from the knowledge base:

{context}

Based on this information, answer the user's question directly and accurately. 
- If the information directly answers the question, provide a clear, helpful answer
- If the information is related but doesn't fully answer the question, use it to provide the best answer you can
- If the information doesn't relate to the question, say so politely
- Be conversational, natural, and helpful
- Don't just repeat the FAQ answers - actually answer what the user is asking
- Synthesize information from multiple sources if relevant
- Keep answers concise but complete"""),
            ("user", "{question}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def generate_answer(self, question: str, context: str) -> str:
        """
        Generate answer using Vertex AI with retrieved context
        
        Args:
            question: User's question (in English)
            context: String containing formatted context from multiple FAQs
            
        Returns:
            Generated answer, or None if error occurred (for fallback handling)
        """
        try:
            if not question or not question.strip():
                return None
            
            if not context or context.strip() == "No relevant information found in the knowledge base.":
                return None
            
            response = self.chain.invoke({
                "context": context,
                "question": question
            })
            result = response.strip()
            
            if not result or "error" in result.lower() and "encountered" in result.lower():
                return None
            
            return result
        except Exception as e:
            error_msg = str(e)
            print(f"Error generating answer: {error_msg}")
            print(f"Question: {question[:100]}")
            print(f"Context length: {len(context) if context else 0}")
            return None
