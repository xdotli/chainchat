import random
import string
from openai import OpenAI
from supabase import create_client, Client
import os

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
openai_apikey: str = os.environ.get("OPENAI_API_KEY")
print(url)
supabase: Client = create_client(url, key)

client = OpenAI(
    # api_key=openai_apikey,
    # base_url="https://api.upstage.ai/v1/solar"
)

# # Create the table
# def create_table():
#     supabase.table('courses').create(
#         primary_keys=['id'],
#         columns=[
#             {'name': 'id', 'type': 'int', 'auto_increment': True},
#             {'name': 'rating', 'type': 'float'},
#             {'name': 'course_name', 'type': 'text'},
#             {'name': 'course_description', 'type': 'text'},
#             {'name': 'lecturer', 'type': 'text'},
#             {'name': 'course_description_embeddings', 'type': 'vector(1536)'}
#         ]
#     ).execute()

# Generate fake data using ChatGPT 3.5
def generate_fake_data(num_rows):
    fake_data = []
    for _ in range(num_rows):
        rating = round(random.uniform(1, 5), 1)
        course_name = "Course " + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        lecturer = "Lecturer " + ''.join(random.choices(string.ascii_uppercase, k=3))
        
        prompt = f"Generate a short description for a course named {course_name} taught by {lecturer}."
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "system", "content": "You are a helpful assistant."},
        #               {"role": "user", "content": prompt}],
        #     max_tokens=100,
        #     n=1,
        #     stop=None,
        #     temperature=0.7,
        # )
        completion = client.chat.completions.create(
            # model="solar-1-mini-chat",
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=1000,
            n=1,
            temperature=0.7,
        )
        course_description = completion.choices[0].message.content
        
        fake_data.append(
            {"rating": rating, "course_name": course_name, "course_description": course_description, "lecturer": lecturer}
        )
    return fake_data

# Insert fake data into the table
def insert_fake_data(fake_data):
    print(fake_data)
    supabase.table('courses').insert(fake_data).execute()

# Run the functions
# create_table()
fake_data = generate_fake_data(10)
insert_fake_data(fake_data)