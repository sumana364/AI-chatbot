# 🤖 Streamlit Chatbot using Gemini API

This project is a **conversational AI chatbot** built with **Streamlit** and **Google Gemini API**, designed for natural, context-aware interactions. It also includes a **local conversation history database** to save and manage previous chats.

---

## 🚀 Features

- 💬 **Real-time conversation interface** built with Streamlit  
- 🧠 **Context retention** across messages for natural chat flow  
- 🗃️ **Chat history management** (create, view, and delete chats)  
- 🔐 **Environment variable support** using `.env` and `python-dotenv`  
- 💡 **Custom system instructions** to define chatbot personality and tone  
- ⚙️ **Database integration** for persistent conversations  

---

## 🛠️ Technologies Used

| Component | Technology |
|------------|-------------|
| Frontend | Streamlit |
| AI Model | Google Gemini API |
| Environment Management | python-dotenv |
| Database | Custom SQLite wrapper (ChatDatabase) |
| Language | Python 3.10+ |

---

## 📂 Project Structure

```
├── app.py                                     # Main Streamlit app
├── database.py                                # Database for conversation storage
├── .env                                       # Contains GEMINI_API_KEY
├── requirements.txt                           # Required dependencies
└── README.md                                  # Project documentation
```

---

## ⚙️ Installation

1. **Clone this repository**  
   ```bash
   git clone https://github.com/yourusername/chatbot-gemini-streamlit.git
   cd chatbot-gemini-streamlit
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**  
   Create a `.env` file and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the application**  
   ```bash
   streamlit run 3474ba77-3d2a-429a-9c11-2fc7e6ebea67.py
   ```

---

## 💾 Database Features

- All chat sessions are stored locally
- Users can **create**, **view**, **delete**, or **clear** conversations
- Data is persisted even after app restart

---

## 💡 Example Use Cases

- Personal AI assistant for productivity  
- Learning chatbot for education apps  
- Contextual customer support bot  
- Research assistant for summarization and Q&A  

---

## 📜 License

This project is open-source and available under the **MIT License**.

---

### 👤 Author
**Sumanasri**  
B.Tech (ECE) Graduate | Tech Enthusiast | Aspiring Developer

---
