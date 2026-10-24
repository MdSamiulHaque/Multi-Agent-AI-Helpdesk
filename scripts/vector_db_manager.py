import os
from glob import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

class ManualRepository:
    def __init__(self, persist_directory: str, embeddings_model):
        self.persist_directory = persist_directory
        self.embeddings = embeddings_model
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def save_documents(self, chunks):
        self.vector_store.add_documents(chunks)

    def search_documents(self, query: str, k: int = 3):
        return self.vector_store.similarity_search(query, k=k)

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def load_and_split_pdfs(self, pdf_directory: str):
        pdf_files = glob(os.path.join(pdf_directory, "*.pdf"))
        all_chunks = []
        
        for pdf_file in pdf_files:
            loader = PyPDFLoader(pdf_file)
            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)
            all_chunks.extend(chunks)
            
        return all_chunks

class VectorDatabaseManager:
    def __init__(self, pdf_directory: str, db_directory: str):
        self.pdf_directory = pdf_directory
        self.db_directory = db_directory
        self.embeddings = OpenAIEmbeddings()
        self.repository = ManualRepository(self.db_directory, self.embeddings)
        self.processor = DocumentProcessor()

    def initialize_database(self):
        chunks = self.processor.load_and_split_pdfs(self.pdf_directory)
        if chunks:
            self.repository.save_documents(chunks)

if __name__ == "__main__":
    pdf_dir = "manuals"
    db_dir = "chroma_db"
    
    os.makedirs(pdf_dir, exist_ok=True)
    
    db_manager = VectorDatabaseManager(pdf_directory=pdf_dir, db_directory=db_dir)
    db_manager.initialize_database()
    
    test_results = db_manager.repository.search_documents("warranty")
    for result in test_results:
        print(result.page_content)