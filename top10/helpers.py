import json

def save_json(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)
        print(f"Data saved to {filename}")

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data