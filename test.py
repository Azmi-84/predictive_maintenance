from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

client = Groq(api_key=groq_api_key)

conversation_history = [
    {"role": "system", "content": "You are a helpful assistant who answers user queries."},
]

print("Chatbot: Hi! How can I assist you today?")
while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye!")
        break

    conversation_history.append({"role": "user", "content": user_input})

    try:
        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=150,
            top_p=0.9,
        )

        assistant_response = chat_completion.choices[0].message.content
        print(f"Chatbot: {assistant_response}")

        conversation_history.append({"role": "assistant", "content": assistant_response})

    except Exception as e:
        print(f"An error occurred: {e}")
