import json

def load_suggestions(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_message_for(trigger_word):
    suggestions = load_suggestions('data/suggestion.json')
    for suggestion in suggestions:
        if suggestion['trigger'].lower() == trigger_word.lower():
            return suggestion['message']
    return "No suggestion found for this trigger."

# Test independently
if _name_ == "_main_":
    word = input("Enter trigger: ")
    print(get_message_for(word))