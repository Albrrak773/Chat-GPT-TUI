# The following is a naming-convention explainer
# a Chat contains units of convertions
# a conversation contains units of messages
# a message is a pice of text that has meta data (like who it belongs to and what convertion it belongs to)
import sqlite3
import time
from typing import Literal
import asyncio
import aiohttp
CONVERSATOIN_TALE_NAME = "conversation"
MESSAGE_TABLE_NAME = "message"
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TITLE = "Untitled"

# a conversation is fully defined by its file. *so the actual conversation object is kinda of ephemeral*
class Chat():
    def __init__(self):
        self.con = sqlite3.connect("chat.db")
    
    def get_latest_conversation(self):
        with self.con:
            result = self.con.cursor().execute(f"SELECT * FROM {CONVERSATOIN_TALE_NAME} ORDER BY updated_at DESC LIMIT 1")
            return result.fetchone()

    def get_conversations(self) -> list:
        with self.con:
            result = self.con.cursor().execute(f"SELECT * FROM {CONVERSATOIN_TALE_NAME}")
            return result.fetchall()

    def get_conversation_by_id(self, id):
        with self.con:
            result = self.con.cursor().execute(f"SELECT * FROM {CONVERSATOIN_TALE_NAME} WHERE {CONVERSATOIN_TALE_NAME}.id = {id}")
            return result.fetchone()

    def create_conversation(self, model = DEFAULT_MODEL, title = DEFAULT_TITLE):
        """returns (id, model, title, created_at, updated_at, total_tokens)"""
        with self.con:
            result = self.con.cursor().execute(f"INSERT INTO {CONVERSATOIN_TALE_NAME} (model, title) VALUES (?, ?) RETURNING *", (model, title))
            result = result.fetchone()
            return Conversation(*result, self.con)
        

    def delete_conversation(self, id):
        with self.con:
            result = self.con.cursor().execute(f"DELETE FROM {CONVERSATOIN_TALE_NAME} WHERE {CONVERSATOIN_TALE_NAME}.id = {id} RETURNING *")
            return result.fetchone()
        
    def delete_All_conversation(self):
        with self.con:
            result = self.con.cursor().execute(f"DELTE FROM {CONVERSATOIN_TALE_NAME} RETURNING *")
            return result.fetchall()

class Conversation():

    def __init__(self, id, model, title, created_at, updated_at, total_tokens, con: sqlite3.Connection):
        self.id = id
        self.model = model
        self.title = title
        self.created_at = created_at
        self.updated_at = updated_at
        self.total_tokens = total_tokens
        self.con = con

    def get_messages(self):
        with self.con:
            result = self.con.cursor().execute(f"SELECT * FROM {MESSAGE_TABLE_NAME} WHERE {MESSAGE_TABLE_NAME}.id = {self.id} ORDER BY ")
            return result.fetchall()

    def add_message(self, content, owner: Literal["AI", "user"]):
        with self.con:
            result = self.con.cursor().execute(f"INSERT INTO {MESSAGE_TABLE_NAME} (conversation_id, content, owner) VALUES (?, ?, ?) RETURNING *", (self.id, content, owner))
            return result.fetchone()


    async def get_AI_response(self, prompt: str) -> str:
        async with aiohttp.ClientSession() as s:
            async with s.get("https://jsonplaceholder.typicode.com/todos/1") as res:
                if res.status == 200:
                    json = await res.json()
                    return json['title']

    async def add_exchange(self, prompt: str) -> tuple[tuple, tuple]:
        """An Endpoint that manages all thing necessary for an exchange that start from a user prompt
        return a tuple containg (AI message, user message) 
        """    
        user_message = self.add_message(prompt, "user")
        AI_response = await self.get_AI_response(prompt)
        AI_message = self.add_message(AI_response, "AI")
        return (user_message, AI_message)
    

if __name__ == "__main__":
    async def main():
        chat = Chat()
        conversation = chat.create_conversation()
        (user_message, AI_message ) = await conversation.add_exchange("say something laten")
        print("========================================")
        print(user_message)
        print("========================================")
        print(AI_message)
        print("========================================")
    asyncio.run(main())