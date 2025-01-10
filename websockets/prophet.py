from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
key = os.environ.get("GROQ_API_KEY")

client = Groq(
    api_key=key
)

def llmresponse(query: str):
    try:
        chat = client.chat.completions.create(
            messages= [
                {
                    "role": "user",
                    "content": query
                }
            ],
            model= "llama-3.3-70b-versatile", 
            stream = True
        )
        for chunk in chat:
            print(chunk.choices[0].delta.content)
            yield chunk.choices[0].delta.content
    except:
        print("error with setting up the llm")
        
llmresponse("define growth")