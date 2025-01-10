from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(
    api_key= os.environ.get("GROQ_API_KEY")
)

response = client.chat.completions.create(
    messages= [
        {
            "role": "user",
            "content": "define growth"
        }
    ],
    model="llama-3.3-70b-versatile"
)

data = response.choices[0].message.content
print(data)