import chromadb
from sentence_transformers import SentenceTransformer

def main():
    print("Loading database and embedding model...")
    # 1. 连接本地 ChromaDB 和 Embedding 模型
    db_client = chromadb.PersistentClient(path="./chroma_db")
    collection = db_client.get_collection(name="cuny_study_abroad")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    print("\n=======================================================")
    print("🔍 RAG Retrieval Tester (No LLM)")
    print("Type your question to see the raw chunks retrieved from ChromaDB.")
    print("Type 'exit' to quit.")
    print("=======================================================\n")
    
    while True:
        query = input("\n🧑‍🎓 Test Query: ")
        if query.lower() in ['exit', 'quit']:
            break
        if not query.strip():
            continue
            
        # 2. 将问题向量化并检索
        query_embedding = embedding_model.encode(query).tolist()
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )
        
        # 3. 打印检索结果和距离分数
        print(f"\n✅ Top 5 Results for: '{query}'\n")
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            source = results['metadatas'][0][i]['url']
            distance = results['distances'][0][i]
            
            print(f"--- Rank {i+1} | Distance: {distance:.4f} | Source: {source} ---")
            print(f"{doc}\n")

if __name__ == "__main__":
    main()