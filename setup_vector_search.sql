-- Enable pgvector extension if not already enabled
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a function for semantic similarity search
CREATE OR REPLACE FUNCTION search_recipes(
    query_embedding vector(384),
    match_threshold float DEFAULT 0.1,
    match_count int DEFAULT 5
)
RETURNS TABLE (
    id uuid,
    file_name text,
    file_path text,
    file_content text,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        recipes.id,
        recipes.file_name,
        recipes.file_path,
        recipes.file_content,
        1 - (recipes.embedding <=> query_embedding) as similarity
    FROM recipes
    WHERE 1 - (recipes.embedding <=> query_embedding) > match_threshold
    ORDER BY recipes.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Grant execute permission to anon and authenticated users
GRANT EXECUTE ON FUNCTION search_recipes(vector(384), float, int) TO anon, authenticated;
