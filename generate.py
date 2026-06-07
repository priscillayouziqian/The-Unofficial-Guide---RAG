import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

# 1. 加载环境变量 (读取 .env 文件里的 GROQ_API_KEY)
load_dotenv()

# 2. 初始化客户端和模型
try:
    groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    print("Error initializing Groq. Did you set GROQ_API_KEY in your .env file?")
    exit(1)

print("Loading database and models...")
db_client = chromadb.PersistentClient(path="./chroma_db")
collection = db_client.get_collection(name="cuny_study_abroad")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_context(query, top_k=5):
    """把用户的问题转成向量，并从 ChromaDB 检索最相关的 5 个文本块"""
    query_embedding = embedding_model.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    # 提取查找到的文本和元数据(比如URL)
    chunks = results['documents'][0]
    sources = results['metadatas'][0]
    return chunks, sources

def generate_answer(query, context_chunks, sources):
    """将检索到的上下文和用户问题组合，发送给 Groq (LLaMA 3) 生成答案"""
    # 拼接上下文文本
    context_text = ""
    for i, (chunk, source) in enumerate(zip(context_chunks, sources)):
        context_text += f"\n--- Source {i+1}: {source['url']} ---\n{chunk}\n"
        
    # 组装 Prompt，强调“基于事实回答 (Grounded Generation)”
    prompt = f"""You are a helpful advisor for CUNY students looking to study abroad.
    Answer the question using only the information in the provided documents. 
    If the documents provide limited information, state what is available and explicitly advise the user on where they can manually look for more information (e.g., advising them to contact their school's study abroad representative) based on hints in the context. If the documents don't contain any relevant information at all, say 'I don't have enough information on that.'

    Context:
    {context_text}

    User Question: {query}
    """
    
    response = groq_client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.2, # 较低的温度可以让回答更准确、不乱编
        max_tokens=1024,
    )
    
    return response.choices[0].message.content

def ask(query):
    """对外暴露的统一问答接口，返回答案与来源列表"""
    chunks, sources = retrieve_context(query)
    answer = generate_answer(query, chunks, sources)
    unique_sources = list(set([s['url'] for s in sources]))
    return {"answer": answer, "sources": unique_sources}

def main():
    print("\n=======================================================")
    print("🎓 Welcome to the CUNY Study Abroad QA System!")
    print("Type your question below. Type 'exit' to quit.")
    print("=======================================================\n")
    
    while True:
        query = input("\n🧑‍🎓 Your Question: ")
        if query.lower() in ['exit', 'quit']:
            break
        if not query.strip():
            continue
            
        print("\n🔍 Searching knowledge base...")
        
        print("🤖 Generating answer via Groq LLaMA 3...\n")
        result = ask(query)
        
        print("====================== ANSWER ======================")
        print(result["answer"])
        print("\n📚 Retrieved Sources:")
        for s in result["sources"]:
            print(f"- {s}")
        print("====================================================")

if __name__ == "__main__":
    main()