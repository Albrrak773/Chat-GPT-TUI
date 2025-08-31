# The following is a naming-convention explainer
# a Chat contains units of convertions
# a conversation contains units of messages
# a message is a pice of text that has meta data (like who it belongs to and what convertion it belongs to)
from baseData import header, endPoints, DIRCTORY_NAME, IDS_PATH, FIRSTTIME_PATH, RECPONCE_PATH, THE_KING_RECPONCE, CONVER_PATH
import datetime
import json
import requests
import os
import random
import math
import pprint
from pathlib import Path
import The_king as TK
import sys
os.system("cls")



def _generate_id():
    newId = random.randint(int(math.pow(2,10)), int( math.pow(2,50)))
    with open(IDS_PATH, 'r') as file:
        ids = file.readlines()
        for id in ids:
            if newId == id:
                newId = _generate_id()
                break
        ids.append("\n" + (str(newId)))
    with open(IDS_PATH, 'w') as file:
        file.writelines(ids)
    return newId

# a conversation is fully defined by its file. *so the actual conversation object is kinda of ephemeral*
class conversation():

    def __init__(self, model: str = "gpt-4o-mini", id: int = 0, title: str = "Untitled", messages:list = [] ,total_tokens: int = 0, date: datetime = datetime.datetime.today(), edited_date: datetime =datetime.datetime.today()):
        self.model = model
        self.id = id 
        self.title = title
        self.messages = messages
        self.total_tokens = total_tokens
        self.date = date
        self.edited_date = edited_date
        self.FILEPATH = f"{CONVER_PATH}/{self.title + ' - ' + str(self.id) }.json" #not part of the json file
        self._firstTime = True # not part of the json file
        
        # this constructs the JSON file based on the instance variables
        with open(self.FILEPATH, 'w') as file:
            json.dump(
                {
                    "model":f"{self.model}",
                    "id": f"{self.id}",
                    "title": f"{self.title}",
                    "total_tokens":f"{self.total_tokens}", 
                    "date": f"{self.date}", 
                    "edited_date": f"{self.edited_date}",
                    "messages": self.messages
                }, 
                file , 
                indent=4
                )

    def update_data(self, attribute:str, newValue):
        """updates the given attribute in both the the instance and in the JSON file, and any other place where applicable
            \nattributes are given as a string
            \nnew_value should be typed correctly based on the type of the attribute
        """
        print(f"UPDATING: ATTIBUTE: {attribute}, WITH NEW VALUE : {newValue}")
        attributs = ["model", "title", "total_tokens", "edited_date", "messages"]
        if attribute not in attributs:
            sys.exit(f"Error can't update attribute {attribute} since its not an attribute, or not a str")

        data = self.get_data()

        if attribute == "model":
            self.model = newValue
            data[attribute] = newValue
            
        if attribute == "total_tokens":
            self.total_tokens = newValue
            data[attribute] = f"{newValue}"

        if attribute == "messages":
            self.messages = newValue
            data[attribute] = newValue

        if attribute == "title":

            self.title = newValue
            data[attribute] = newValue

            JsonFile = Path(self.FILEPATH)
            self.FILEPATH = f"{CONVER_PATH}/{self.title + ' - ' + str(self.id) }.json"
            JsonFile.rename(self.FILEPATH)

            if attribute == "edited_date":
                self.edited_date = newValue
                data[attribute] = f"{newValue}"

        with open(self.FILEPATH, 'w') as file:
            json.dump(data, file, indent=4)

    def update_date(self):
        self.update_data("edited_date", datetime.datetime.today())

    def get_data(self) -> dict:
        """returns the JSON file data as python objects"""
        
        with open(self.FILEPATH, 'r') as file:
            data = json.load(file)
            return data
        
    def add_User_message(self, message:str):
        self.update_date()

        message_object = {"role": "user", "content": f"{message}"} # this is the object we want to append to the file
        data = self.get_data()    
        data['messages'].append(message_object)
        self.update_data("messages", data['messages'])


    def add_AI_message(self, message:str) -> None:
        self.update_date()

        print(f"Adding AI message: {message}")
        message_object = {"role": "assistant", "content": f"{message}"} # this is the object we want to append to the file
        data = self.get_data()
        data['messages'].append(message_object)
        self.update_data("messages", data['messages'])

    def get_messsages(self) -> list:
        """returns the messages list []"""
        self.update_date()

        data = self.get_data()
        return data['messages']
        
    def _get_payload(self) -> dict:
        self.update_date()

        payload = {
            "model": self.model,
            "messages": self.get_messsages()
        }
        return payload
    
    def get_AI_answer(self, prompt:str) -> str:
        self.update_date()

        self.add_User_message(prompt)
        payload = self._get_payload()
        recponce = requests.post(endPoints["Chat"], json.dumps(payload), headers=header)

        with open(f"{DIRCTORY_NAME}/recponce.json", 'r+') as file:
            json.dump(recponce.json(), file, indent=4)
        answer = json.loads(json.dumps(recponce.json())) # convert recponce to a python object
        self.add_AI_message(answer["choices"][0]["message"]["content"])

        print(f"THE VALUE OF IS_FIRST_TIME IS: {self._firstTime}")

        if self._firstTime:
            self.give_title(self.get_messsages())
            self._firstTime = False

        return answer["choices"][0]["message"]["content"]
    
    def give_title(self, messages:list):
        print("Giving Title.....")
        if len(messages) != 2:
            self._firstTime = False
            return
        Title = TK.get_Title(messages)
        self.update_data("title", Title)



