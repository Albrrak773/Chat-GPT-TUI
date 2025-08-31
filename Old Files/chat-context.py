# The following is a naming-convention explainer 
# a Chat contains units of convertions
# a conversation contains units of messages
# a message is a pice of text that has meta data (like who it belongs to and what convertion it belongs to)
import json
import requests
import os
import random
import math
import pprint
from baseData import header, endPoints, getData
from colors import color
import textwrap
os.system("cls")
logPath = "DataFiles/chats-logs.json"
idsPath = "DataFiles/list of ids.txt"
recponcePath = "DataFiles/recponce.json"



def generate_id():

    newId = random.randint(int(math.pow(2,10)), int( math.pow(2,50)))
    with open(idsPath, 'r') as file:
        ids = file.readlines()
        for id in ids:
            if newId == id:
                newId = generate_id()
                break
        ids.append("\n" + (str(newId)))
    with open(idsPath, 'w') as file:
        file.writelines(ids)
    return newId

def init_log():
    with open(idsPath, 'w') as file:
        file
    data = {
            "converstions": []
        }
    with open(logPath, 'w') as file:
        json.dump(data, file, indent=4)

def createNewChat(prompt, model:int):
    chat_id = generate_id()
    with open(logPath, 'r') as file:
        data = json.load(file)
    
    if model == 1:
        model = "gpt-4o-mini"
    if model == 2:
        model = "gpt-4o"

    chat = {
            "model": f"{model}",
            "chat-id":f"{chat_id}",
            "chat-title": "Untiteld",
            "messages":[
                {
                    "role": "user",
                    "content":f"{prompt}"
                }
            ]
        }
    
    data["converstions"].append(chat)

    with open(logPath, 'w') as file:
        json.dump(data, file, indent=4)

    return chat_id

def get_index(chat_id) -> int:
    with open(logPath, 'r') as file:
        data = json.load(file)
    data = data["converstions"]

    for i, item in enumerate(data):
        if int(item['chat-id']) == chat_id:
            return i
    raise SystemExit("ERROR something went wrong, couldn't find id!")

def add_message(chat_id, role:str, message):
    with open(logPath, 'r') as file:
        data = json.load(file)
    messages = data["converstions"][get_index(chat_id)]["messages"]
    messages.append(
        {
      "role": role,
      "content": message
        }
    )
    data["converstions"][get_index(chat_id)]["messages"] = messages
    with open(logPath, 'w') as file:
        json.dump(data, file, indent=4)

def get_messages(chat_id) -> list: # returns a list of messages [{role:use, contenet:what is the capital of japan?}, {role:assistant, content:the capital of japan is tokoy}]
    with open(logPath, 'r') as file: 
        data = json.load(file)
    data = data["converstions"][get_index(chat_id)]["messages"]
    return data

def get_model(chat_id) -> str:
    with open(logPath, 'r') as file: 
        data = json.load(file)
    data = data["converstions"][get_index(chat_id)]["model"]
    return data

def get_payload(chat_id): # returns the actual object  that will sent to the API
    payload = {
        "model": get_model(chat_id),
        "messages": get_messages(chat_id)
    }
    return payload

def edit_Title(chat_id, Title):
    with open(logPath, 'r') as file:
        data = json.load(file)
    data["converstions"][get_index(chat_id)]["chat-title"] = Title
    with open(logPath, 'w') as file:
        json.dump(data, file, indent=4)

def print_message(message=None, who=None): # This is dumb 
        spacer = "################################################################"
        if who == "assistant":
            print(f"{color['yellow']}{spacer}{color['None']}")
            print(textwrap.fill(message,width=70))
            print(f"{color['yellow']}{spacer}{color['None']}")
        elif who == "user":
            print(f"{color['green']}{spacer}{color['None']}")
            prompt = input("Enter a Prompt: ") # This is dumb 
            print(f"{color['green']}{spacer}{color['None']}")
            return prompt # This is dumb 
        elif who == None:
            SystemExit("ERROR print_message() Is missing the argument who")

def have_a_Chat(chat_id:int, initial_prompt:str):

    os.system("cls")
    spacer = "################################################################"
    prompt = initial_prompt
    print(f"{color['green']}{spacer}{color['None']}")
    print(f"Enter a Prompt: {initial_prompt}")
    print(f"{color['green']}{spacer}{color['None']}")

    while True:

        payload = get_payload(chat_id)
        recponce = requests.post(endPoints["Chat"], json.dumps(payload), headers=header)

        with open(recponcePath, 'r+') as file:
            json.dump(recponce.json(), file, indent=4)

        answer = json.loads(json.dumps(recponce.json())) # convert recponce to a python object
        answer = answer["choices"][0]["message"]["content"] # read the content of the AI's message
        print_message(answer, "assistant") 
        add_message(chat_id, "assistant", answer)

        prompt = print_message(who="user")
        if prompt.isdigit():
            if int(prompt) == 0:
                    Title = input("Give the converstoin a Title: ")
                    return Title
        add_message(chat_id, "user", prompt)

def is_input_valid(input:str, Numrange:int) -> bool:
    if  not input.isdigit():
        print("Error Please enter a number Not a character")
        os.system("cls")
        return False
    input = int(input)
    numbers = list(range(1, Numrange+1))
    if input not in numbers:
        print(f"Error Please choose one of thesse Numbers: {numbers}")
        os.system("cls")
        return False
    os.system("cls")
    return True

def main():
    init_log()

    while True:
        print(
                f"{color['green']}what do you want to do?{color['None']}",
                "\n1. continue Chat",
                "\n2. start New Chat",
                "\n3. List Chats",
                "\n4. Exit"
        )
        choice = input("\nChoose a number:")
        if not is_input_valid(choice, 4):
            continue
        else:
            choice = int(choice)
        if choice == 1:
            choice
        elif choice == 2:
            while True:
                model = input(f"{color['green']}which model do you want to use?{color['None']}\n1.gpt-4o-mini\n2.gpt-4o\nEnter a Number: ")
                if not is_input_valid(model,2):
                    continue
                else:
                    break
            prompt = input("Enter a prompt: ")
            id = createNewChat(prompt, int(model))
            Title = have_a_Chat(id, prompt)
            edit_Title(id, Title)
            os.system('cls')
        elif choice == 3:
            choice
        elif choice == 4:
            print("Exiting the program....")
            break




if __name__ == "__main__":
    main()