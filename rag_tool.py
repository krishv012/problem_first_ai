# rag_query.py
import os
from dotenv import load_dotenv
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from typing import List, Optional

# Load environment variables
load_dotenv()

# Check for the OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it in a .env file or your environment.")


class RAGTool:
    """
    A class for performing Retrieval-Augmented Generation (RAG) operations
    using FAISS vector store and OpenAI embeddings.
    """
    
    def __init__(self, query: str):
        """
        Initialize the RAG tool with a vector store index path.
        
        Args:
            index_path (str): The path to the directory containing the saved vector store.
        """
        self.index_path = os.getenv("EMBEDDINGS_PATH")
        print(f"-"*100)
        print(f"Index path: {self.index_path}")
        print(f"-"*100)
        self.vector_store = None
        self.embeddings = OpenAIEmbeddings()
        self.query = query
        self.vector_store = self.load_vector_store()
    
    def load_vector_store(self) -> Optional[FAISS]:
        """
        Loads a FAISS vector store from a local directory.
        
        Returns:
            FAISS: The loaded FAISS vector store object, or None if loading fails.
        """
        try:
            if not os.path.exists(self.index_path):
                print(f"Vector store directory '{self.index_path}' not found.")
                print("Please run rag_ingestion.py first to create the index.")
                return None
            
            # Load the index from the specified path.
            self.vector_store = FAISS.load_local(
                self.index_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
            print(f"Successfully loaded FAISS vector store from '{self.index_path}'.")
            return self.vector_store
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return None
    
    def retrieve_chunks(self, query: str = None, k: int = 4) -> List:
        """
        Performs a similarity search on the vector store to retrieve relevant document chunks.
        
        Args:
            query (str): The user's query string.
            k (int): The number of top-k most similar chunks to retrieve.
            
        Returns:
            list: A list of relevant document objects.
        """
        if not self.vector_store:
            print("Vector store not loaded. Please call load_vector_store() first.")
            return []
        
        print(f"\nPerforming similarity search for query: '{self.query}'")
        # Use the vector store to find the 'k' most similar documents.
        # The query is automatically embedded using the same model.
        docs = self.vector_store.similarity_search(self.query, k=k)
        return docs
    
    def search_and_display(self, query: str, k: int = 4) -> None:
        """
        Performs a search and displays the results in a formatted way.
        
        Args:
            query (str): The user's query string.
            k (int): The number of top-k most similar chunks to retrieve.
        """
        relevant_chunks = self.retrieve_chunks(query, k)
        
        if relevant_chunks:
            print("\n--- Retrieved Chunks ---")
            for i, doc in enumerate(relevant_chunks):
                print(f"\nChunk {i+1}:")
                print(doc.page_content)
                print("-" * 20)
        else:
            print("No relevant chunks found.")
    
    def get_vector_store(self) -> Optional[FAISS]:
        """
        Returns the current vector store instance.
        
        Returns:
            FAISS: The current vector store, or None if not loaded.
        """
        return self.vector_store
    
    def is_loaded(self) -> bool:
        """
        Checks if the vector store is loaded.
        
        Returns:
            bool: True if vector store is loaded, False otherwise.
        """
        return self.vector_store is not None


def main():
    """
    Main function to demonstrate the RAG tool usage.
    """
    # Create RAG tool instance
    rag_tool = RAGTool()
    
    # Load the vector store
    if rag_tool.load_vector_store():
        # Example queries
        queries = [
            "What is the main topic of the document?",
            "What does the document say about vector databases?"
        ]
        
        for query in queries:
            rag_tool.search_and_display(query)


if __name__ == "__main__":
    main()
