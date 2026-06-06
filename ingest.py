import requests
from bs4 import BeautifulSoup
import json

# 10 Sources from planning.md
URLS = [
    "https://www.reddit.com/r/CUNY/comments/1j7crv4/anyone_here_studied_abroad_at_bmcc/",
    "https://www.studyabroad101.com/providers/cuny-college-of-staten-island",
    "https://www.reddit.com/r/CUNY/comments/1qpbwan/talk_about_your_experience_studying_abroad/",
    "https://www.bmcc.cuny.edu/academics/success-programs/study-abroad/financial-aid-and-scholarships/",
    "https://www1.cuny.edu/sites/global/students/programs/programs-search/",
    "https://www.hunter.cuny.edu/students/opportunities/study-abroad/eligibility-requirements/",
    "https://www.reddit.com/r/CUNY/comments/17bxq0j/cuny_study_abroad/",
    "https://www.reddit.com/r/CUNY/comments/11lhs5r/study_abroad/",
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
            if "reddit.com" in url:
                # Bypass Reddit HTML blocks by fetching JSON directly
                json_url = url.rstrip('/') + '.json'
                # Reddit API requires a distinct User-Agent
                reddit_headers = {"User-Agent": "python:rag-project:v1.0 (by /u/student)"}
                
                response = requests.get(json_url, headers=reddit_headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                post_data = data[0]['data']['children'][0]['data']
                title = post_data.get('title', '')
                selftext = post_data.get('selftext', '')
                
                comments = []
                if len(data) > 1:
                    for child in data[1]['data'].get('children', []):
                        if 'body' in child.get('data', {}):
                            comments.append(child['data']['body'])
                            
                text = f"{title} {selftext} " + " ".join(comments)
            else:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract text and replace newlines/tabs with spaces
                text = soup.get_text(separator=' ', strip=True)
            
            documents.append({"url": url, "text": text})
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            
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
    docs = load_documents(URLS)
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