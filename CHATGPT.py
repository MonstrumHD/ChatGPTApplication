import openai
import time
import re
import auth as key
from InquirerPy import prompt

openai.api_key = key.thekey

def question(text):
    questions = {
        'type': 'input',
        'name': 'prompt',
        'message': text
    }

    return prompt(questions)

def setkey(text):
    inputs = question(text)['prompt']
    if inputs.find('sk-') == -1:
        print('    Incorrect API Key!! Re-Insert Key Below, Key can be found at "https://beta.openai.com/account/api-keys"')
        setkey('API KEY: ')
    else:
        with open("auth.py", "r") as f:
            data = f.read()
            data = re.sub(key.thekey, inputs, key.thekey)
            data = 'thekey = "'+data+'"'

        with open("auth.py", "w") as f:
            f.write(data)

        openai.api_key = re.sub(key.thekey, inputs, key.thekey)

def ask():
    print('')
    prompt = question('What is your question?')['prompt']

    try:
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5
        )
    except:
        print('')
        print('Incorrect API Key!! Re-Insert Key Below, Key can be found at "https://beta.openai.com/account/api-keys"')
        setkey('API KEY: ')
        ask()
    else:
        print(completions.choices[0].text)
        time.sleep(0.5)
        print('')
        ask()

if key.thekey == "":
    print('Hello New User, This application communicates to ChatGPT on your computer so you do not have to deal with the website. Insert your API Key below from "https://beta.openai.com/account/api-keys" to get started.')
    print('')
    setkey('API KEY: ')
    ask()
elif key.thekey.find('sk-') == -1:
    print('    Insert API Key below, Key can be found at "https://beta.openai.com/account/api-keys"')
    print('')
    setkey('API KEY: ')
    ask()

ask()
