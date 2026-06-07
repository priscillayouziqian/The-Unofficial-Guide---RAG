import requests
from bs4 import BeautifulSoup
import json
import time
import urllib.parse
import os

# 只保留能稳定抓取的 CUNY 官方网站
URLS = [
    "https://www.studyabroad101.com/providers/cuny-college-of-staten-island",
    "https://www.bmcc.cuny.edu/academics/success-programs/study-abroad/financial-aid-and-scholarships/",
    "https://www1.cuny.edu/sites/global/students/programs/programs-search/",
    "https://www.hunter.cuny.edu/students/opportunities/study-abroad/eligibility-requirements/",
    "https://www.jjay.cuny.edu/academics/undergraduate-programs/international-studies-programs/study-abroad",
    "https://www.bmcc.cuny.edu/academics/success-programs/study-abroad/student-testimonials/"
]

def load_documents(urls):
    """Fetches HTML from URLs and extracts clean text using BeautifulSoup."""
    documents = []
    # Using a User-Agent to prevent getting blocked by Reddit/CUNY servers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    for url in urls:
        try:
            print(f"Fetching: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text and replace newlines/tabs with spaces
            text = soup.get_text(separator=' ', strip=True)
            
            documents.append({"url": url, "text": text})
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            
        # 每次抓取后暂停 1 秒
        time.sleep(1)
            
    return documents

def load_local_txt_documents(folder_path="documents"):
    """从本地文件夹读取所有的 .txt 文件"""
    documents = []
    if not os.path.exists(folder_path):
        print(f"Local folder '{folder_path}' not found. Skipping local documents.")
        return documents
        
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({"url": f"Local File: {filename}", "text": text})
            print(f"Loaded local file: {filename}")
            
    return documents

def chunk_documents(documents, chunk_size=500, overlap=50):
    """Splits document text into chunks of specified size and overlap."""
    chunks = []
    
    for doc in documents:
        text = doc["text"]
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            
            chunks.append({
                "url": doc["url"],
                "chunk_id": chunk_index,
                "text": chunk_text
            })
            
            start += (chunk_size - overlap)
            chunk_index += 1
            
    return chunks

if __name__ == "__main__":
    print("Starting document ingestion...")
    # 组合网络抓取的文档和本地的 txt 文档
    web_docs = load_documents(URLS)
    local_docs = load_local_txt_documents("documents")
    docs = web_docs + local_docs
    print(f"\nSuccessfully loaded {len(docs)} documents.")
    
    chunks = chunk_documents(docs, chunk_size=500, overlap=50)
    print(f"Generated {len(chunks)} total chunks.")
    
    if chunks:
        print("\n--- Sample Chunk ---")
        print(f"URL: {chunks[0]['url']}")
        print(f"Text: {chunks[0]['text']}")
        
        # 保存为 JSON 文件供检查和下一步使用
        with open("chunks.json", "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=4)
        print("\nAll chunks successfully saved to chunks.json")