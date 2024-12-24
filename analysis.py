import json
import torch

with open('responses.json', 'r', encoding = 'utf-8') as file:
    data = json.load(file)

responses = data['sentences']
embeddings = data['embeddings']
embeddings = torch.tensor(embeddings)

class Node:
    def __init__(self, value = None):
        self.value = value
        self.children = {}
        self.count = 1
    def __repr__(self):
        return f"Node(value = {self.value}, count = {self.count}, children = {list(self.children.keys())})"
    
def insert_sentence(root: Node, tokens: list[str]) -> None:
    """
    Inserts the tokens of a single sentence into the trie
    Only merges nodes if both the word and position (index in original sentence) are the same 

    """

    current = root
    for word in tokens:
        #If this word does not exist among current node's children, create a new child
        if word not in current.children:
            current.children[word] = Node(value = word)

        #If a child with the same word already exists, increase it's count
        else:
            current.children[word].count += 1

        current = current.children[word]

def export_trie_to_dict(node: Node):
    """
    Recursively converts the trie to a dictionary for JSON export
    
    """

    return {
        'value': node.value,
        'count': node.count,
        'children': {
            child_word: export_trie_to_dict(child_node) for child_word, child_node in node.children.items()      
        }
    }



root = Node(value = "ROOT")

for response in responses:
    #Tokenize the response into a word-based split
    tokens = response.strip().split()

    #Insert each sentence into the trie
    insert_sentence(root, tokens)

#convert the trie to a dictionary for JSON storage
trie_dict = export_trie_to_dict(root)

#Save the trie to a JSON file
with open('trie.json', 'w', encoding = 'utf-8') as file:
    json.dump(trie_dict, file, ensure_ascii = False, indent = 4)

    
