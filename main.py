from openai import OpenAI
import json
from tqdm import tqdm

responses = []
iterations = 20

DEBUG = False

def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

client = OpenAI()
def get_response():
    completion = client.chat.completions.create(
        model = 'gpt-4o',
        store = False,
        messages = [
            {
            'role': 'system',
            'content': 'Complete the phrase in only one sentence of length no more than 250 tokens.'
            },
            {
            'role': 'user', 
            'content': 'Complete the phrase: Intelligence is...'
            } 
        ]
    )
    return completion

# Gather responses from ChatGPT
for i in tqdm(range(iterations)):
    completion = get_response()
    response = completion.choices[0].message.content
    debug('Unparsed Response {i}: ', response)
    #add Intelligence is to the beginning of the response if not already present
    response = response.strip()
    response = response.lower()
    if not response.startswith('intelligence is'):
        response = 'intelligence is ' + response
    debug('Parsed Response {i}: ', response)
    responses.append(response)

data = {
    'sentences': responses
}

debug('data dictionary created')

with open("responses.json", 'w', encoding = 'utf-8') as f:
    json.dump(data, f, ensure_ascii = False, indent = 4)

print('JSON file saved as *responses.json*')




