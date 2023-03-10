"""Load html from files, clean up, split, ingest into Weaviate."""
import sys
import os
import pickle
from langchain.document_loaders import FileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS

def ingest_docs(html_files):
    """Get documents from HTML files."""
    documents = []
    for html_file in html_files:
        loader = FileLoader(html_file)
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
    # Get list of HTML file paths from command-line arguments
    html_files = sys.argv[1:]

    # Ingest HTML files into Weaviate
    ingest_docs(html_files)




#!/bin/bash
# Bash script to ingest data
# This involves scraping the data from the web and then cleaning up and putting in Weaviate.
# Error if any command fails
set -e

# List of URLs to scrape
urls=(
    "https://weedmaps.com/learn",
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5312634/",
        "https://www.leafly.com/news/cannabis-101",
)

# Download HTML files for each URL
for url in "${urls[@]}"
do
  echo "Downloading $url"
  wget --user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299' \
       --wait=5 \
       --random-wait \
       --recursive \
       --level=1 \
       --no-parent \
       --accept-regex '.*\.\(html\|htm\)' \
       "$url"
done

# Ingest HTML files into Weaviate
python3 ingest.py
