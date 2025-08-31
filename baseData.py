import os


DIRCTORY_NAME = "chat_Data"
IDS_PATH = f"{DIRCTORY_NAME}/list_of_ids.txt"
FIRSTTIME_PATH = f"{DIRCTORY_NAME}/is_first_Time.txt"
RECPONCE_PATH = f"{DIRCTORY_NAME}/recponce.json"
THE_KING_RECPONCE = f"{DIRCTORY_NAME}/the_king_recponce.json"
CONVER_PATH = f"{DIRCTORY_NAME}\conversations"

TOKEN = os.getenv("OpenAI_TestKey")
header = {
    "Content-Type" : "application/json",
    "Authorization": f"Bearer {TOKEN}",
    "OpenAI-Organization": "org-bGRLoPiK0yukTuka3L82Pd4V",
    "OpenAI-Project": "proj_KjQ2TeY1Z25SdNulVKESshgk"
}
endPoints = {
    "Chat": "https://api.openai.com/v1/chat/completions"
}

def getData(model, prompt):
    data = {
        "model": f"{model}", 
        "messages": 
            [
                {
                "role": "user", 
                "content": f"{prompt}"
                }
            ]
        }
    return data
