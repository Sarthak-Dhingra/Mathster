import os
import gradio as gr
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()


# Read the bot role from the file
try:
    with open('bot_role.txt', 'r') as file:
        bot_role = file.read().strip()
    if not bot_role:
        bot_role = "system"  # Default role if file is empty
except FileNotFoundError:
    bot_role = "system"  # Default role if file is not found

# Try to get the API key from the environment variable
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please set it before running the script.")

client = Groq(api_key=api_key)

# Initialize global variable for chat history
chat_history = []

def math_chatbot(user_input, history):
    global chat_history
    
    # Append the system role and behavior
    chat_history.append({
        "role": "system",
        "content": bot_role,
    })

    for bot_messages, user_messages in history:
        chat_history.append({
            "role": "assistant",  
            "content": bot_messages,
        })
        chat_history.append({
            "role": "user",
            "content": user_messages,
        })

    chat_history.append({
        "role": "user",
        "content": user_input,
    })
    
    # Create the chat completion with the updated history
    chat_completion = client.chat.completions.create(
        messages=chat_history,
        model="llama-3.1-8b-instant",
        temperature=0.5
    )
    
    # Extract the bot's reply and return it
    bot_reply = chat_completion.choices[0].message.content
    
    return bot_reply

# add the UI
iface = gr.ChatInterface(
    fn=math_chatbot,
    chatbot=gr.Chatbot(height=650),
    textbox=gr.Textbox(placeholder="Type your message here...", container=False, scale=7),
    title="Mathster - Math Tutor",  # This sets the tab name
    description="""
    <div>
        <span style="font-size: 20px; font-weight: bold;float: right;">#<a href="https://www.linkedin.com/in/sarthak-dhingra/">sarthak-dhingra</a></span>
    </div>
    <p style="color:limegreen;font-weight: bold;font-size: 15px;">I am Mathster, your friendly and enthusiastic math tutor! I'm here to help you navigate the wonderful world of mathematics, making it fun and accessible for you.</p>
    """,
    theme="soft",
    examples=["Can you explain the concept of probability and how it's used in real-life situations?", 
              "How do you calculate the area of a circle?",
              "Can you help me solve this math problem: 2x + 5 = 11?",
              "How is math used in cryptography and encryption?",
              "What is the significance of the number pi in mathematics?"],
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear"
)

if __name__ == "__main__":
    iface.launch(share=True)
