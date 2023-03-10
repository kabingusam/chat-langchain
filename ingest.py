"""Load html from files, clean up, split, ingest into Weaviate."""
import pickle
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS

def ingest_docs(urls):
    """Get documents from web pages."""
    documents = []
    for url in urls:
        loader = WebBaseLoader(url)
        raw_documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        documents += text_splitter.split_documents(raw_documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Save vectorstore
    with open("vectorstore.pkl", "wb") as f:
        pickle.dump(vectorstore, f)

if __name__ == "__main__":
    urls = [
        "https://weedmaps.com/learn",
        "https://weedmaps.com/strains",
        "https://bsd.biomedcentral.com",
        "https://weedmaps.com/learn/introduction/what-does-it-feel-like-to-be-high"
    ]
    ingest_docs(urls)
