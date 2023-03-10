#!/bin/bash
# Bash script to ingest data
# This involves scraping the data from the web and then cleaning up and putting in Weaviate.
# Error if any command fails
set -e

# List of URLs to scrape
urls=(
  "https://weedmaps.com/learn"
  "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5312634/"
  "https://jcannabisresearch.biomedcentral.com/"
)

# Download HTML files for each URL
for url in "${urls[@]}"
do
  wget -r -A.html "$url"
done

# Ingest HTML files into Weaviate
python3 ingest.py
