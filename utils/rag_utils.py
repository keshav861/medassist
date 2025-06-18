import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from utils.hf_utils import get_hf_embeddings

def create_vector_store(documents):
    """
    Create a vector store from documents for retrieval.
    
    Args:
        documents: List of documents to be indexed
        
    Returns:
        FAISS vector store with indexed documents
    """
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # Create embeddings using HuggingFace model
    embeddings = get_hf_embeddings()
    
    # Create vector store
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Save vector store locally if needed
    vector_store_path = os.path.join("data", "vector_store")
    os.makedirs(vector_store_path, exist_ok=True)
    vector_store.save_local(vector_store_path)
    
    return vector_store

def load_vector_store():
    """
    Load a previously saved vector store.
    
    Returns:
        FAISS vector store loaded from disk
    """
    vector_store_path = os.path.join("data", "vector_store")
    
    if os.path.exists(vector_store_path):
        embeddings = get_hf_embeddings()
        vector_store = FAISS.load_local(vector_store_path, embeddings)
        return vector_store
    else:
        raise FileNotFoundError(f"Vector store not found at {vector_store_path}")

def get_relevant_documents(query, vector_store, k=3):
    """
    Retrieve relevant documents for a query.
    
    Args:
        query: User query string
        vector_store: Vector store to search in
        k: Number of documents to retrieve
        
    Returns:
        List of relevant documents
    """
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    relevant_docs = retriever.get_relevant_documents(query)
    return relevant_docs