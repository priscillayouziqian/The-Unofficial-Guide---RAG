import json
import random

def main():
    try:
        with open("chunks.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)
    except FileNotFoundError:
        print("Error: chunks.json not found. Please run ingest.py first.")
        return
        
    if not chunks:
        print("No chunks found in chunks.json.")
        return
        
    print(f"Total chunks loaded: {len(chunks)}\n")
    print("=== 5 RANDOM CHUNKS FOR INSPECTION ===\n")
    
    # 随机抽取 5 个，如果总数不够 5 个就抽取全部
    sample_size = min(5, len(chunks))
    random_chunks = random.sample(chunks, sample_size)
    
    for i, chunk in enumerate(random_chunks, 1):
        print(f"--- Chunk {i} | ID: {chunk['chunk_id']} ---")
        print(f"Text:\n{chunk['text']}\n")

if __name__ == "__main__":
    main()