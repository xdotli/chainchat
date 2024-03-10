import os
from supabase import create_client, Client
from openai import OpenAI

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
openai_apikey: str = os.environ.get("OPENAI_API_KEY")
supabase: Client = create_client(url, key)

client = OpenAI(
    # api_key=openai_apikey,
    # base_url="https://api.upstage.ai/v1/solar"
)

# Fetch course descriptions from the table
def fetch_course_descriptions():
    data = supabase.table('courses').select('id, course_description').execute()
    return data.data

# Generate embeddings for course descriptions using OpenAI
def generate_embeddings(course_descriptions):
    embeddings = []
    for course in course_descriptions:
        course_id = course["id"]
        description = course["course_description"]
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=description
        )
        embedding = response.data[0].embedding
        embeddings.append({'id': course_id, 'course_description_embeddings': embedding})
    return embeddings

# Update the table with the generated embeddings
def update_embeddings(embeddings):
    supabase.table('courses').upsert(embeddings).execute()

# Run the functions
course_descriptions = fetch_course_descriptions()
embeddings = generate_embeddings(course_descriptions)
update_embeddings(embeddings)