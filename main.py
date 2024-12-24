from openai import OpenAI
import json
from tqdm import tqdm

responses = []
embeddings = []
iterations = 3

DEBUG = 1

def debug(level, *args, **kwargs):
    if DEBUG == 1 and level >= 1:
        print(*args, **kwargs)
    if DEBUG == 2 and level == 2:
        print(*args, **kwargs)
    if DEBUG == 3 and level == 3:
        print(*args, **kwargs)
    if DEBUG == 4:
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
    debug(2, completion)
    return completion

def get_embedding(text):
    embedding = client.embeddings.create(
        model = 'text-embedding-ada-002',
        input = text,
        encoding_format = 'float'
    )
    debug(3, embedding)
    return embedding.data[0].embedding

# Gather responses from ChatGPT
for i in tqdm(range(iterations)):
    completion = get_response()
    response = completion.choices[0].message.content
    embedding = get_embedding(response)
    debug(1, 'Unparsed Response {i}: ', response)
    debug(1, 'Embedding fetched {i}')
    #add Intelligence is to the beginning of the response if not already present
    response = response.strip()
    response = response.lower()
    if not response.startswith('intelligence is'):
        response = 'intelligence is ' + response
    debug(1, 'Parsed Response {i}: ', response)
    responses.append(response)
    embeddings.append(embedding)
    debug(1, 'Appended responses and embeddings')

data = {
    'sentences': responses,
    'embeddings': embeddings
}

debug(1, 'data dictionary created')

with open("responses.json", 'w', encoding = 'utf-8') as f:
    json.dump(data, f, ensure_ascii = False, indent = 4)

print('JSON file saved as *responses.json*')




