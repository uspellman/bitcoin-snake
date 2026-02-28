import os
from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

# Get your Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Set up Groq client
client = Groq(api_key=groq_api_key)

# Initialize conversation history
messages = [
    {"role": "system", "content": "You are an IT professional with over 30 years of experience."}
]

def get_llm_response(prompt):
    # Append user message
    messages.append({"role": "user", "content": prompt})
    
    # Send the whole conversation
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7
    )
    
    # Extract assistant response
    reply = response.choices[0].message.content
    
    # Append assistant message to history
    messages.append({"role": "assistant", "content": reply})
    
    return reply

# Conversation loop
while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["conversation done", "done", "exit", "quit"]:
        print("Conversation ended.")
        break
    reply = get_llm_response(user_input)
    print(f"\nAI: {reply}")
