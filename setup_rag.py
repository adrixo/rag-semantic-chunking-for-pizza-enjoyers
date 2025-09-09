#!/usr/bin/env python3
"""
Setup script to create the vector search RPC function in Supabase
"""

import os
from supabase import create_client, Client

def load_env_file(file_path):
    """Load environment variables from .env file"""
    env_vars = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    return env_vars

def main():
    # Load environment variables
    env_vars = load_env_file('supabase-docker/.env')
    SUPABASE_URL = env_vars.get('SUPABASE_PUBLIC_URL')
    SUPABASE_KEY = env_vars.get('ANON_KEY')
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: Missing SUPABASE_PUBLIC_URL or ANON_KEY in .env file")
        return
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Read the SQL setup file
    with open('setup_vector_search.sql', 'r') as f:
        sql_content = f.read()
    
    print("Setting up vector search function...")
    
    try:
        # Execute the SQL to create the RPC function
        result = supabase.rpc('exec_sql', {'sql': sql_content}).execute()
        print("✅ Vector search function created successfully!")
        print("You can now run: python rag_small_tester.py")
    except Exception as e:
        print(f"❌ Error setting up vector search: {e}")
        print("\nYou may need to run the SQL manually in your Supabase dashboard:")
        print("1. Go to your Supabase project dashboard")
        print("2. Navigate to SQL Editor")
        print("3. Run the contents of setup_vector_search.sql")

if __name__ == "__main__":
    main()
