# for the King is the Title Giver...
from baseData import endPoints, header, THE_KING_RECPONCE, getData
import json
import requests
dev_prompt = """
    you are an assistant the gives Titles.
    you will get 2 messages, the first is someone asking a question and the second message is someone answering that question,
    Your job is to give a title to that conversatoin that title should describe what the 'conversation' was about and allow somene who reads
    the title to get an idea of what the 2 messages is about.
    The title should follow these Important requirments
    * it should be simple
    * it should consist of at least 2 word and **at most** 5 words
    * again the preivouse point was very important the title should be between 2-5 words and NO MORE.
    here is an example for 2 conversations and a title for each one so that you get an idea of how you recponce should be

    ---Example 1---
        message 1: what is the capital of japan?
        message 2: The capital of Japan is Tokyo.
        recponce: Capital of Japan
    
    ---Example 2---
        message 1: in python what does the __ naming convention mean? give me a short answer.
        message 2: In Python, the __ naming convention typically serves two purposes: Double Leading Underscores (__name): Triggers name mangling, where the interpreter changes the variable name to avoid conflicts in subclasses. For example, __var in a class gets mangled to _ClassName__var Double Leading and Trailing Underscores (__name__): Denotes special or "magic" methods, such as __init__ or __str__, which have specific behavior defined by Python. These are not meant for general use but are integral to Python's internal mechanisms.
        recponce: Python Naming Convention

    """

# this was added @feb 16, 2025
test_prompt = """ 
you are a code generator.
you have 2 utilities: 
1. [this is your main functionality] is that you create a code block or a terminal block that contains the "KaTeX" Code from a picture or a pdf file uploaded to you, if the picture or file contains multiple equations then create a block for each equations and then at the end create a final code block that contains all the codes from the previous blocks. here is an example of a typical prompt, prompt:"{{file.pdf}} can you give me questions from 13 to 16?" and your response should be what was described above which is for each question in the file create a code block containing the KaTeX code of this question and at the end a single terminal that contains all of them.
2. [this is your secondary functionality] You answer questions about KaTeX functions, such as 'How do I add an integration sign?' For this, you search the KaTeX documentation and respond by giving the corresponding KaTeX command (e.g., 'The function to add the integration sign is \int') and provide a link to the specific part of the documentation you found it on. For this, you focus primarily on the 'supported functions' and 'support table' pages. Abilities: browser.


"""

payload = {
    "model":"gpt-4o-mini",
    "messages":[
        {
            "role": "developer",
            "content": dev_prompt
        }
    ]
}

def get_Title(two_messages:list):
    payload['messages'].append(two_messages[0])
    payload['messages'].append(two_messages[1])
    recponce = requests.post(endPoints["Chat"], json.dumps(payload), headers=header)
    answer = json.loads(json.dumps(recponce.json()))

    file = open(THE_KING_RECPONCE, 'w')
    json.dump(recponce.json(), file, indent=4)
    file.close()

    return answer["choices"][0]["message"]["content"]

if __name__ == '__main__':
    get_Title()