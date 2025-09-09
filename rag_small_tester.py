import sys
import time
from langchain_huggingface import HuggingFaceEmbeddings
from supabase import create_client, Client

def load_env_file(file_path):
    env_vars = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    return env_vars

def main():
    env_vars = load_env_file('supabase-docker/.env')
    SUPABASE_URL = env_vars.get('SUPABASE_PUBLIC_URL')
    SUPABASE_KEY = env_vars.get('ANON_KEY')
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    embedding_model = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    
    print("🔍 RAG Real-time Tester")
    print("Type your query and press Enter. Press Ctrl+C to exit.")
    print("-" * 50)
    
    try:
        while True:
            query = input("\nQuery: ").strip()
            
            if not query:
                continue
                
            query_embedding = embedding_model.embed_query(query)
            
            # Use RPC function for vector similarity search
            result = supabase.rpc(
                "search_recipes",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": 0.5,
                    "match_count": 5
                }
            ).execute()
            
            if result.data:
                print(f"\n📋 Top {len(result.data)} results:")
                print("-" * 30)
                
                for i, recipe in enumerate(result.data, 1):
                    content = recipe['file_content']
                    display_content = content[:200] + "..." if len(content) > 200 else content
                    similarity = recipe.get('similarity', 0)
                    print(f"{i}. [Similarity: {similarity:.3f}] {display_content}")
                    print()
            else:
                print("❌ No results found")
                
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
