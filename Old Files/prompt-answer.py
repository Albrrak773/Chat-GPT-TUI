import json
import os
import requests
from baseData import header, endPoints, getData
os.system("cls")

def main():
    while True:
        model_choice = int(input("What model do you want to use?\n1. gpt-4o-mini\n2. gpt-4o\n0. Exit\nEnter Number:"))
        if model_choice == 0:
            print("Closing the program...")
            break
        elif model_choice == 1:
            model = "gpt-4o-mini"
            os.system("cls")
        elif model_choice == 2:
            model = "gpt-4o"
            os.system("cls")
        else:
            os.system("cls")
            print("\nERROR Please choose 1 OR 2")
            continue
        prompt = input("Type a prompt:")
        
        if prompt.isdigit() and int(prompt) == 0:
            print("Closing the program...")
            break
        
        data = getData(model, prompt)
        recponce = requests.post(endPoints["Chat"], headers=header, data=json.dumps(data))
        with open("DataFiles/recponce.json", 'r+') as file:
                file.truncate(0)
                json.dump(recponce.json(), file, indent="    ")

        if recponce.status_code == 200:
            recponce_Py = json.loads(json.dumps(recponce.json()))
            answer = recponce_Py["choices"][0]["message"]["content"]
            tokens = recponce_Py["usage"]["total_tokens"]
            print(f"{answer}\n\033[31mTokens Used:{tokens}\033[0m")
        else:
            print(f"Something Went wrong Error Code: {recponce.status_code}, Look at the file for more details")
        


if __name__ == '__main__':
    main()