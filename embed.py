import json
import chromadb
from sentence_transformers import SentenceTransformer

def main():
    # 1. 从 JSON 文件加载文本块
    print("Loading chunks from chunks.json...")
    try:
        with open("chunks.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)
    except FileNotFoundError:
        print("Error: chunks.json not found. Please run ingest.py first.")
        return

    # 2. 初始化 ChromaDB 本地持久化客户端
    print("Initializing ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # 创建 Collection（集合）
    collection_name = "cuny_study_abroad"
    
    # 为了防止重复运行导致数据叠加，如果集合已存在我们先删除它
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
        
    collection = client.create_collection(name=collection_name)
    
    # 3. 加载 embedding 模型
    print("Loading sentence-transformers model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # 4. 提取文本并进行向量化
    print(f"Embedding {len(chunks)} chunks... This might take a minute or two.")
    texts = [chunk["text"] for chunk in chunks]
    
    # model.encode 会返回向量数组，我们需要转换成列表格式供 Chroma 接收
    embeddings = model.encode(texts).tolist()
    
    # 5. 准备 ChromaDB 需要的 ID 和元数据 (Metadata)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"url": chunk["url"], "chunk_id": chunk["chunk_id"]} for chunk in chunks]
    
    # 6. 将数据存入 Vector Store
    print("Saving to ChromaDB...")
    collection.add(embeddings=embeddings, documents=texts, metadatas=metadatas, ids=ids)
    
    print("\nSuccess! All chunks embedded and saved to local ChromaDB (./chroma_db).")

if __name__ == "__main__":
    main()