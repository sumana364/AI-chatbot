import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from database import ChatDatabase

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize database
db = ChatDatabase()

# Page configuration
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .user-message {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        color: #000000;
    }
    .assistant-message {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_conversation_id' not in st.session_state:
    st.session_state.current_conversation_id = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'model' not in st.session_state:
    # Create model with conversational system instruction
    system_instruction = """You are a friendly, helpful, and knowledgeable AI assistant engaged in a natural conversation with the user.

Key characteristics:
- Maintain context from previous messages in the conversation
- Be warm and personable while remaining professional
- Ask clarifying questions when needed
- Provide detailed, accurate information
- Acknowledge when you don't know something
- Remember and reference earlier parts of the conversation
- Be concise but thorough
- Use a natural, conversational tone

Your goal is to have a genuine, helpful conversation with the user."""

    st.session_state.model = genai.GenerativeModel(
        'gemini-2.0-flash-exp',
        system_instruction=system_instruction
    )

# Sidebar
with st.sidebar:
    st.title("💬 Chat History")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_conversation_id = db.create_conversation("New Chat")
        st.session_state.messages = []
        st.rerun()

    conversations = db.get_all_conversations()

    if conversations:
        if st.button("🗑️ Clear All History", use_container_width=True, type="secondary"):
            db.clear_all_conversations()
            st.session_state.current_conversation_id = None
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")

    if conversations:
        for conv_id, title, created_at, updated_at in conversations:
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"📝 {title}", key=f"conv_{conv_id}", use_container_width=True):
                    st.session_state.current_conversation_id = conv_id
                    messages = db.get_conversation_messages(conv_id)
                    st.session_state.messages = [
                        {"role": role, "content": content}
                        for role, content, _ in messages
                    ]
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{conv_id}"):
                    db.delete_conversation(conv_id)
                    if st.session_state.current_conversation_id == conv_id:
                        st.session_state.current_conversation_id = None
                        st.session_state.messages = []
                    st.rerun()

# Main interface
st.title("🤖 Chatbot")

# Create conversation if none exists
if st.session_state.current_conversation_id is None:
    st.session_state.current_conversation_id = db.create_conversation("New Chat")

# Display messages
if not st.session_state.messages:
    # Welcome message for empty conversation
    welcome_msg = """👋 **Welcome! I'm your AI assistant.**

I can help you with:
- 💬 **Natural conversations** - Ask me anything and I'll remember our discussion
- 💡 **Questions & Answers** - Get detailed, thoughtful responses
- 🔍 **Context Awareness** - I maintain context throughout our entire conversation
- 🧠 **Knowledge & Reasoning** - Tap into my knowledge across many topics

**How I work:**
- I remember everything from our conversation and can reference previous messages
- I provide thoughtful, detailed answers
- I ask clarifying questions when needed
- I maintain a natural, friendly tone throughout our chat

What would you like to talk about today?"""

    st.markdown(f'<div class="assistant-message">{welcome_msg}</div>',
               unsafe_allow_html=True)
else:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message"><strong>You:</strong><br>{message["content"]}</div>',
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message"><strong>Assistant:</strong><br>{message["content"]}</div>',
                       unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    db.add_message(st.session_state.current_conversation_id, "user", user_input)

    # Update title if first message
    if len(st.session_state.messages) == 1:
        title = user_input[:50] + "..." if len(user_input) > 50 else user_input
        db.update_conversation_title(st.session_state.current_conversation_id, title)

    # Prepare conversation history
    conversation_history = []
    for msg in st.session_state.messages:
        conversation_history.append({
            "role": msg["role"],
            "parts": [msg["content"]]
        })

    try:
        # Start chat with conversation history
        chat = st.session_state.model.start_chat(history=conversation_history[:-1])

        # Generate response
        with st.spinner("💭 Thinking..."):
            response = chat.send_message(user_input)
            assistant_response = response.text

        # Add assistant response
        st.session_state.messages.append({"role": "model", "content": assistant_response})
        db.add_message(st.session_state.current_conversation_id, "model", assistant_response)

        st.rerun()

    except Exception as e:
        st.error(f"Error: {str(e)}")