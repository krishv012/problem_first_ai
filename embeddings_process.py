# rag_ingestion.py
import os
import argparse
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from typing import List
from langchain.docstore.document import Document

# Load environment variables from a .env file
# This is a best practice for securely managing API keys.
load_dotenv()

# Check if the OpenAI API key is set
# This script requires an OpenAI API key to generate embeddings.
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it in a .env file or your environment.")

def load_documents_from_directory(directory_path: str, file_pattern: str = "**/*.pdf") -> List[Document]:
    """
    Loads all documents from a given directory based on the specified pattern.
    
    Args:
        directory_path (str): The path to the directory containing the documents.
        file_pattern (str): The glob pattern to match files (e.g., "**/*.pdf", "**/*.txt").
    
    Returns:
        List[Document]: A list of all LangChain Document objects from the directory.
    """
    try:
        # Use DirectoryLoader to load multiple files.
        # The 'glob' parameter specifies a pattern to match files.
        # The 'loader_cls' specifies the loader to use for each file.
        loader = DirectoryLoader(
            directory_path,
            glob=file_pattern,
            loader_cls=PyPDFLoader
        )
        documents = loader.load()
        print(f"Successfully loaded {len(documents)} document(s) from '{directory_path}' using pattern '{file_pattern}'.")
        return documents
    except Exception as e:
        print(f"Error loading documents from directory: {e}")
        return []

def split_documents(documents: List[Document], chunk_size: int = 200, chunk_overlap: int = 40) -> List[Document]:
    """
    Splits a list of documents into smaller, manageable chunks.
    This is important to fit within the context window of the language model
    and to improve the accuracy of retrieval.
    
    Args:
        documents (List[Document]): A list of LangChain Document objects.
        chunk_size (int): The size of each chunk in characters.
        chunk_overlap (int): The number of characters to overlap between chunks.
    
    Returns:
        List[Document]: A list of smaller, chunked Document objects.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")
    return chunks

def create_embeddings_and_vector_store(chunks: List[Document], save_path: str):
    """
    Generates embeddings for document chunks and creates a FAISS vector store.
    The vector store is then saved to disk for later use.
    
    Args:
        chunks (List[Document]): A list of chunked Document objects.
        save_path (str): The directory to save the vector store to.
    """
    # Initialize the embedding model. You can use other models like Hugging Face embeddings.
    embeddings = OpenAIEmbeddings()
    print("Generating embeddings and building the FAISS vector store...")
    
    # Create the FAISS vector store from the document chunks and embeddings.
    # FAISS is a great option for local, file-based vector stores.
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Save the vector store to a local directory.
    vector_store.save_local(save_path)
    print(f"FAISS vector store saved to '{save_path}'.")

def main(directory_path: str, faiss_index_path: str, chunk_size: int, chunk_overlap: int, file_pattern: str):
    """
    Main function to run the document ingestion pipeline.
    
    Args:
        directory_path (str): Path to the directory containing documents
        faiss_index_path (str): Path where to save the FAISS vector store
        chunk_size (int): Size of each document chunk in characters
        chunk_overlap (int): Number of characters to overlap between chunks
        file_pattern (str): File pattern to match (e.g., "**/*.pdf")
    """
    # Check if the directory exists.
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' not found. "
              "Please create the directory and add your documents.")
        return

    # 1. Load documents
    documents = load_documents_from_directory(directory_path, file_pattern)
    if not documents:
        return

    # 2. Split documents into chunks
    chunks = split_documents(documents, chunk_size, chunk_overlap)
    
    # 3. Create and save the vector store
    create_embeddings_and_vector_store(chunks, faiss_index_path)
    print("Document ingestion complete!")

def parse_arguments():
    """
    Parse command line arguments for the document ingestion pipeline.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Process documents and create FAISS vector store for RAG",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--directory", "-d",
        type=str,
        default="./docs",
        help="Path to the directory containing documents to process"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="faiss_index",
        help="Path where to save the FAISS vector store"
    )
    
    parser.add_argument(
        "--chunk-size", "-cs",
        type=int,
        default=200,
        help="Size of each document chunk in characters"
    )
    
    parser.add_argument(
        "--chunk-overlap", "-co",
        type=int,
        default=40,
        help="Number of characters to overlap between chunks"
    )
    
    parser.add_argument(
        "--pattern", "-p",
        type=str,
        default="**/*.pdf",
        help="File pattern to match (e.g., '**/*.pdf', '**/*.txt')"
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    main(
        directory_path=args.directory,
        faiss_index_path=args.output,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        file_pattern=args.pattern
    )
