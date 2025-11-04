import sqlite3
from datetime import datetime
import json

class ChatDatabase:
    def __init__(self, db_name="chat_history.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        ''')

        conn.commit()
        conn.close()

    def create_conversation(self, title="New Chat"):
        """Create a new conversation and return its ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO conversations (title) VALUES (?)', (title,))
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return conversation_id

    def get_all_conversations(self):
        """Get all conversations ordered by most recent"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, created_at, updated_at
            FROM conversations
            ORDER BY updated_at DESC
        ''')
        conversations = cursor.fetchall()
        conn.close()
        return conversations

    def add_message(self, conversation_id, role, content):
        """Add a message to a conversation"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Insert message
        cursor.execute('''
            INSERT INTO messages (conversation_id, role, content)
            VALUES (?, ?, ?)
        ''', (conversation_id, role, content))

        # Update conversation timestamp
        cursor.execute('''
            UPDATE conversations
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (conversation_id,))

        conn.commit()
        conn.close()

    def get_conversation_messages(self, conversation_id):
        """Get all messages from a specific conversation"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT role, content, timestamp
            FROM messages
            WHERE conversation_id = ?
            ORDER BY timestamp ASC
        ''', (conversation_id,))
        messages = cursor.fetchall()
        conn.close()
        return messages

    def update_conversation_title(self, conversation_id, title):
        """Update the title of a conversation"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE conversations
            SET title = ?
            WHERE id = ?
        ''', (title, conversation_id))
        conn.commit()
        conn.close()

    def delete_conversation(self, conversation_id):
        """Delete a conversation and all its messages"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Delete messages first (due to foreign key constraint)
        cursor.execute('DELETE FROM messages WHERE conversation_id = ?', (conversation_id,))

        # Delete conversation
        cursor.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))

        conn.commit()
        conn.close()

    def clear_all_conversations(self):
        """Delete all conversations and messages"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Delete all messages first
        cursor.execute('DELETE FROM messages')

        # Delete all conversations
        cursor.execute('DELETE FROM conversations')

        conn.commit()
        conn.close()