class Chat():

    def __init__(self):

        if not os.path.isdir(f"{DIRCTORY_NAME}"):
            print(f"the dir {DIRCTORY_NAME} dosn't exsist Adding it.")
            os.system(f"mkdir {DIRCTORY_NAME}")

        if not os.path.isdir(CONVER_PATH):
            print(f"the dir {CONVER_PATH} dosn't exsist Adding it.")
            os.system(f"mkdir {CONVER_PATH}")


        if not os.path.isfile(RECPONCE_PATH):
            print(f"the file {RECPONCE_PATH} doesn't exsist adding it.")
            with open(RECPONCE_PATH, 'w'):
                pass
        
        if not os.path.isfile(THE_KING_RECPONCE):
            print(f"the file {THE_KING_RECPONCE} doesn't exsist adding it.")
            with open(THE_KING_RECPONCE, 'w'):
                pass

        if not os.path.isfile(IDS_PATH):
            print(f"the file {IDS_PATH} doesn't exsist adding it.")
            with open(IDS_PATH, 'w'):
                pass

        if not os.path.isfile(FIRSTTIME_PATH): # if the file not exsit, create it
            print(f"the file {FIRSTTIME_PATH} doesn't exsist adding it.")
            with open(FIRSTTIME_PATH, 'w'):
                pass
    
        self.Conversations_list = []
        for JsonFile in Path(CONVER_PATH).iterdir():
            with open(JsonFile, 'r') as file:
                data = json.load(file)
            JsonFile.unlink()
            self.Conversations_list.append(
                conversation(
                    model= data['model'],
                    id= int(data['id']),
                    title= data['title'],
                    messages= data['messages'],
                    total_tokens= int(data['total_tokens']),
                    date= datetime.datetime.strptime((data['date']), '%Y-%m-%d %H:%M:%S.%f'),
                    edited_date= datetime.datetime.strptime(data['edited_date'], '%Y-%m-%d %H:%M:%S.%f')
                )
            )

        # check if any file contains no messages and delete it
        converList_copy = self.Conversations_list.copy()
        for convert in converList_copy:
            print(convert.messages)
            if not convert.messages:
                self.delete_conversation(convert.id)

        if any(Path(CONVER_PATH).iterdir()): # if there are any files in the 'conversation' dirctory set 'is_first_Time' to false
            print("Found Files in conver dir, setting to False...")
            self.update_FirstTime(False)
        else:
            print("DID NOT Find Files in conver dir, setting to True...")
            self.update_FirstTime(True)

    def create_conversation(self) -> conversation:
        id=_generate_id()
        self.Conversations_list.append(conversation(id=id))
        if self.isFirstTime():
            self.update_FirstTime(False)
        return self.Conversations_list[len(self.Conversations_list) - 1]

    def get_latest_conversation(self) -> conversation:
        if self.isFirstTime():
            print("IS FIRST TIME TRUE")
            return self.create_conversation()
        
        dates = {} # holds title and date i.e {"title 1 - 1451981498": datetimeObject }
        for conversation in self.Conversations_list:
            dates[conversation.id] = conversation.edited_date
        
        latest_Date = max(dates.values())
        for id, date in dates.items(): 
            if date == latest_Date:
                return self.get_conversation_by_id(id)

    def get_conversation_by_id(self, id:int) -> conversation:
        for conversation in self.Conversations_list:
            if int(conversation.id) == id:
                print("Found ")
                return conversation

    def isFirstTime(self) -> bool:
        with open(FIRSTTIME_PATH, 'r') as file:
            if file.readline() == "1":
                return True
            if file.readline() == "0":
                return False

    def update_FirstTime(self, FirstTime:bool) -> None:
        with open(FIRSTTIME_PATH, 'w') as file:
            if FirstTime:
                file.write('1')
            if not FirstTime:
                file.write('0')

    def delete_ALL_Conversations(self):
        with open(IDS_PATH, 'w'):
            pass
        with open(FIRSTTIME_PATH, 'w') as file:
            file.write('1')
        for file in Path(CONVER_PATH).iterdir():
            if file.is_file(): 
                file.unlink()

    def delete_conversation(self, conversation_id:int):
        print(f"Now deleting The file with id: {conversation_id}")
        deleted_id = 0
        # first delete from conversation_list
        for conversation in self.Conversations_list:
            if conversation_id == conversation.id:
                deleted_id = conversation.id
                self.Conversations_list.remove(conversation)
        
        # second we delete the file
        for JsonFile in Path(CONVER_PATH).iterdir():
            if int(JsonFile.name.split('-')[1].split('.')[0]) == deleted_id:
                JsonFile.unlink()
                return

    def get_conversations_list(self) -> list:
        return self.Conversations_list
    
    def get_conversation_names(self) -> list:
        """returns a name/id List, i.e [ [ 'title', id ], [ 'title 2', id]  ]"""
        conversation_names = []
        for conversation in self.Conversations_list:
            conversation_names.append([conversation.title, conversation.id])
        return conversation_names



if __name__ == '__main__':
    my_chat = Chat()
    # my_chat.create_conversation().get_AI_answer("what is the capital of sweeden?")
    # my_chat.create_conversation().get_AI_answer("just let you answer be the the name of the band, who made the 'back in black' song?")


