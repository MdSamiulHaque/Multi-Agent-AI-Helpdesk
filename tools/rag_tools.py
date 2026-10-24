from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

class ManualRepository:
    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def search_documents(self, query: str, k: int = 3):
        return self.vector_store.similarity_search(query, k=k)

@tool
def retrieve_manual_info(query: str) -> str:
    """Retrieve relevant troubleshooting steps and product manual information based on a query."""
    repository = ManualRepository(persist_directory="chroma_db")
    results = repository.search_documents(query)
    
    if not results:
        return "No relevant information found in the product manuals."
        
    return "\n\n".join([doc.page_content for doc in results])