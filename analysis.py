import json

with open('responses.json', 'r', encoding = 'utf-8') as file:
    data = json.load(file)

responses = data['sentences']
embeddings = data['embeddings']

class Node:
    def __init__(self, value = None):
        self.value = value
        self.children = {}
        self.count = 1
    def __repr__(self):
        return f"Node(value = {self.value}, count = {self.count}, children = {list(self.children.keys())})"
    
root = Node(value = "ROOT")
    
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

def trie_to_node_link(root: Node):
    """
    Convertrs the trie into a node-link structure for 3D visualization
    """

    nodes_dict = {}
    node_info = {}
    links = []

    def dfs(node: Node, depth: int, parent_id: str = None):
        # Create an ID for this node based on (value, depth)
        node_id = f"{node.value}--{depth}"

        #If not yet in nodes_dict, append it
        if (node.value, depth) not in nodes_dict:
            nodes_dict[(node.value, depth)] = node_id
            node_info[node_id] = {
                'id': node_id,
                'label': node.value,
                'count': depth
            }

        #If there is a parent, create a link from parent to this node
        if parent_id is not None:
            links.append({
                'source': parent_id,
                'target': node_id
            })

        #Recursively call this function for all children
        for child_word, child_node in node.children.items():
            dfs(child_node, depth + 1, parent_id=node_id)

    #Start from the ROOT and build the final tree-link structure
    dfs(root, depth=0, parent_id = None)

    data = {
        'nodes': list(node_info.values()),
        'links': links
    }

    return data


for response in responses:
    #Tokenize the response into a word-based split
    tokens = response.strip().split()

    #Insert each sentence into the trie
    insert_sentence(root, tokens)

# #convert the trie to a dictionary for JSON storage
# trie_dict = export_trie_to_dict(root)

#Convert to node-link tree structure for 3D visualization
tree_dict = trie_to_node_link(root)

#Save the trie to a JSON file
with open('tree.json', 'w', encoding = 'utf-8') as file:
    json.dump(tree_dict, file, ensure_ascii = False, indent = 4)

    
