from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 

DATA_PATH = './data'
DB_FAISS_PATH = 'vectorstore/db_faiss'

def create_vector_db():
    # Load PDFs from the data directory
    loader = DirectoryLoader(DATA_PATH, glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()

    # Split documents into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # Initialize PubMedBERT embeddings (fixed indentation)
    embeddings = HuggingFaceEmbeddings(
        model_name="pritamdeka/S-PubMedBert-MS-MARCO",  # Sentence-transformers compatible model
        model_kwargs={'device': 'cpu'}  # Use 'cuda' if GPU is available
    )

    # Create FAISS vector store
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)
    print(f"Vector database saved at {DB_FAISS_PATH}")

if __name__ == "__main__":
    create_vector_db()
